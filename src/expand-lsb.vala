namespace Stegosaurus {
  public class ExpandLSB : Gst.Base.Transform {
    protected static Gst.PadTemplate sink_factory;
    protected static Gst.PadTemplate src_factory;

    static construct {
      set_static_metadata(
        "expandlsb",
        "Filter",
        "Expand least-significant-bit in video",
        "nieltansah@gmail.com");

      sink_factory = new Gst.PadTemplate(
        "sink",
        Gst.PadDirection.SINK,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.any()
      );
      src_factory = new Gst.PadTemplate(
        "src",
        Gst.PadDirection.SRC,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.any()
      );

      add_pad_template(sink_factory);
      add_pad_template(src_factory);
    }

    construct {
      set_in_place(true);
    }

    public override Gst.FlowReturn transform_ip(Gst.Buffer iobuf) {
      Gst.MapInfo iobuf_map_info;
      iobuf.map(out iobuf_map_info, Gst.MapFlags.READ | Gst.MapFlags.WRITE);

      for (int i = 0; i < iobuf_map_info.size; i++) {
        iobuf_map_info.data[i] = (iobuf_map_info.data[i] & 1) == 0 ? 0xff : 0;
      }

      iobuf.unmap(iobuf_map_info);

      return Gst.FlowReturn.OK;
    }
  }
}
