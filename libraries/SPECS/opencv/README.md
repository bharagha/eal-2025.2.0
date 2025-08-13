# Intel OpenCV Package

This package provides OpenCV with Intel optimizations and VAAPI support for Intel DL Streamer.

## Package Information

- **Name**: intel-opencv
- **Version**: 4.10.0
- **Installation Path**: `/opt/intel/opencv/`
- **License**: Apache-2.0

## Features

- Intel VAAPI hardware acceleration
- Intel TBB (Threading Building Blocks) optimization
- OpenMP parallelization
- Intel IPP (Integrated Performance Primitives) when available
- Optimized for Intel CPUs and GPUs

## Build Dependencies

- cmake ninja-build
- gcc gcc-c++
- python3-devel python3-numpy
- libjpeg-turbo-devel libpng-devel libtiff-devel
- libva-devel intel-media-driver
- tbb-devel
- openexr-devel

## Runtime Dependencies

- libjpeg-turbo libpng libtiff
- libva intel-media-driver
- tbb
- openexr

## Optimizations Included

- **VAAPI**: Hardware-accelerated video decode/encode
- **TBB**: Multi-threading optimization
- **OpenMP**: Parallel processing
- **IPP**: Intel performance primitives
- **CPU dispatching**: Runtime CPU feature detection

## Example Usage

```cpp
#include <opencv2/opencv.hpp>
#include <opencv2/core/va_intel.hpp>

// Hardware-accelerated video decoding
cv::VideoCapture cap;
cap.open("video.mp4", cv::CAP_FFMPEG, {
    cv::CAP_PROP_HW_ACCELERATION, cv::VIDEO_ACCELERATION_VAAPI,
    cv::CAP_PROP_HW_DEVICE, 0
});

cv::Mat frame;
while (cap.read(frame)) {
    // Process frame with GPU acceleration
    cv::gpu::GpuMat gpu_frame;
    gpu_frame.upload(frame);
    
    // GPU-accelerated operations
    cv::gpu::cvtColor(gpu_frame, gpu_frame, cv::COLOR_BGR2GRAY);
    
    gpu_frame.download(frame);
}
```

## Python Bindings

Python bindings are included and optimized:

```python
import cv2
import numpy as np

# Hardware-accelerated video capture
cap = cv2.VideoCapture('video.mp4')
cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_VAAPI)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Optimized image processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    cv2.imshow('Edges', edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

## Building

```bash
cd SPECS/intel-opencv
rpmbuild -ba intel-opencv.spec
```

## Installation

```bash
sudo rpm -ivh intel-opencv-*.rpm
```

## Files Installed

```
/opt/intel/opencv/
├── include/
│   └── opencv4/
│       └── opencv2/
├── lib64/
│   ├── libopencv_*.so*
│   ├── pkgconfig/
│   │   └── opencv4.pc
│   └── cmake/
│       └── opencv4/
├── share/
│   └── opencv4/
└── python3/
    └── cv2/
```

## Development Package

The `-devel` subpackage includes:
- C++ header files
- CMake configuration files
- pkg-config files
- Static libraries (if built)

## Integration with DL Streamer

This OpenCV build integrates seamlessly with Intel DL Streamer, providing:
- Hardware-accelerated computer vision operations
- Optimized deep learning inference
- Efficient memory management for video processing
