Name:           gstreamer
Version:        1.26.1
Release:        1%{?dist}
Summary:        Intel optimized GStreamer build with VAAPI support

License:        LGPL-2.0+
Source0:        gstreamer-%{version}.tar.gz
URL:            https://gstreamer.freedesktop.org/
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  meson ninja-build gcc gcc-c++
BuildRequires:  python3 python3-pip
#BuildRequires:  glib2-devel gobject-introspection-devel
BuildRequires:  libva-devel libva-intel-media-driver
#BuildRequires:  ffmpeg-devel >= 6.1.1
BuildRequires:  pkgconfig flex bison

Requires:       glib2 gobject-introspection
Requires:       libva libva-intel-media-driver
Requires:       ffmpeg >= 6.1.1

%description
Intel optimized GStreamer build with VAAPI hardware acceleration support.
This version is specifically configured for use with Intel DL Streamer.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel

%description devel
Development files and headers for Intel GStreamer.

%prep
%setup -q -n gstreamer-%{version}

%build
# Add FFmpeg to PKG_CONFIG_PATH
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/lib/pkgconfig:/opt/intel/ffmpeg/lib/pkgconfig:${PKG_CONFIG_PATH}"
export LD_LIBRARY_PATH="/opt/intel/ffmpeg/lib:${LD_LIBRARY_PATH}"

meson setup -Dexamples=disabled \
            -Dtests=disabled \
            -Dvaapi=enabled \
            -Dgst-examples=disabled \
            --buildtype=release \
            --prefix=/opt/intel/dlstreamer/gstreamer \
            --libdir=lib/ \
            --libexecdir=bin/ \
            build/

ninja -C build

%install
rm -rf %{buildroot}
env PATH=~/python3venv/bin:$PATH DESTDIR=%{buildroot} meson install -C build/


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license COPYING
/opt/intel/dlstreamer/gstreamer/bin/
/opt/intel/dlstreamer/gstreamer/lib64/*.so.*
/opt/intel/dlstreamer/gstreamer/lib64/gstreamer-1.0/
/opt/intel/dlstreamer/gstreamer/share/
/opt/intel/dlstreamer/gstreamer/libexec/
/usr/lib64/pkgconfig/gstreamer*.pc

%files devel
%defattr(-,root,root,-)
/opt/intel/dlstreamer/gstreamer/include/
/opt/intel/dlstreamer/gstreamer/lib64/*.so
/opt/intel/dlstreamer/gstreamer/lib64/pkgconfig/

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 1.26.1-1
- Initial Intel optimized GStreamer build
