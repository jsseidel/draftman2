"""
Message

This class is used to deliver messages to the user as well as
confirmations.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Message:

    def warning(self, app_window, msg_title, msg):
        dialog = Gtk.MessageDialog(app_window, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, msg_title)
        dialog.format_secondary_text(msg)
        dialog.run()
        dialog.destroy()

