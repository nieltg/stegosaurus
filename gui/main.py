import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DialogVideo(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Stegosaurus Video", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        # self.set_default_size(150, 100)
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

    def on_file_selected(self, widget):
        filename = widget.get_filename()
        print("File Choosen: ", filename)

    def get_hide_msg_window(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed", self.on_file_selected)
        key_entry = Gtk.Entry()
        button_open_text = Gtk.FileChooserButton("Open File")
        button_open_text.set_width_chars(15)
        button_open_text.connect("selection-changed", self.on_file_selected)

        hbox1 = Gtk.Box()
        btn_frame_acak = Gtk.RadioButton.new_with_label_from_widget(None, "Frame Acak")
        btn_frame_acak.connect(
            "toggled", self.on_button_toggled, "btn_frame_acak")

        btn_frame_seq = Gtk.RadioButton.new_from_widget(btn_frame_acak)
        btn_frame_seq.set_label("Frame Sequential")
        btn_frame_seq.connect(
            "toggled", self.on_button_toggled, "btn_frame_seq")
        hbox1.pack_start(btn_frame_acak, True, True, 10)
        hbox1.pack_start(btn_frame_seq, True, True, 10)

        hbox2 = Gtk.Box()
        btn_pixel_acak = Gtk.RadioButton.new_with_label_from_widget(
            None, "Pixel Acak")
        btn_pixel_acak.connect(
            "toggled", self.on_button_toggled, "btn_pixel_acak")

        btn_pixel_seq = Gtk.RadioButton.new_from_widget(btn_pixel_acak)
        btn_pixel_seq.set_label("Pixel Sequential")
        btn_pixel_seq.connect(
            "toggled", self.on_button_toggled, "btn_pixel_seq")
        hbox2.pack_start(btn_pixel_acak, True, True, 10)
        hbox2.pack_start(btn_pixel_seq, True, True, 10)
        
        btn_encrypt_and_hide = Gtk.Button("Encrypt & Hide")


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

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

    def get_extract_msg_window(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed", self.on_file_selected)
        key_entry = Gtk.Entry()
        path_entry = Gtk.Entry()

        btn_extract = Gtk.Button("Extract")

        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("Save File Path"), 0, 2, 1, 1)
        grid.attach(path_entry, 1, 2, 3, 1)
        grid.attach(btn_extract, 0, 3, 4, 1)

        return grid


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Stegosaurus")
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        label = Gtk.Label()
        label.set_markup("<big><b>Stegosaurus</b></big>")
        label.set_justify(Gtk.Justification.CENTER)
        label_sub = Gtk.Label("Steganography for video and audio")
        separator = Gtk.HSeparator()
        button_video = Gtk.Button(label="Video")
        button_video.connect("clicked", self.on_button_clicked)
        button_audio = Gtk.Button(label="Audio")
        button_audio.connect("clicked", self.on_button_clicked)

        grid.attach(label, 0, 0, 2, 2)
        grid.attach(label_sub, 0, 2, 2, 1)
        grid.attach(separator, 0, 3, 2, 1)
        grid.attach(button_audio, 1, 4, 1, 1)
        grid.attach(button_video, 0, 4, 1, 1)

    def on_button_clicked(self, widget):
        dialog = DialogVideo(self)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
