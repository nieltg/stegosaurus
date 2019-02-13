namespace Stegosaurus {
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
        new Gst.Caps.simple("video/x-raw", "format", typeof(string), "RGB"));
      src_factory = new Gst.PadTemplate(
        "src",
        Gst.PadDirection.SRC,
        Gst.PadPresence.ALWAYS,
        new Gst.Caps.simple("video/x-raw", "format", typeof(string), "RGB"));

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

    public override Gst.FlowReturn transform_ip(Gst.Buffer iobuf) {
      return Gst.FlowReturn.OK;
    }
  }
}
