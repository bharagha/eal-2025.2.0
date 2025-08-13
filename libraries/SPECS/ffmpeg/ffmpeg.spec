%define debug_package %{nil}
Name:           ffmpeg
Version:        6.1.1
Release:        1%{?dist}
Summary:        Intel optimized FFmpeg build with VAAPI support

License:        LGPL-2.1+
Source0:        ffmpeg-%{version}.tar.gz
URL:            https://ffmpeg.org/
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  gcc gcc-c++ make yasm nasm
BuildRequires:  libva-devel libva-intel-media-driver
BuildRequires:  libX11-devel libXext-devel
#BuildRequires:  x264-devel x265-devel
#BuildRequires:  openssl-devel

Requires:       libva2 libva-intel-media-driver
#Requires:       libX11 libXext libXv
#Requires:       libvpx opus
#Requires:       x264-libs x265-libs

%description
Intel optimized FFmpeg build with VAAPI hardware acceleration support.
This version is specifically configured for use with Intel DL Streamer.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development files and headers for Intel FFmpeg.

%prep
%setup -q -n ffmpeg-%{version}

%build
./configure --prefix=/opt/intel/ffmpeg \
            --enable-pic \
            --enable-shared \
            --enable-static \
            --enable-avfilter \
            --enable-vaapi \
            --extra-cflags="-I/include" \
            --extra-ldflags="-L/lib" \
            --extra-libs=-lpthread \
            --extra-libs=-lm \
            --bindir="/bin"

make -j "$(nproc)"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
tree %{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md COPYING.LGPLv2.1
%license LICENSE.md
/opt/intel/ffmpeg
/bin/ffmpeg
/bin/ffprobe

%files devel
%defattr(-,root,root,-)
/opt/intel/ffmpeg
/bin/ffmpeg
/bin/ffprobe

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 6.1.1-1
- Initial Intel optimized FFmpeg build
