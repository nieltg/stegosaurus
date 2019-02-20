import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class ProgressBarDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Progress", parent, 0)
        self.set_border_width(10)
        
        GLib.threads_init()
        box = self.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(0.0)
        self.text = Gtk.Label("0 % completed")
        vbox.pack_start(self.progressbar, True, True, 0)
        vbox.pack_start(self.text, True, True, 0)

        self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)
        self.activity_mode = False

        self.show_all()

    def on_timeout(self, user_data):
        new_val = self.progressbar.get_fraction() + 0.01
        self.progressbar.set_fraction(new_val)
        self.text.set_text(str(int(new_val*100-1))+" % completed")
        return True
