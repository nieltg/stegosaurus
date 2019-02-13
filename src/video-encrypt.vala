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

    public override bool start() {
      return payload_pad.activate_mode(Gst.PadMode.PULL, true);
    }

    protected Gst.Video.Info in_info;
    protected Gst.Video.Info out_info;

    public override bool set_caps(Gst.Caps incaps, Gst.Caps outcaps) {
      Gst.Video.Info in_info, out_info;

      in_info = new Gst.Video.Info();
      out_info = new Gst.Video.Info();

      if (in_info.from_caps(incaps) && out_info.from_caps(outcaps)) {
        this.in_info = in_info;
        this.out_info = out_info;

        return true;
      } else {
        return false;
      }
    }

    public override Gst.FlowReturn transform_ip(Gst.Buffer iobuf) {
      return Gst.FlowReturn.OK;
    }
  }
}
