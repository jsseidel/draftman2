import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import signal
import sys
from AppWindowSignalHandler import AppWindowSignalHandler
from lib.Project import Project

def main():
    project = None
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    builder = Gtk.Builder()
    builder.add_from_file('%s/draftman2.glade' % os.path.dirname(os.path.realpath(__file__)))
    builder.connect_signals(AppWindowSignalHandler(project))
    app_window = builder.get_object('appWindow')
    app_window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()


