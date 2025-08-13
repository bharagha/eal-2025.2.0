Name:           paho-mqtt-c
Version:        1.3.4
Release:        1%{?dist}
Summary:        Eclipse Paho MQTT C client library for Intel DL Streamer

License:        EPL-2.0 OR BSD-3-Clause
Source0:        paho.mqtt.c-%{version}.tar.gz
URL:            https://github.com/eclipse/paho.mqtt.c
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  cmake gcc gcc-c++ make
BuildRequires:  openssl-devel

%description
Eclipse Paho MQTT C client library configured for Intel DL Streamer.
Provides MQTT connectivity for edge AI applications.

%prep
%setup -q -n paho.mqtt.c-%{version}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/intel/paho-mqtt-c \
      -DCMAKE_BUILD_TYPE=Release \
      ..
make -j "$(nproc)"

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}
tree %{buildroot}
echo "install done..."

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
/opt/intel/paho-mqtt-c

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 1.3.4-1
- Initial Intel optimized Paho MQTT C build
