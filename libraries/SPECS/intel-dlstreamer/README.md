# Intel DL Streamer Package

This is the main Intel Deep Learning Streamer framework package that provides AI inference capabilities for video analytics.

## Package Information

- **Name**: intel-dlstreamer
- **Version**: 2025.2.0
- **Installation Path**: `/opt/intel/dlstreamer/`
- **License**: Proprietary

## Features

- GStreamer-based video analytics framework
- Hardware-accelerated AI inference on Intel CPUs and GPUs
- Pre-trained AI models for common computer vision tasks
- Python and C++ APIs
- Real-time video processing capabilities
- Integration with Intel OpenVINO toolkit

## Dependencies

This package depends on the other Intel packages:
- intel-opencv >= 4.10.0
- intel-gstreamer >= 1.26.1
- intel-ffmpeg >= 6.1.1
- intel-paho-mqtt-c >= 1.3.4
- openvino >= 2025.2.0

## Subpackages

### intel-dlstreamer-devel
Development files for building applications with DL Streamer:
- Header files
- CMake configuration files
- pkg-config files

### intel-dlstreamer-samples
Sample applications and scripts:
- Video analytics samples
- Python examples
- Pre-trained models
- Demo scripts

## Building

```bash
cd SPECS/intel-dlstreamer
rpmbuild -ba intel-dlstreamer.spec
```

## Installation

```bash
# Install main package (will install dependencies)
sudo rpm -ivh intel-dlstreamer-*.rpm

# Optional: Install development files
sudo rpm -ivh intel-dlstreamer-devel-*.rpm

# Optional: Install samples
sudo rpm -ivh intel-dlstreamer-samples-*.rpm
```

## Environment Setup

After installation, setup the environment:

```bash
source /etc/profile.d/intel-dlstreamer.sh
```

Or manually:
```bash
export INTEL_DLSTREAMER_ROOT="/opt/intel/dlstreamer"
export PATH="/opt/intel/dlstreamer/bin:$PATH"
export LD_LIBRARY_PATH="/opt/intel/dlstreamer/lib64:/opt/intel/opencv/lib64:/opt/intel/gstreamer/lib64:/opt/intel/ffmpeg/lib:/opt/intel/paho-mqtt-c/lib64:$LD_LIBRARY_PATH"
export GST_PLUGIN_PATH="/opt/intel/dlstreamer/lib64/gstreamer-1.0:/opt/intel/gstreamer/lib64/gstreamer-1.0:$GST_PLUGIN_PATH"
export PYTHONPATH="/opt/intel/dlstreamer/python:$PYTHONPATH"
```

## Files Installed

```
/opt/intel/dlstreamer/
├── bin/
│   ├── gst-launch-1.0 (DL Streamer version)
│   └── [other tools]
├── lib64/
│   ├── libdlstreamer*.so*
│   ├── gstreamer-1.0/
│   │   ├── libgvadetect.so
│   │   ├── libgvaclassify.so
│   │   ├── libgvainference.so
│   │   └── [other DL Streamer plugins]
│   ├── pkgconfig/
│   └── cmake/
├── include/
│   └── dlstreamer/
├── python/
│   └── dlstreamer/
├── share/
│   ├── models/
│   └── doc/
├── samples/ (if samples package installed)
│   ├── cpp/
│   ├── python/
│   └── scripts/
└── models/ (if samples package installed)
    ├── intel/
    └── public/
```

## Example Usage

### Object Detection Pipeline
```bash
gst-launch-1.0 filesrc location=video.mp4 ! \
  qtdemux ! h264parse ! vaapidecode ! \
  gvadetect model=person-vehicle-bike-detection-crossroad-0078 ! \
  gvawatermark ! vaapipostproc ! autovideosink
```

### Python API
```python
import dlstreamer

# Create pipeline
pipeline = dlstreamer.Pipeline()

# Add elements
pipeline.add_source("filesrc", location="video.mp4")
pipeline.add_decode()
pipeline.add_inference("person-detection")
pipeline.add_sink("display")

# Run pipeline
pipeline.run()
```

### Face Detection and Analytics
```bash
gst-launch-1.0 v4l2src device=/dev/video0 ! \
  videoconvert ! vaapih264enc ! h264parse ! vaapidecode ! \
  gvadetect model=face-detection-adas-0001 ! \
  gvaclassify model=age-gender-recognition-retail-0013 ! \
  gvawatermark ! vaapipostproc ! autovideosink
```

## Available Models

The framework supports various pre-trained models:
- Object detection (person, vehicle, face, etc.)
- Classification (age, gender, emotion, etc.)
- Semantic segmentation
- Instance segmentation
- Custom models via OpenVINO

## Development

### C++ Development
```cpp
#include <dlstreamer/gst/context.h>
#include <dlstreamer/base/inference.h>

// Create inference context
auto context = dlstreamer::ContextPtr(new dlstreamer::GSTContext());

// Load model
auto inference = dlstreamer::create_inference_backend(context);
inference->load_model("path/to/model.xml");
```

### Python Development
```python
import dlstreamer

# Create inference backend
backend = dlstreamer.InferenceBackend("OpenVINO")
backend.load_model("path/to/model.xml")

# Process frame
result = backend.infer(frame)
```

## Troubleshooting

### Check Installation
```bash
gst-inspect-1.0 gvadetect
gst-inspect-1.0 gvaclassify
```

### Debug Pipeline
```bash
GST_DEBUG=3 gst-launch-1.0 [your-pipeline]
```

### Check Hardware Acceleration
```bash
vainfo  # Check VAAPI support
ls /dev/dri/  # Check GPU devices
```

## Documentation

- Online documentation: [Intel DL Streamer Documentation]
- API reference: `/opt/intel/dlstreamer/share/doc/`
- Samples: `/opt/intel/dlstreamer/samples/`
