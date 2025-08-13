# Guide to Packaging an RPM Package and Hosting a Repository with createrepo

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Step 1: Prepare Your Source Code](#step-1-prepare-your-source-code)
4. [Step 2: Install RPM Build Tools](#step-2-install-rpm-build-tools)
5. [Step 3: Create the RPM Spec File](#step-3-create-the-rpm-spec-file)
6. [Step 4: Build the RPM Package](#step-4-build-the-rpm-package)
7. [Step 5: Test the RPM Package](#step-5-test-the-rpm-package)
8. [Step 6: Set Up a Repository with createrepo](#step-6-set-up-a-repository-with-createrepo)
9. [Step 7: Distribute and Use Your Repository](#step-7-distribute-and-use-your-repository)
10. [References](#references)

---

## Introduction

This guide provides a step-by-step process to package an application as an RPM and host your own YUM/DNF repository using the `createrepo` tool.

---

## Prerequisites

- CentOS, Fedora, RHEL, or compatible RPM-based distribution
- Tools installed:
  - `rpm-build`
  - `rpmdevtools`
  - `createrepo`
  - `yum-utils` or `dnf-plugins-core`
  - `gcc`, `make`, and other build dependencies as needed
- GPG key (optional, for signing packages)

---

## Step 1: Prepare Your Source Code

Organize your project for packaging. Example:

```
myproject-1.0/
  ├── src/
  ├── README.md
  └── ...
```

Create a source tarball:

```bash
tar czvf myproject-1.0.tar.gz myproject-1.0/
```

---

## Step 2: Install RPM Build Tools

Install necessary tools:

```bash
sudo dnf install rpm-build rpmdevtools createrepo
```
or
```bash
sudo yum install rpm-build rpmdevtools createrepo
```

---

## Step 3: Create the RPM Spec File

1. Set up the RPM build environment:

    ```bash
    rpmdev-setuptree
    ```

    This creates `~/rpmbuild` with subdirectories: `SOURCES`, `SPECS`, etc.

2. Move your tarball to the SOURCES directory:

    ```bash
    mv myproject-1.0.tar.gz ~/rpmbuild/SOURCES/
    ```

3. Create a spec file template:

    ```bash
    rpmdev-newspec ~/rpmbuild/SPECS/myproject.spec
    ```

4. Edit `~/rpmbuild/SPECS/myproject.spec` to define metadata, build instructions, and install paths.

---

## Step 4: Build the RPM Package

Build the source and binary RPMs:

```bash
cd ~/rpmbuild/SPECS
rpmbuild -ba myproject.spec
```

Find the resulting `.rpm` files in `~/rpmbuild/RPMS/` and `.src.rpm` in `~/rpmbuild/SRPMS/`.

---

## Step 5: Test the RPM Package

Install and test your package locally:

```bash
sudo rpm -ivh ~/rpmbuild/RPMS/x86_64/myproject-1.0-1.el8.x86_64.rpm
```
Or upgrade if already installed:

```bash
sudo rpm -Uvh ~/rpmbuild/RPMS/x86_64/myproject-1.0-1.el8.x86_64.rpm
```

Check for missing dependencies or errors.

---

## Step 6: Set Up a Repository with createrepo

1. Create a directory to host your repository (e.g., in `/var/www/html/repo` for web access):

    ```bash
    mkdir -p ~/myrepo
    cp ~/rpmbuild/RPMS/x86_64/*.rpm ~/myrepo/
    ```

2. Initialize the repository metadata:

    ```bash
    createrepo ~/myrepo
    ```

3. (Optional) Sign your RPMs and/or the repodata for extra security.

---

## Step 7: Distribute and Use Your Repository

### 7.1 Host the Repository

- Use a web server (Apache, Nginx) to serve the `~/myrepo` directory.
  - For local testing, use:
    ```bash
    python3 -m http.server --directory ~/myrepo 8080
    ```

### 7.2 Add the Repository on Client Machines

Create a repo file `/etc/yum.repos.d/myrepo.repo` with the following contents:

```
[myrepo]
name=My Custom Repo
baseurl=http://yourserver-or-ip:8080/
enabled=1
gpgcheck=0   # set to 1 if you sign your RPMs and provide a GPG key
```

Update and install your package:

```bash
sudo dnf clean all
sudo dnf makecache
sudo dnf install myproject
```

---

## References

- [RPM Packaging Guide](https://rpm-packaging-guide.github.io/)
- [Fedora RPM Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [createrepo documentation](https://createrepo.baseurl.org/)
- [Signing RPM Packages](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/package_management/signing-packages-using-gpg_package-management)

---

*Prepared by: [Your Name]*  
*Date: August 2025*