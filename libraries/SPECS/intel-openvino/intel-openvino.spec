Name:           intel-openvino
Version:        2025.2.0
Release:        1%{?dist}
Summary:        Intel® Distribution of OpenVINO™ Toolkit

License:        Apache-2.0
URL:            https://www.intel.com/openvino
Source0:        https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/linux/openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz

%description
The Intel® Distribution of OpenVINO™ toolkit is a comprehensive toolkit for quickly developing applications and solutions that emulate human vision. It enables deep learning inference and easy heterogeneous execution across multiple Intel® platforms.

%prep
%setup -q

%build
# No build steps required, prebuilt binaries

%install
mkdir -p %{buildroot}/opt/intel/openvino_2025.2.0
cp -a * %{buildroot}/opt/intel/openvino_2025.2.0/

%post
cd /opt/intel/openvino_2025.2.0/
python3 -m pip install -r ./python/requirements.txt
cd /opt/intel
ln -sf openvino_2025.2.0 openvino_2025

%files
/opt/intel/openvino_2025.2.0

%changelog
* Thu Jun 13 2024 OpenVINO Maintainer <openvino@intel.com> - 2025.2.0-1
- Initial package for Intel OpenVINO 2025.2.0
