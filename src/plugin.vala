namespace Stegosaurus {
  public static bool plugin_init(Gst.Plugin p) {
    Gst.Element.register(
      p, "vigenere", Gst.Rank.NONE, typeof(Stegosaurus.Vigenere));
    Gst.Element.register(
      p, "stegosaurusvideoenc", Gst.Rank.NONE, typeof(Stegosaurus.VideoEncrypt));
      Gst.Element.register(
        p, "expandlsb", Gst.Rank.NONE, typeof(Stegosaurus.ExpandLSB));

    return true;
  }
}
