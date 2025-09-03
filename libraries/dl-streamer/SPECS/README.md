# DL Streamer RPM generation

This guide explains how to use the provided scripts to:
- Download all required sources
- Build all RPM and SRPM packages
- Install the resulting RPMs
- Generate and sign a YUM/DNF repository for distribution

## 1. Downloading Sources

> **Note**: If any of the package versions needs to be updated,
> it needs to be done in `versions.env` file and in the respective
> package .spec files.

Navigate to the [libraries/SPECS](libraries/SPECS/) directory and run:

```sh
./download_sources.sh
```

This script will:
- Download all required third-party and DL Streamer sources
- Place them in the appropriate locations for RPM building

## 2. Building And Installing All Packages

### Prerequisite

Download OpenVINO 2025.2 prebuilt binary:

```
sudo rm -rf /opt/intel/openvino*
wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/linux/openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz
tar -xvzf openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz 
sudo mv openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64 /opt/intel/openvino_2025.2.0
cd /opt/intel/openvino_2025.2.0/
sudo -E python3 -m pip install -r ./python/requirements.txt
cd /opt/intel
sudo ln -s openvino_2025.2.0 openvino_2025
```
### Building and Installation of few DL Streamer Dependent RPM packages

> **Note**: Please uninstall intel dlstreamer package if already installed by running following command:
> ```sh
> sudo dnf remove -y intel-dlstreamer-2025.2.0-1.emt3.x86_64
> ```

After building, install the the runtime and devel DL Streamer dependent packages:

```sh
./build_and_install_packages.sh
```

This script will:
- Install build dependencies (using `dnf`)
- Set up the RPM build environment (`~/rpmbuild`)
- Build and install all packages in dependency order, producing both `.rpm` and `.src.rpm` files in `~/rpmbuild/RPMS/x86_64/` and `~/rpmbuild/SRPMS/`

### Installation of DL Streamer RPM package

```sh
sudo dnf install -y  --setopt=install_weak_deps=False ~/rpmbuild/RPMS/x86_64/intel-dlstreamer-*.rpm
# setup environment
source /opt/intel/openvino_2025/setupvars.sh
source /opt/intel/dlstreamer/setupvars.sh
```

## 4. Creating a Signed RPM Repository

### 4.1. Collect RPMs

Copy all `.rpm` and `.src.rpm` files to a directory for your repository, e.g.:

```sh
mkdir -p ~/dlstreamer-repo
cp ~/rpmbuild/RPMS/x86_64/*.rpm ~/dlstreamer-repo/
cp ~/rpmbuild/SRPMS/*.src.rpm ~/dlstreamer-repo/
```

### 4.2. Initialize the Repository

Install `createrepo` if not already present:

```sh
sudo dnf install createrepo
```

Create repository metadata:

```sh
createrepo ~/dlstreamer-repo
```

### 4.3. Signing RPMs

#### 4.3.1. Generate a GPG Key (if needed)

```sh
gpg --full-generate-key
```
- Choose RSA and a key size (e.g., 4096)
- Remember the email and passphrase

#### 4.3.2. Export the Public Key

```sh
gpg --armor --export 'Your Name or Email' > RPM-GPG-KEY-dlstreamer
```

#### 4.3.3. Configure RPM to Use Your Key

Edit `~/.rpmmacros` and add:

```
%_gpg_name Your Name or Email
```

#### 4.3.4. Sign All RPMs

```sh
rpm --addsign ~/dlstreamer-repo/*.rpm
```

You will be prompted for your GPG passphrase.

### 4.4. Sign the Repository Metadata

```sh
gpg --detach-sign --armor ~/dlstreamer-repo/repodata/repomd.xml
```

### 4.5. Distribute the Repository

- Place the contents of `~/dlstreamer-repo` on a web server or shared location.
- Make sure to include the `RPM-GPG-KEY-dlstreamer` file.

### 4.6. Using the Repository on Client Machines

1. Import the GPG key:

    ```sh
    sudo rpm --import https://your.server/path/RPM-GPG-KEY-dlstreamer
    ```

2. Create a repo file `/etc/yum.repos.d/dlstreamer.repo`:

    ```
    [dlstreamer]
    name=DL Streamer Custom Repo
    baseurl=https://your.server/path/
    enabled=1
    gpgcheck=1
    gpgkey=https://your.server/path/RPM-GPG-KEY-dlstreamer
    ```

3. Install packages:

    ```sh
    sudo dnf install intel-dlstreamer
    ```

---

## Troubleshooting

- If you encounter GPG errors, ensure your key is trusted and imported on the client.
- For build errors, check that all dependencies are installed and sources are downloaded.

---

## References

- [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)
- [createrepo Documentation](https://github.com/rpm-software-management/createrepo)
- [Fedora GPG Guide](https://docs.fedoraproject.org/en-US/quick-docs/creating-gpg-keys/)

---

For more details, see the scripts in [libraries/SPECS](libraries/SPECS/)