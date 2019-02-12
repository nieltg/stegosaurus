namespace Stegosaurus {
  public class Vigenere : Gst.Base.Transform {
    public enum Mode {
      ENCRYPT = 0,
      DECRYPT = 1
    }

    protected static Gst.PadTemplate sink_factory;
    protected static Gst.PadTemplate src_factory;

    static construct {
      set_static_metadata(
        "vigenere",
        "Filter",
        "Encode or decode using vigenere cipher algorithm",
        "nieltansah@gmail.com");

      sink_factory = new Gst.PadTemplate(
        "sink",
        Gst.PadDirection.SINK,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.empty_simple("text/x-raw")
      );
      src_factory = new Gst.PadTemplate(
        "src",
        Gst.PadDirection.SRC,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.empty_simple("text/x-raw")
      );

      add_pad_template(sink_factory);
      add_pad_template(src_factory);
    }

    construct {
      set_in_place(true);
    }

    [Description(nick = "operation mode")]
    public Mode mode { get; set; default = Mode.ENCRYPT; }

    protected string _key;

    [Description(nick = "encryption key")]
    public string key {
      get {
        return _key;
      }

      set {
        Gst.State state = this.current_state;

        if (state != Gst.State.READY && state != Gst.State.NULL) {
          warning(
            "Changing the `key' property on vigenere when pipeline has been " +
            "started is not supported");
        } else {
          _key = value;
        }
      }
    }

    public override Gst.FlowReturn transform_ip(Gst.Buffer iobuf) {
      if (_key != null && _key.length > 0) {
        Gst.MapInfo iobuf_map_info;
        iobuf.map(out iobuf_map_info, Gst.MapFlags.READ | Gst.MapFlags.WRITE);

        bool is_encrypt = mode == Mode.ENCRYPT;

        uint8* key_ptr = &_key.data[0];
        uint8* key_end_ptr = key_ptr + _key.length;
        uint8* cur_key_ptr = key_ptr + (iobuf.offset % _key.length);

        for (ssize_t i = 0; i < iobuf_map_info.size; i++) {
          uint8 key_char = *cur_key_ptr++;

          if (is_encrypt)
            iobuf_map_info.data[i] += key_char;
          else
            iobuf_map_info.data[i] -= key_char;

          if (cur_key_ptr == key_end_ptr)
            cur_key_ptr = key_ptr;
        }

        iobuf.unmap(iobuf_map_info);
      }

      return Gst.FlowReturn.OK;
    }
  }
}
