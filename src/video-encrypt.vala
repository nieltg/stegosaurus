namespace Stegosaurus {
  const string[] bit_rep = {
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101", "1110", "1111",
  };

  public class VideoEncrypt : Gst.Base.Transform {
    protected static Gst.PadTemplate payload_factory;
    protected static Gst.PadTemplate sink_factory;
    protected static Gst.PadTemplate src_factory;

    static construct {
      set_static_metadata(
        "stegosaurusvideoenc",
        "Filter",
        "Put the specified payload in the video stream",
        "nieltansah@gmail.com");

      payload_factory = new Gst.PadTemplate(
        "payload",
        Gst.PadDirection.SINK,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.empty_simple("text/x-raw"));
      sink_factory = new Gst.PadTemplate(
        "sink",
        Gst.PadDirection.SINK,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.empty_simple("video/x-raw"));
      src_factory = new Gst.PadTemplate(
        "src",
        Gst.PadDirection.SRC,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.empty_simple("video/x-raw"));

      add_pad_template(payload_factory);
      add_pad_template(sink_factory);
      add_pad_template(src_factory);
    }

    protected Gst.Pad payload_pad;

    construct {
      set_in_place(true);

      Gst.PadTemplate pad_template = get_pad_template("payload");
      payload_pad = new Gst.Pad.from_template(pad_template, "payload");
      add_pad(payload_pad);
    }

    public override bool start() {
      return payload_pad.activate_mode(Gst.PadMode.PULL, true);
    }

    protected Gst.Video.Info in_info = new Gst.Video.Info();

    public override bool set_caps(Gst.Caps incaps, Gst.Caps outcaps) {
      return in_info.from_caps(incaps);
    }

    protected uint8 generate_payload_bitmask(uint8 n_bits) {
      uint8 mask = 0;

      for (uint8 i = 0; i < n_bits; i++)
        mask |= 1 << i;
      return mask;
    }

    protected uint8 _n_bits = 1;
    protected uint8 _n_bits_mask = 0x1;

    public uint8 n_bits {
      get { return _n_bits; }
      set {
        _n_bits = value;
        _n_bits_mask = generate_payload_bitmask(value);
      }
    }

    public override Gst.FlowReturn transform_ip(Gst.Buffer iobuf) {
      var current_frame_num = iobuf.offset;
      var capacity_of_frame = in_info.size * _n_bits;

      var bit_offset = current_frame_num * capacity_of_frame;

      var bit_offset_div = bit_offset / 8;
      uint8 bit_offset_mod = (uint8) (bit_offset % 8);

      var bit_offset_end = bit_offset + capacity_of_frame;

      var bit_offset_end_div = bit_offset_end / 8;
      uint8 bit_offset_end_mod = (uint8) (bit_offset_end % 8);

      var buffer_offset = bit_offset_div;
      var buffer_size = bit_offset_end_div - buffer_offset + (bit_offset_end_mod > 0 ? 1 : 0);

      Gst.Buffer payload_buffer;
      if (payload_pad.pull_range(buffer_offset, (uint) buffer_size, out payload_buffer) != Gst.FlowReturn.OK) {
        return Gst.FlowReturn.OK;
      }

      Gst.MapInfo payload_map_info;
      payload_buffer.map(out payload_map_info, Gst.MapFlags.READ);

      Gst.MapInfo iobuf_map_info;
      iobuf.map(out iobuf_map_info, Gst.MapFlags.READ | Gst.MapFlags.WRITE);

      for (int i = 0; i < in_info.size; i++) {
        var pixel_bit_offset = bit_offset_mod + i * _n_bits;

        var pixel_bit_offset_div = pixel_bit_offset / 8;
        uint8 pixel_bit_offset_mod = (uint8) (pixel_bit_offset % 8);

        if (pixel_bit_offset_div < payload_map_info.size) {
          uint8 payload_byte = payload_map_info.data[pixel_bit_offset_div];

          uint8 payload_bits = payload_byte >> (8 - _n_bits - pixel_bit_offset_mod);

          debug(@"nbmask = $(bit_rep[payload_bits >> 4])$(bit_rep[payload_bits & 0x0F])");

          iobuf_map_info.data[i] &= ~_n_bits_mask;
          iobuf_map_info.data[i] |= payload_bits;
        }
      }

      payload_buffer.unmap(payload_map_info);

      iobuf.unmap(iobuf_map_info);

      return Gst.FlowReturn.OK;
    }
  }
}
