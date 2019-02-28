import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.progress_bar import ProgressBarDialog
from gui.handler import encode, decode, psnr


class DialogError(Gtk.Dialog):

    def __init__(self, parent):
        self.data = {}
        Gtk.Dialog.__init__(self, "Error", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_border_width(10)

        box = self.get_content_area()
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        box.add(grid)

        label = Gtk.Label()
        label.set_markup("<big><b>Error</b></big>")
        label.set_justify(Gtk.Justification.CENTER)
        separator = Gtk.HSeparator()
        label_sub = Gtk.Label(str(parent.error))

        grid.attach(label, 0, 0, 2, 2)
        grid.attach(separator, 0, 2, 2, 1)
        grid.attach(label_sub, 0, 3, 2, 1)

        self.show_all()
