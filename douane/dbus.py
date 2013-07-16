import dbus
from dbus.mainloop.glib import DBusGMainLoop

class DBusServiceNotFoundError(Exception):
	pass

class DBusClient(object):

	def __init__(self):
		# Open the Session bus
		self.__bus = dbus.SystemBus(mainloop=DBusGMainLoop())

		self.__dbus_serive_name = "org.zedroot.Douane"
		self.__dbus_serive_path = "/org/zedroot/Douane"

		# Try to connect to the Dounae service
		try:
			self.__service_douane = self.__bus.get_object(self.__dbus_serive_name,
														  self.__dbus_serive_path)
			self.__properties_interface = dbus.Interface(self.__service_douane,
														 "org.freedesktop.DBus.Properties")
		except dbus.DBusException:
			raise DBusServiceNotFoundError("D-Bus service %s not found." % self.__dbus_serive_name)

	def get_property(self, name):
		try:
			return self.__properties_interface.Get(self.__dbus_serive_name, name)
		except dbus.DBusException as error:
			raise DBusServiceNotFoundError(error)

	def call(self, method, argument):
		try:
			return self.__service_douane.get_dbus_method(method, self.__dbus_serive_name)(argument)
		except dbus.DBusException as error:
			raise DBusServiceNotFoundError(error)
