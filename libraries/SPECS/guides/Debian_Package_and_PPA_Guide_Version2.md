# Guide to Packaging a Debian Package, Hosting a Repository with reprepro, and Releasing it as a PPA

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Step 1: Prepare Your Source Code](#step-1-prepare-your-source-code)
4. [Step 2: Create Debian Packaging Files](#step-2-create-debian-packaging-files)
5. [Step 3: Build the Debian Package](#step-3-build-the-debian-package)
6. [Step 4: Test the Debian Package](#step-4-test-the-debian-package)
7. [Step 5: Host Your Own APT Repository with reprepro](#step-5-host-your-own-apt-repository-with-reprepro)
8. [Step 6: Create a PPA on Launchpad](#step-6-create-a-ppa-on-launchpad)
9. [Step 7: Upload the Package to the PPA](#step-7-upload-the-package-to-the-ppa)
10. [Step 8: Publishing and Using the Repository or PPA](#step-8-publishing-and-using-the-repository-or-ppa)
11. [References](#references)

---

## Introduction

This guide provides step-by-step instructions for packaging an application as a Debian package (`.deb`), hosting your own APT repository using `reprepro`, and releasing it as a Personal Package Archive (PPA) on Launchpad.

---

## Prerequisites

- Ubuntu/Debian-based system
- Launchpad account: [https://launchpad.net/](https://launchpad.net/)
- Installed tools:
  - `devscripts`
  - `build-essential`
  - `debhelper`
  - `gnupg`
  - `dput`
  - `lintian`
  - `dh-make`
  - `pbuilder`
  - `reprepro`
  - Web server (e.g. `nginx`, `apache2`) if self-hosting repository
- GPG key (for signing uploads)

---

## Step 1: Prepare Your Source Code

Organize your source code into a directory. Example:

```
myproject-1.0/
  ├── src/
  ├── README.md
  └── ...
```

---

## Step 2: Create Debian Packaging Files

1. Change to your project directory:
    ```bash
    cd myproject-1.0
    ```

2. Run `dh_make` to create the `debian/` directory:
    ```bash
    dh_make --createorig
    ```
   - Choose the package type (single binary, library, etc.)

3. Edit the files in the `debian/` directory:
   - `control`: Package metadata
   - `changelog`: Version history
   - `copyright`: Licensing info
   - `rules`: Build instructions
   - `install`: List files to install

---

## Step 3: Build the Debian Package

```bash
debuild -S -sa
```

- `-S`: Source package
- `-sa`: Include orig tarball

Or, to build a binary package:

```bash
debuild -b
```

---

## Step 4: Test the Debian Package

Run Lintian to check for common issues:

```bash
lintian ../myproject_1.0-1_source.changes
```

---

## Step 5: Host Your Own APT Repository with reprepro

### 5.1 Install reprepro

```bash
sudo apt-get install reprepro
```

### 5.2 Prepare the repository directory

```bash
sudo mkdir -p /srv/repo/{conf,incoming}
sudo chown -R $USER /srv/repo
```

### 5.3 Create configuration files

Create `/srv/repo/conf/distributions`:
```
Codename: focal
Suite: stable
Components: main
Architectures: amd64 source
SignWith: <YOUR-GPG-KEYID>
```

### 5.4 Import your package

```bash
cd /srv/repo
reprepro includedeb focal /path/to/myproject_1.0-1_amd64.deb
```

To include source packages:

```bash
reprepro include focal /path/to/myproject_1.0-1.dsc
```

### 5.5 Serve repository via HTTP

Configure your web server (nginx, apache) to serve `/srv/repo` at an endpoint (e.g., `http://yourdomain.com/repo`).

### 5.6 Add repository on client machines

On users' machines:

```bash
echo "deb [signed-by=/usr/share/keyrings/myrepo.gpg] http://yourdomain.com/repo focal main" | sudo tee /etc/apt/sources.list.d/myrepo.list
# Add your GPG public key to /usr/share/keyrings/myrepo.gpg
sudo apt-get update
sudo apt-get install myproject
```

---

## Step 6: Create a PPA on Launchpad

1. Log in to [https://launchpad.net/](https://launchpad.net/).
2. Click “Create a PPA” in your profile.
3. Fill in the PPA details.

---

## Step 7: Upload the Package to the PPA

1. Import your GPG key to Launchpad (if not already done).
2. Configure `dput`:
    ```ini
    [ppa]
    fqdn = ppa.launchpad.net
    method = ftp
    incoming = ~<your-launchpad-username>/ubuntu/<ppa-name>/
    login = anonymous
    ```

3. Upload your package:
    ```bash
    dput ppa ../myproject_1.0-1_source.changes
    ```

---

## Step 8: Publishing and Using the Repository or PPA

### Using Your Custom Repository

- Add your APT line to `/etc/apt/sources.list.d/myrepo.list` as above.
- Import your GPG public key if signed.

### Using the PPA

- Add your PPA on a client machine:
    ```bash
    sudo add-apt-repository ppa:<your-launchpad-username>/<ppa-name>
    sudo apt update
    sudo apt install myproject
    ```

---

## References

- [Debian New Maintainers' Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [Launchpad PPA Documentation](https://help.launchpad.net/Packaging/PPA)
- [Ubuntu Packaging Guide](https://packaging.ubuntu.com/html/)
- [reprepro Manual](https://mirrorer.alioth.debian.org/)
- [Hosting a Debian Repository with reprepro](https://wiki.debian.org/DebianRepository/SetupWithReprepro)

---

*Prepared by: [Your Name]*  
*Date: August 2025*