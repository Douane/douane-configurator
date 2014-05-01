from gi.repository import Gtk, GdkPixbuf
import os

class DouaneAboutDialog(Gtk.AboutDialog):

  def __init__(self):
    Gtk.AboutDialog.__init__(self)

    self.set_logo(GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "douane.png")))
    self.set_program_name("Douane configurator")
    self.set_version("UNKNOWN")
    self.set_copyright("Guillaume Hain")
    self.set_comments("Configurator for Douane firewall at application layer.")
    self.set_license("Distributed under the GPL v2 license")
    self.set_authors(["Guillaume Hain"])
    self.set_website("http://douaneapp.com/")
    self.set_website_label("Douane website")
