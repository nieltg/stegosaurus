import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from progress_bar import ProgressBarDialog


class DialogVideo(Gtk.Dialog):

    def __init__(self, parent):
        self.data = {}
        Gtk.Dialog.__init__(self, "Stegosaurus Video", parent, 0)
        self.set_border_width(10)

        box = self.get_content_area()
        notebook = Gtk.Notebook()
        box.add(notebook)

        page1 = self.get_hide_msg_window()
        page1.set_border_width(10)
        notebook.append_page(page1, Gtk.Label('Hide'))

        page2 = self.get_extract_msg_window()
        page2.set_border_width(10)
        notebook.append_page(page2, Gtk.Label('Extract'))

        self.show_all()

    def on_file_selected(self, widget, name):
        self.data[name] = widget.get_filename()

    def get_hide_msg_window(self):
        self.data = {
            "filename": "",
            "key": "",
            "text_path": "",
            "frame_mode": "acak",
            "pixel_mode": "acak"
        }
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed", self.on_file_selected, "filename")
        key_entry = Gtk.Entry()
        button_open_text = Gtk.FileChooserButton("Open File")
        button_open_text.set_width_chars(15)
        button_open_text.connect("selection-changed", self.on_file_selected, "text_path")

        hbox1 = Gtk.Box()
        btn_frame_acak = Gtk.RadioButton.new_with_label_from_widget(None, "Frame Acak")
        btn_frame_acak.connect(
            "toggled", self.on_button_toggled, ("frame_mode","acak"))

        btn_frame_seq = Gtk.RadioButton.new_from_widget(btn_frame_acak)
        btn_frame_seq.set_label("Frame Sequential")
        btn_frame_seq.connect(
            "toggled", self.on_button_toggled, ("frame_mode", "seq"))
        hbox1.pack_start(btn_frame_acak, True, True, 10)
        hbox1.pack_start(btn_frame_seq, True, True, 10)

        hbox2 = Gtk.Box()
        btn_pixel_acak = Gtk.RadioButton.new_with_label_from_widget(
            None, "Pixel Acak")
        btn_pixel_acak.connect(
            "toggled", self.on_button_toggled, ("pixel_mode", "acak"))

        btn_pixel_seq = Gtk.RadioButton.new_from_widget(btn_pixel_acak)
        btn_pixel_seq.set_label("Pixel Sequential")
        btn_pixel_seq.connect(
            "toggled", self.on_button_toggled, ("pixel_mode", "seq"))
        hbox2.pack_start(btn_pixel_acak, True, True, 10)
        hbox2.pack_start(btn_pixel_seq, True, True, 10)
        
        btn_encrypt_and_hide = Gtk.Button("Encrypt & Hide")
        btn_encrypt_and_hide.connect("clicked", self.on_button_submit, {
            "key_entry": key_entry
        })


        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("Text"), 0, 2, 1, 1)
        grid.attach(button_open_text, 1, 2, 3, 1)
        grid.attach(hbox1, 0, 3, 4, 1)
        grid.attach(hbox2, 0, 4, 4, 1)
        grid.attach(btn_encrypt_and_hide, 0, 5, 4, 1)

        return grid

    def on_button_toggled(self, button, data):
        if button.get_active():
            self.page1[data[0]] = data[1]

    def on_button_submit(self, button, additional_data):
        self.data["key"] = additional_data["key_entry"].get_text()
        if additional_data.get("save_path"):
            self.data["save_path"] = additional_data["save_path"].get_text()
        print(self.data)
        dialog = ProgressBarDialog(self)
        response = dialog.run()

        dialog.destroy()

    def get_extract_msg_window(self):
        self.data = {
            "filename": "",
            "key": "",
            "save_path": ""
        }
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed",
                            self.on_file_selected, "filename")
        key_entry = Gtk.Entry()
        save_path = Gtk.Entry()

        btn_extract = Gtk.Button("Extract")
        btn_extract.connect('clicked', self.on_button_submit, {
            "key_entry": key_entry,
            "save_path": save_path
        })

        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("Save File Path"), 0, 2, 1, 1)
        grid.attach(save_path, 1, 2, 3, 1)
        grid.attach(btn_extract, 0, 3, 4, 1)

        return grid
