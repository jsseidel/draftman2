import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import signal
from handlers.AppWindowHandlerRouter import AppWindowHandlerRouter

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    builder = Gtk.Builder()
    builder.add_from_file('%s/draftman2.glade' % os.path.dirname(os.path.realpath(__file__)))
    builder.connect_signals(AppWindowHandlerRouter())
    app_window = builder.get_object('appWindow')
    app_window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()


