# Intel FFmpeg Package

This package provides FFmpeg with Intel VAAPI hardware acceleration optimizations for Intel DL Streamer.

## Package Information

- **Name**: intel-ffmpeg
- **Version**: 6.1.1
- **Installation Path**: `/opt/intel/ffmpeg/`
- **License**: LGPL-2.1+

## Features

- Intel VAAPI hardware acceleration
- VP8/VP9 encoding and decoding
- H.264/H.265 hardware encoding
- Opus audio codec support
- x264 and x265 software encoders

## Build Dependencies

- gcc gcc-c++
- make
- yasm nasm
- libva-devel
- intel-media-driver
- libX11-devel libXext-devel libXv-devel
- libvpx-devel opus-devel
- x264-devel x265-devel
- openssl-devel

## Runtime Dependencies

- libva intel-media-driver
- libX11 libXext libXv
- libvpx opus
- x264-libs x265-libs

## Hardware Acceleration

This build includes optimizations for:
- Intel Quick Sync Video (QSV)
- Intel Media SDK integration
- VAAPI surface sharing

## Example Usage

```bash
# Hardware-accelerated H.264 encoding
/opt/intel/ffmpeg/bin/ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 \
  -i input.mp4 -c:v h264_vaapi output.mp4

# Hardware-accelerated scaling
/opt/intel/ffmpeg/bin/ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 \
  -i input.mp4 -vf 'scale_vaapi=1920:1080' -c:v h264_vaapi output.mp4
```

## Building

```bash
cd SPECS/intel-ffmpeg
rpmbuild -ba intel-ffmpeg.spec
```

## Installation

```bash
sudo rpm -ivh intel-ffmpeg-*.rpm
```

## Files Installed

```
/opt/intel/ffmpeg/
├── bin/
│   ├── ffmpeg
│   ├── ffprobe
│   └── ffplay
├── lib/
│   ├── libavcodec.so*
│   ├── libavformat.so*
│   ├── libavutil.so*
│   ├── libavfilter.so*
│   ├── libavdevice.so*
│   ├── libswscale.so*
│   ├── libswresample.so*
│   └── pkgconfig/
└── share/
    └── ffmpeg/
```

## Development Package

The `-devel` subpackage includes:
- Header files
- Static libraries
- pkg-config files for all libraries

## Integration with DL Streamer

This FFmpeg build is specifically configured to work with Intel DL Streamer's GStreamer pipelines, providing hardware-accelerated video processing capabilities.
