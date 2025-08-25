Name:           intel-dlstreamer
Version:        2025.2.0
Release:        1%{?dist}
Summary:        Intel Deep Learning Streamer framework

License:        Proprietary
Source0:        %{name}-%{version}.tar.gz
URL:            https://github.com/open-edge-platform/edge-ai-libraries/tree/release-1.2.0/libraries/dl-streamer
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

# Build dependencies
BuildRequires:  cmake gcc gcc-c++ make
BuildRequires:  libva-devel libva-intel-media-driver
BuildRequires:  python3-devel python3-pip
BuildRequires:  pkgconfig patchelf

# Runtime dependencies
Requires:       opencv >= 4.10.0
Requires:       gstreamer >= 1.26.1
Requires:       ffmpeg >= 6.1.1
Requires:       paho-mqtt-c >= 1.3.4
Requires:       openvino >= 2025.2.0
Requires:       libva intel-media-driver
Requires:       python3 python3-pip python3-gobject
Requires:       glib2

# System libraries still needed
Requires:       libjpeg-turbo libpng libdrm
Requires:       wayland-devel libX11 libXext
Requires:       mesa-libGL mesa-libGLU
Requires:       libgudev cairo cairo-gobject
Requires:       gobject-introspection
Requires:       libvpx opus libsrtp libXv
Requires:       libva-utils libogg libusb1
Requires:       x265-libs x264-libs
Requires:       openexr tbb

%description
Intel Deep Learning Streamer (DL Streamer) is a streaming media analytics 
framework based on GStreamer for creating complex media analytics pipelines 
optimized for Intel hardware including Intel CPUs, Intel integrated GPUs, 
and Intel discrete GPUs.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description devel
Development files and headers for Intel DL Streamer.

%package samples
Summary:        Sample applications and scripts for %{name}
Requires:       %{name} = %{version}-%{release}

%description samples
Sample applications, scripts, and models for Intel DL Streamer.

%prep
%setup -q -n intel-dlstreamer-%{version}

%build
cur_dir=`pwd`

# Download OpenVINO 2025.2 prebuilt binary
sudo rm -rf /opt/intel/openvino*
wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/linux/openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz
tar -xvzf openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz 
sudo mv openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64 /opt/intel/openvino_2025.2.0
cd /opt/intel/openvino_2025.2.0/
sudo -E python3 -m pip install -r ./python/requirements.txt
cd /opt/intel
sudo ln -s openvino_2025.2.0 openvino_2025

cd $cur_dir

mkdir build
cd build

# Set up PKG_CONFIG_PATH for packages
export PKG_CONFIG_PATH="/opt/intel/opencv/lib/pkgconfig:/opt/intel/dlstreamer/gstreamer/lib/pkgconfig:/opt/intel/dlstreamer/gstreamer/lib/gstreamer-1.0/pkgconfig:/opt/intel/ffmpeg/lib/pkgconfig:/opt/intel/paho-mqtt-c/lib/pkgconfig:${PKG_CONFIG_PATH}"

# Set up paths for packages
# export CMAKE_PREFIX_PATH="/opt/intel/opencv:/opt/intel/dlstreamer/gstreamer:/opt/intel/ffmpeg:/opt/intel/paho-mqtt-c"

# Configure with optimized dependencies
cmake -DCMAKE_INSTALL_PREFIX=/opt/intel/dlstreamer \
      -DCMAKE_BUILD_TYPE=Release \
      -DENABLE_PAHO_INSTALLATION=ON \
      -DENABLE_RDKAFKA_INSTALLATION=ON \
      -DENABLE_VAAPI=ON \
      -DENABLE_SAMPLES=ON \
      ..

make -j "$(nproc)"

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

# Remove RPATH for all binaries/libs
find %{buildroot} -type f \( -name "*.so*" -o -perm -111 \) | while read -r file; do
    if patchelf --print-rpath "$file" &>/dev/null; then
        rpath=$(patchelf --print-rpath "$file")
        if [ -n "$rpath" ]; then
            echo "Removing RPATH from $file"
            patchelf --remove-rpath "$file"
        fi
    fi
done

# Create environment setup script
mkdir -p %{buildroot}/etc/profile.d
cat > %{buildroot}/etc/profile.d/intel-dlstreamer.sh << 'EOF'
# Intel DL Streamer environment setup
export INTEL_DLSTREAMER_ROOT="/opt/intel/dlstreamer"
export PATH="/opt/intel/dlstreamer/bin:$PATH"
export LD_LIBRARY_PATH="/opt/intel/dlstreamer/lib64:/opt/intel/opencv/lib64:/opt/intel/gstreamer/lib64:/opt/intel/ffmpeg/lib:/opt/intel/paho-mqtt-c/lib64:$LD_LIBRARY_PATH"
export GST_PLUGIN_PATH="/opt/intel/dlstreamer/lib64/gstreamer-1.0:/opt/intel/gstreamer/lib64/gstreamer-1.0:$GST_PLUGIN_PATH"
export PKG_CONFIG_PATH="/opt/intel/dlstreamer/lib64/pkgconfig:/opt/intel/opencv/lib64/pkgconfig:/opt/intel/gstreamer/lib64/pkgconfig:/opt/intel/ffmpeg/lib/pkgconfig:/opt/intel/paho-mqtt-c/lib64/pkgconfig:$PKG_CONFIG_PATH"
export PYTHONPATH="/opt/intel/dlstreamer/python:$PYTHONPATH"
EOF

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
/opt/intel/dlstreamer/bin/
/opt/intel/dlstreamer/lib64/*.so.*
/opt/intel/dlstreamer/lib64/gstreamer-1.0/
/opt/intel/dlstreamer/python/
/opt/intel/dlstreamer/share/
/etc/profile.d/intel-dlstreamer.sh

%files devel
%defattr(-,root,root,-)
/opt/intel/dlstreamer/include/
/opt/intel/dlstreamer/lib64/*.so
/opt/intel/dlstreamer/lib64/pkgconfig/
/opt/intel/dlstreamer/lib64/cmake/

%files samples
%defattr(-,root,root,-)
/opt/intel/dlstreamer/samples/
/opt/intel/dlstreamer/models/

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 2025.2.0-1
- Split into modular package architecture
- Use Intel optimized dependencies
- Added development and samples subpackages
