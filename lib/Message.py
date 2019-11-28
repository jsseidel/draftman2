"""
Message

This class is used to deliver messages to the user as well as
confirmations.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Message:

    def __message(self, app_window, msg_title, msg, msg_type):
        dialog = Gtk.MessageDialog(app_window, 0, msg_type,
            Gtk.ButtonsType.OK, msg_title)
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()

    def warning(self, app_window, msg_title, msg):
        self.__message(app_window, msg_title, msg, Gtk.MessageType.WARNING)

    def error(self, app_window, msg_title, msg):
        self.__message(app_window, msg_title, msg, Gtk.MessageType.ERROR)

    def info(self, app_window, msg_title, msg):
        self.__message(app_window, msg_title, msg, Gtk.MessageType.INFO)

    def confirm(self, app_window, msg_title, msg):
        dialog = Gtk.MessageDialog(app_window, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, msg_title)
        dialog.format_secondary_text(msg)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True

        return False

