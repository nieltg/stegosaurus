#include <gst/gst.h>

gboolean stegosaurus_plugin_init (GstPlugin* p);

// Needed by GST_PLUGIN_DEFINE.
#ifndef PACKAGE
#define PACKAGE "stegosaurus"
#endif

GST_PLUGIN_DEFINE (
  GST_VERSION_MAJOR,
  GST_VERSION_MINOR,
  stegosaurus,
  "Steganography-related plugin",
  stegosaurus_plugin_init,
  "0.1",
  "LGPL",
  "Stegosaurus",
  "https://github.com/nieltg/stegosaurus"
)
