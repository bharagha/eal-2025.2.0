# DL Streamer RPM generation

This guide explains how to use the provided scripts to:
- Download all required sources
- Build all RPM and SRPM packages
- Install the resulting RPMs
- Generate and sign a YUM/DNF repository for distribution

## 1. Downloading Sources

Navigate to the [libraries/SPECS](libraries/SPECS/) directory and run:

```sh
./download_sources.sh
```

This script will:
- Download all required third-party and DL Streamer sources
- Place them in the appropriate locations for RPM building

## 2. Building And Installing All Packages


This script will:
- Install build dependencies (using `dnf`)
- Set up the RPM build environment (`~/rpmbuild`)
- Build all packages in dependency order, producing both `.rpm` and `.src.rpm` files in `~/rpmbuild/RPMS/x86_64/` and `~/rpmbuild/SRPMS/`

**Note:**  
To see all script options, run:
```sh
./build_an_install_packages.sh --help
```

After building, install the the runtime and devel DL Streamer dependent packages:

```sh
./build_an_install_packages.sh
```

Install the the Intel DL Streamer runtime package:

```sh
./build_an_install_packages.sh --install-dlstreamer
```

To set up the environment:

```sh
source /etc/profile.d/intel-dlstreamer.sh
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