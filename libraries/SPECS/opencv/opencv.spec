Name:           opencv
Version:        4.10.0
Release:        1%{?dist}
Summary:        Intel optimized OpenCV build for DL Streamer

License:        Apache-2.0
Source0:        opencv-%{version}.tar.gz
URL:            https://opencv.org/
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  cmake ninja-build gcc gcc-c++ make
BuildRequires:  libva-devel libva-intel-media-driver
BuildRequires:  pkgconfig

Requires:       libjpeg-turbo libpng libtiff
Requires:       libva2 libva-intel-media-driver

%description
Intel optimized OpenCV build with VAAPI support for hardware acceleration.
This version is specifically configured for use with Intel DL Streamer.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development files and headers for Intel OpenCV.

%prep
%setup -q -n opencv-%{version}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/intel/opencv \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=OFF \
      -DBUILD_PERF_TESTS=OFF \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_opencv_apps=OFF \
      -GNinja ..
ninja -j "$(nproc)"

%install
rm -rf %{buildroot}
cd build
env PATH=~/python3venv/bin:$PATH DESTDIR=%{buildroot} ninja install
cp -r %{_builddir}/%{name}-%{version}/cmake %{buildroot}/

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

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%cmake cmake/
/opt/intel/opencv/lib64/*.so.*
/opt/intel/opencv/lib/
/opt/intel/opencv/share/
/opt/intel/opencv/bin/


%files devel
%defattr(-,root,root,-)
/opt/intel/opencv/include/
/opt/intel/opencv/lib/
/opt/intel/opencv/lib64/*.so
/opt/intel/opencv/bin/

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 4.10.0-1
- Initial Intel optimized OpenCV build
