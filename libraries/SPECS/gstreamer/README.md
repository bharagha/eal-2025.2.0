# Intel GStreamer Package

This package provides GStreamer with Intel VAAPI plugins and optimizations for Intel DL Streamer.

## Package Information

- **Name**: intel-gstreamer
- **Version**: 1.26.1
- **Installation Path**: `/opt/intel/gstreamer/`
- **License**: LGPL-2.0+

## Features

- Intel VAAPI hardware acceleration plugins
- Intel Media SDK integration
- Optimized for Intel GPUs and Quick Sync Video
- FFmpeg integration with hardware acceleration
- Custom plugins for AI inference

## Build Dependencies

- meson ninja-build
- gcc gcc-c++
- python3 python3-pip
- glib2-devel gobject-introspection-devel
- libva-devel intel-media-driver
- intel-ffmpeg-devel
- flex bison

## Runtime Dependencies

- glib2 gobject-introspection
- libva intel-media-driver
- intel-ffmpeg

## VAAPI Plugins Included

- **vaapidecode**: Hardware video decoding
- **vaapipostproc**: Hardware video post-processing
- **vaapih264enc**: H.264 hardware encoding
- **vaapih265enc**: H.265 hardware encoding
- **vaapisink**: Hardware-accelerated video sink

## Example Pipelines

### Hardware-Accelerated Video Decode
```bash
gst-launch-1.0 filesrc location=input.mp4 ! \
  qtdemux ! h264parse ! vaapidecode ! \
  vaapipostproc ! autovideosink
```

### Hardware-Accelerated Transcoding
```bash
gst-launch-1.0 filesrc location=input.mp4 ! \
  qtdemux ! h264parse ! vaapidecode ! \
  vaapipostproc ! vaapih265enc ! \
  h265parse ! mp4mux ! filesink location=output.mp4
```

### AI Inference Pipeline
```bash
gst-launch-1.0 filesrc location=video.mp4 ! \
  qtdemux ! h264parse ! vaapidecode ! \
  gvadetect model=person-detection.xml ! \
  gvaclassify model=age-gender.xml ! \
  gvawatermark ! vaapipostproc ! autovideosink
```

## Building

```bash
cd SPECS/intel-gstreamer
rpmbuild -ba intel-gstreamer.spec
```

## Installation

```bash
sudo rpm -ivh intel-gstreamer-*.rpm
```

## Files Installed

```
/opt/intel/gstreamer/
├── bin/
│   ├── gst-launch-1.0
│   ├── gst-inspect-1.0
│   ├── gst-discoverer-1.0
│   └── gst-play-1.0
├── lib64/
│   ├── libgstreamer-1.0.so*
│   ├── libgstbase-1.0.so*
│   ├── libgstvideo-1.0.so*
│   ├── gstreamer-1.0/
│   │   ├── libgstvaapi.so
│   │   ├── libgstlibav.so
│   │   └── [other plugins]
│   └── pkgconfig/
├── include/
│   └── gstreamer-1.0/
├── share/
│   └── gstreamer-1.0/
└── libexec/
    └── gstreamer-1.0/
```

## Development Package

The `-devel` subpackage includes:
- Header files for plugin development
- pkg-config files
- GObject introspection data

## Environment Setup

To use this GStreamer build:

```bash
export GST_PLUGIN_PATH="/opt/intel/gstreamer/lib64/gstreamer-1.0:$GST_PLUGIN_PATH"
export LD_LIBRARY_PATH="/opt/intel/gstreamer/lib64:$LD_LIBRARY_PATH"
export PATH="/opt/intel/gstreamer/bin:$PATH"
```

## Plugin Debugging

Check available plugins:
```bash
gst-inspect-1.0 | grep vaapi
gst-inspect-1.0 vaapidecode
```

Debug pipeline:
```bash
GST_DEBUG=3 gst-launch-1.0 [pipeline]
```

## Integration with DL Streamer

This GStreamer build provides the media framework foundation for Intel DL Streamer, enabling:
- Hardware-accelerated video processing
- AI inference integration
- Efficient pipeline management
- Real-time streaming capabilities
