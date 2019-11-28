import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import signal
import sys
from AppWindowSignalHandler import AppWindowSignalHandler
from lib.Project import Project

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Create a new project that is the only project object
    # we'll use for this instance.
    project = Project()

    # Use a builder to create our objects from the glade
    # file.
    builder = Gtk.Builder()
    builder.add_from_file('%s/draftman2.glade' %
            os.path.dirname(os.path.realpath(__file__)))

    # Get a pointer to our main app window
    app_window = builder.get_object('appWindow')
    builder.connect_signals(AppWindowSignalHandler(builder, project))


    app_window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()


