import gi
gi.require_version('Gtk', '3.0')
from gui.progress_bar import ProgressBarDialog
from gi.repository import Gtk
from gui.utils import open_file


class DialogAudio(Gtk.Dialog):

    def __init__(self, parent):
        self.data = {}
        Gtk.Dialog.__init__(self, "Stegosaurus Audio", parent, 0)
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
        
        notebook.connect('switch-page', self.callback_tab)
        
        self.show_all()
    
    def callback_tab(self, notebook, tab, index):
        if index == 0:
            self.data = {
                "filename": "",
                "key": "",
                "payload_path": "",
                "mode": "acak"
            }
        elif index == 0:
            self.data = {
                "filename": "",
                "key": "",
                "save_path": ""
            }
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

        hbox1 = Gtk.Box()
        btn_frame_acak = Gtk.RadioButton.new_with_label_from_widget(
            None, "Mode Acak")
        btn_frame_acak.connect(
            "toggled", self.on_button_toggled, ("mode", "acak"))

        btn_frame_seq = Gtk.RadioButton.new_from_widget(btn_frame_acak)
        btn_frame_seq.set_label("Mode Sequential")
        btn_frame_seq.connect(
            "toggled", self.on_button_toggled, ("mode", "seq"))
        hbox1.pack_start(btn_frame_acak, True, True, 10)
        hbox1.pack_start(btn_frame_seq, True, True, 10)

        btn_encrypt_and_hide = Gtk.Button("Encrypt & Hide")
        btn_encrypt_and_hide.connect("clicked", self.on_button_submit, {
            "key_entry": key_entry
        })

        grid.attach(Gtk.Label("Choose Audio"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(Gtk.Label("Key"), 0, 1, 1, 1)
        grid.attach(key_entry, 1, 1, 3, 1)
        grid.attach(Gtk.Label("Text"), 0, 2, 1, 1)
        grid.attach(button_open_text, 1, 2, 3, 1)
        grid.attach(hbox1, 0, 3, 4, 1)
        grid.attach(btn_encrypt_and_hide, 0, 5, 4, 1)

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

        grid.attach(Gtk.Label("Choose Audio"), 0, 0, 1, 1)
        grid.attach(button_open, 1, 0, 3, 1)
        grid.attach(btn_play, 0, 1, 4, 1)

        return grid

    def on_button_toggled(self, button, data):
        if button.get_active():
            self.data[data[0]] = data[1]

    def on_button_submit(self, button, additional_data):
        if additional_data.get("key_entry"):
            self.data["key"] = additional_data["key_entry"].get_text()
        if additional_data.get("save_path"):
            self.data["save_path"] = additional_data["save_path"].get_text()
        print(self.data)
        dialog = ProgressBarDialog(self)
        response = dialog.run()

        dialog.destroy()

    def on_button_play(self, button):
        open_file(self.data['filename'])

