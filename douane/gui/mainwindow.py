import os
import time

from gi.repository import Gtk
from gtktwitterbox.twitter import GtkTwitterBox
from douane.dbus import DBusClient, DBusServiceNotFoundError
from douane.gui.aboutdialog import DouaneAboutDialog
from douane.autostart import Autostart
from subprocess import call

class MainWindow(Gtk.Window):

    def __init__(self):
        self.__disable_triggers = True
        self.__dbus_client = None

        self.builder = Gtk.Builder()
        # self.builder.set_translation_domain(PACKAGE)
        self.builder.add_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "glade", "mainwindow.glade"))
        self.builder.connect_signals(self)

        # Get the main window object, show all widgets and hook to the delete-event
        self.window_main = self.builder.get_object("windowMain")
        self.window_main.set_icon_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "douane_128.png"))
        self.window_main.show_all()
        self.window_main.connect("delete-event", self.quit_configurator)

        self.__image_douane_logo = self.builder.get_object("imageDouaneLogo")
        self.__image_douane_logo.set_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "douane_128.png"))

        self.__box_enable_douane = self.builder.get_object("boxEnableDouane")
        self.__label_enable_douane = self.builder.get_object("labelEnableDouane")
        self.__switch_enable_douane = self.builder.get_object("switchEnableDouane")

        self.__switch_autostart_douane = self.builder.get_object("switchAutostartDouane")

        self.__initial_label_enable_douane_text = self.__label_enable_douane.get_label()

        # liststore is the object representing all the lines of the Gtk Treeview widget for Rules
        self.__list_store_rules = self.builder.get_object("liststoreRules")

        self.__refresh_rules_button = self.builder.get_object("buttonRefreshRules")
        self.__treeview_rules = self.builder.get_object("treeviewRules")
        self.__treeview_rules.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.builder.get_object("treeviewcolumnSHA256").set_visible(False)

        # Context menu on right clicking on the Gtk::Treeview
        menu = Gtk.Menu()
        sub_menu_delete = Gtk.MenuItem("Delete")
        sub_menu_delete.connect("activate", self.on_submenuDelete_clicked)
        menu.append(sub_menu_delete)
        menu.show_all()
        self.__treeview_rules.connect("button-press-event", self.on_treeviewRules_button_press_event, menu)

        # Build an error icon that will be shown when something went wrong
        self.__warning_icon = self._build_warning_icon()

        # Connect D-Bus client to the daemon D-Bus server
        self._connect_dbus()

        self.__switch_autostart_douane.set_active(Autostart().is_installed())

        self.__disable_triggers = False

        # Initialize and start the Twitter box
        self.__box_configurator_and_twitter = self.builder.get_object("boxConfiguratorAndTwitter")
        self.__twitter_box = GtkTwitterBox(self.__box_configurator_and_twitter, "douaneapp", 15)

    # ~~~~ Events ~~~~
    def on_buttonAbout_clicked(self, widget):
        aboutdialog = DouaneAboutDialog()
        aboutdialog.connect("response", self.on_AboutDialog_close)
        aboutdialog.show()

    def on_AboutDialog_close(self, action, parameter):
        action.destroy()

    def on_buttonQuit_clicked(self, widget):
        self.quit_configurator()

    def on_switchEnableDouane_active_notify(self, widget, active):
        # Do nothing during initialization phase
        if self.__disable_triggers: return

        if widget.get_active():
            call(["pkexec", "/etc/init.d/douane", "start"])
            self._reconnect_dbus()
        else:
            call(["pkexec", "/etc/init.d/douane", "stop"])

    def on_switchAutostartDouane_active_notify(self, widget, active):
        # Do nothing during initialization phase
        if self.__disable_triggers: return

        if widget.get_active():
            Autostart().install()
        else:
            Autostart().uninstall()

    def on_buttonRefreshRules_clicked(self, widget):
        self._fetch_rules_and_populate_treeview()

    def on_treeviewRules_button_press_event(self, widget, event, menu):
        if event.button == 3:
            menu.popup(None, None, None, None, event.button, event.get_time())
            return True
        return False

    def on_submenuDelete_clicked(self, menu):
        (model, pathlist) = self.__treeview_rules.get_selection().get_selected_rows()
        pathlist.reverse()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            try:
                if(self.__dbus_client.call("DeleteRule", model.get_value(tree_iter, 1))):
                    self._fetch_rules_and_populate_treeview()
                else:
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Unable to delete rule")
                    dialog.format_secondary_text("At least one of the selected rule hasn't been found.")
                    dialog.run()
                    dialog.destroy()
            except douane.dbus.DBusServiceNotFoundError as error:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Unable to delete rule")
                dialog.format_secondary_text(str(error))
                dialog.run()
                dialog.destroy()

    # ~~~~ Methods ~~~~
    # Warning icon
    def _build_warning_icon(self):
        warning_icon = Gtk.Image()
        warning_icon.set_from_stock("gtk-dialog-warning", Gtk.IconSize.BUTTON)
        warning_icon.show()

        image_alignment = Gtk.Alignment(xalign = 0.5, yalign = 0.5, xscale = 0, yscale = 0)
        image_alignment.set_padding(5, 5, 5, 5);
        image_alignment.add(warning_icon)
        image_alignment.show()

        self.__box_enable_douane.pack_start(image_alignment, False, True, 0)

        return warning_icon

    def _dbus_service_error(self, error):
        self.__label_enable_douane.set_markup('<span color="red">' + self.__initial_label_enable_douane_text + '</span>')
        # Updated error icon tool tip with the error message and show it
        self.__warning_icon.set_tooltip_text(str(error))
        self.__warning_icon.show()
        self.__refresh_rules_button.set_sensitive(False)
        self.__refresh_rules_button.set_tooltip_text("D-Bus client disconnected")

    def _dbus_service_success(self):
        self.__label_enable_douane.set_markup(self.__initial_label_enable_douane_text)
        self.__warning_icon.hide()
        self.__refresh_rules_button.set_sensitive(True)
        self.__refresh_rules_button.set_tooltip_text("Reload all the rules from the daemon")

    def _fetch_rules_and_populate_treeview(self):
        # Load existing rules from the daemon
        try:
            # Fetch rules from daemon through D-Bus
            rules = sorted(self.__dbus_client.call("GetRules", None))
            # As we received rules clean existing rules
            self.__list_store_rules.clear()
            # Create a line for each rules
            for (sha256, path, allowed) in rules:
                if allowed:
                    self.__list_store_rules.append([path, sha256, "allowed"])
                else:
                    self.__list_store_rules.append([path, sha256, "disallowed"])
        except DBusServiceNotFoundError as error:
            self._dbus_service_error(error)

    def quit_configurator(self, *args):
        self.__disable_triggers = True
        self.__twitter_box.kill()
        Gtk.main_quit()

    def _connect_dbus(self):
        self._reconnect_dbus()

    def _reconnect_dbus(self):
        error_count = 0

        # We try 3 times to contact the D-Bus server
        # before to concider it as offline
        while True:
            try:
                # Initiliaze the D-Bus client
                self.__dbus_client = DBusClient()

                # Show the status of the daemon by updating the Gtk.Switch state
                self.__switch_enable_douane.set_active(True)

                self._dbus_service_success()

                self._fetch_rules_and_populate_treeview()

                break
            except DBusServiceNotFoundError as error:
                error_count += 1
                if error_count >= 3:
                    self._dbus_service_error(error)
                    break
                else:
                    time.sleep(1)
