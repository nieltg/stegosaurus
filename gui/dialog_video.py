from gui.handler import encode, decode, psnr
import gi
gi.require_version('Gtk', '3.0')
from gui.progress_bar import ProgressBarDialog
from gi.repository import Gtk
from gui.utils import open_file

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

        page3 = self.get_player()
        page3.set_border_width(10)
        notebook.append_page(page3, Gtk.Label('Player'))

        page4 = self.get_psnr_box()
        page4.set_border_width(10)
        notebook.append_page(page4, Gtk.Label('PSNR'))

        notebook.connect('switch-page', self.callback_tab)

        self.show_all()

    def callback_tab(self, notebook, tab, index):
        if index == 0:
            self.data = {
                "filename": "",
                "key": "",
                "payload_path": "",
                "save_path": "",
                "frame_mode": "acak",
                "pixel_mode": "acak"
            }
            self.text_progress1.set_text("")
        elif index == 1:
            self.data = {
                "filename": "",
                "key": ""
            }
            self.text_progress2.set_text("")
        else:
            self.data = {
                "filename": ""
            }


    def on_file_selected(self, widget, name):
        self.data[name] = widget.get_filename()

    def get_hide_msg_window(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)

        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed",
                            self.on_file_selected, "filename")
        key_entry = Gtk.Entry()
        button_open_text = Gtk.FileChooserButton("Open File")
        button_open_text.set_width_chars(15)
        button_open_text.connect(
            "selection-changed", self.on_file_selected, "payload_path")
        
        save_path = Gtk.Entry()

        hbox1 = Gtk.Box()
        btn_frame_acak = Gtk.RadioButton.new_with_label_from_widget(
            None, "Frame Acak")
        btn_frame_acak.connect(
            "toggled", self.on_button_toggled, ("frame_mode", "acak"))

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
            "key_entry": key_entry,
            "save_path": save_path,
            "is_encode":True
        })

        self.text_progress1 = Gtk.Label("")

        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("Payload Path"), 0, 2, 1, 1)
        grid.attach(button_open_text, 1, 2, 3, 1)
        grid.attach(Gtk.Label("Save File Path"), 0, 3, 1, 1)
        grid.attach(save_path, 1, 3, 3, 1)
        grid.attach(hbox1, 0, 4, 4, 1)
        grid.attach(hbox2, 0, 5, 4, 1)
        grid.attach(btn_encrypt_and_hide, 0, 6, 4, 1)
        grid.attach(self.text_progress1, 0, 7, 4, 1)

        return grid
    
    def get_extract_msg_window(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed",
                            self.on_file_selected, "filename")
        key_entry = Gtk.Entry()

        btn_extract = Gtk.Button("Extract")
        btn_extract.connect('clicked', self.on_button_submit, {
            "key_entry": key_entry,
            "is_encode": False
        })
        self.text_progress2 = Gtk.Label("")
        self.button_save = Gtk.Button("Save")
        self.button_save.set_sensitive(False)
        self.filename_save = Gtk.Entry()
        self.filename_save.set_sensitive(False)

        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(btn_extract, 0, 2, 4, 1)
        grid.attach(self.text_progress2, 0, 3, 4, 1)
        grid.attach(self.button_save, 0, 4, 1, 1)
        grid.attach(self.filename_save, 1, 4, 3, 1)

        return grid
    
    def get_player(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed",
                            self.on_file_selected, "filename")
        btn_play = Gtk.Button("Play")
        btn_play.connect('clicked', self.on_button_play)

        grid.attach(Gtk.Label("Choose Video"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(btn_play, 0, 1, 4, 1)

        return grid

    def get_psnr_box(self):
        grid = Gtk.Grid(column_homogeneous=True)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        button_open = Gtk.FileChooserButton("Open Original File")
        button_open.set_width_chars(15)
        button_open.connect("selection-changed",
                            self.on_file_selected, "data1")
        button_open2 = Gtk.FileChooserButton("Open Edited File")
        button_open2.set_width_chars(15)
        button_open2.connect("selection-changed",
                             self.on_file_selected, "data2")

        btn_psnr = Gtk.Button("Calculate PSNR!")
        btn_psnr.connect('clicked', self.on_button_psnr)

        self.psnr_label = Gtk.Entry()
        self.psnr_label.set_sensitive(False)

        grid.attach(Gtk.Label("Choose Original File"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Choose Edited File"), 0, 1, 1, 1)
        grid.attach(button_open2, 1, 1, 3, 1)
        grid.attach(btn_psnr, 0, 2, 4, 1)
        grid.attach(self.psnr_label, 0, 3, 4, 1)

        return grid

    def on_button_psnr(self, button):
        self.psnr_label.set_text(
            str(psnr('video', self.data['data1'], self.data['data2'])))

    def on_button_toggled(self, button, data):
        if button.get_active():
            self.data[data[0]] = data[1]

    def on_button_submit(self, button, additional_data):
        if additional_data.get("key_entry"):
            self.data["key"] = additional_data["key_entry"].get_text()
        if additional_data.get("save_path"):
            self.data["save_path"] = additional_data["save_path"].get_text()
        print(self.data)
        if additional_data.get('is_encode'):
            encode('video', self.data)
            self.text_progress1.set_text("Complete!")
        else:
            header, payload = decode('video', self.data)
            self.text_progress2.set_text("Complete!")
            self.button_save.set_sensitive(True)
            self.filename_save.set_sensitive(True)
            self.filename_save.set_text("./" + header.payload_name)
            self.button_save.connect('clicked', self.on_button_save, {
                "payload": payload,
                "filename": self.filename_save
            })
        
    def on_button_save(self, button, data):
        with open(data['filename'].get_text(), 'wb') as f:
            f.write(data['payload'])
        self.filename_save.set_text("Save complete!")
        self.button_save.set_sensitive(False)
        self.filename_save.set_sensitive(False)
        self.destroy()

    def on_button_play(self, button):
        open_file(self.data['filename'])
