import os
import re
import subprocess

class Autostart(object):

  def user_autostart_path(self):
    config_autostart_path = os.getenv("HOME") + "/.config/autostart/"

    # Ensure that autostart path exists
    if not os.path.exists(config_autostart_path):
      os.makedirs(config_autostart_path)

    return config_autostart_path + "douane.desktop"

  def is_installed(self):
    return os.path.exists(self.user_autostart_path())

  def install(self):
    with open(self.user_autostart_path(), "w") as desktop_file:
      desktop_file.write("""[Desktop Entry]
Type=Application
Version=1.0
Name=Douane
GenericName=Douane
Comment=Douane application
Exec=/opt/douane/bin/douane-dialog
Terminal=false
Categories=GTK;Utility;
StartupNotify=true""")
    return True

  def uninstall(self):
    os.remove(self.user_autostart_path())
