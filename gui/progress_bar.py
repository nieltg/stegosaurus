import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class ProgressBarDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Progress", parent, 0)
        self.set_border_width(10)

        box = self.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(0.0)
        vbox.pack_start(self.progressbar, True, True, 0)

        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)
        self.activity_mode = False

        self.show_all()

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        self.progressbar.pulse()
        return True
