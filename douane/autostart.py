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

  def rclocal_path(self):
    return "/etc/rc.local"

  def is_installed(self):
    return "modprobe douane" in open(self.rclocal_path()).read() and \
      os.path.exists(self.user_autostart_path())

  def install(self):
    if subprocess.call(["pkexec", "/etc/init.d/douane", "installautostart"], stdout=subprocess.DEVNULL) == 0:
      with open(self.user_autostart_path(), "w") as desktop_file:
        desktop_file.write("""[Desktop Entry]
Type=Application
Version=1.0
Name=Douane
GenericName=Douane
Comment=Douane application
Exec=pkexec /etc/init.d/douaned start
Terminal=false
Categories=GTK;Utility;
StartupNotify=true
                           """)
      return True
    else:
      return False

  def uninstall(self):
    if subprocess.call(["pkexec", "/etc/init.d/douane", "uninstallautostart"], stdout=subprocess.DEVNULL) == 0:
      os.remove(self.user_autostart_path())
      return True
    else:
      return False
