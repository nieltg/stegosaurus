namespace Stegosaurus {
  public class Vigenere : Gst.Base.Transform {
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

      // Process.

      iobuf.unmap(iobuf_map_info);

      return Gst.FlowReturn.OK;
    }
  }
}
