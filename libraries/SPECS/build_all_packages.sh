#!/bin/bash
# Intel DL Streamer Modular Build Script
set -ex


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Source versions
if [[ -f "$SCRIPT_DIR/versions.env" ]]; then
    source "$SCRIPT_DIR/versions.env"
else
    echo "[ERROR] versions.env not found in $SCRIPT_DIR" >&2
    exit 1
fi

# Define packages with their directory and spec file names
declare -A PACKAGES=(
     ["paho-mqtt-c"]="paho-mqtt-c/paho-mqtt-c.spec"
     ["ffmpeg"]="ffmpeg/ffmpeg.spec"
     ["opencv"]="opencv/opencv.spec"
     ["gstreamer"]="gstreamer/gstreamer.spec"
     ["intel-dlstreamer"]="intel-dlstreamer/intel-dlstreamer.spec"
)

# Build order (dependencies first)
BUILD_ORDER=(
    "paho-mqtt-c"
    "ffmpeg"
    "gstreamer"
    "opencv"
    "intel-dlstreamer"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_sources() {
    log_info "Checking source files..."
    
    sources=(
        "paho.mqtt.c-${PAHO_MQTT_VERSION}.tar.gz"
        "ffmpeg-${FFMPEG_VERSION}.tar.gz"
        "gstreamer-${GSTREAMER_VERSION}.tar.gz"
        "opencv-${OPENCV_VERSION}.tar.gz"
        "intel-dlstreamer-${DLSTREAMER_VERSION}.tar.gz"
    )
    
    missing_sources=()
    for source in "${sources[@]}"; do
        if [[ ! -f "$source" ]]; then
            missing_sources+=("$source")
        fi
    done
    
    if [[ ${#missing_sources[@]} -gt 0 ]]; then
        log_error "Missing source files:"
        for source in "${missing_sources[@]}"; do
            echo "  - $source"
        done
        log_info "Download sources manually or run: ./download_sources.sh"
        exit 1
    fi
    
    log_info "All source files found ✓"
}

build_package() {
    local package_name="$1"
    local spec_file="$SCRIPT_DIR/${PACKAGES[$package_name]}"
    
    log_info "Building package: $package_name"
    
    # Check if spec file exists
    if [[ ! -f "$spec_file" ]]; then
        log_error "Spec file not found: $spec_file"
        exit 1
    fi
    
    # Create build directories
    mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
    
    # Copy spec file
    cp "$spec_file" ~/rpmbuild/SPECS/
    
    # Copy source files based on package
    case "$package_name" in
        "paho-mqtt-c")
            cp paho.mqtt.c-${PAHO_MQTT_VERSION}.tar.gz ~/rpmbuild/SOURCES/
            ;;
        "ffmpeg")
            cp ffmpeg-${FFMPEG_VERSION}.tar.gz ~/rpmbuild/SOURCES/
            ;;
        "opencv")
            cp opencv-${OPENCV_VERSION}.tar.gz ~/rpmbuild/SOURCES/
            ;;
        "gstreamer")
            cp gstreamer-${GSTREAMER_VERSION}.tar.gz ~/rpmbuild/SOURCES/
            ;;
        "intel-dlstreamer")
            cp intel-dlstreamer-${DLSTREAMER_VERSION}.tar.gz ~/rpmbuild/SOURCES/
            ;;
    esac
    
    # Build the package
    local spec_basename=$(basename "$spec_file")
    if rpmbuild -ba ~/rpmbuild/SPECS/$spec_basename; then
        log_info "Successfully built $package_name ✓"
        
        # Install the package for dependencies (skip the main dlstreamer package)
        if [[ "$package_name" != "intel-dlstreamer" ]]; then
            log_info "Installing $package_name for dependency resolution..."
            
            # Get the actual package name from the spec file
            local actual_package_name=$(grep "^Name:" "$spec_file" | awk '{print $2}')
            rpm -Uvh ~/rpmbuild/RPMS/x86_64/${actual_package_name}-*.rpm
        fi
    else
        log_error "Failed to build $package_name ✗"
        exit 1
    fi
}

install_build_deps() {
    log_info "Installing build dependencies..."
    
    deps=(
        "rpm-build" "rpmdevtools" "cmake" "ninja-build"
        "gcc" "gcc-c++" "make" "git" "python3" "python3-pip"
        "yasm" "nasm" "meson" "pkgconfig" "openssl-devel"
        "patchelf" "flex" "bison"
    )
    
    if command -v dnf &> /dev/null; then
        sudo dnf install -y "${deps[@]}"
    else
        log_error "Neither dnf nor yum found. Please install build dependencies manually."
        exit 1
    fi
}

main() {
    log_info "Intel DL Streamer Modular Build Started"
    log_info "========================================"
    
    
    # Validate all spec files exist
    local missing_specs=()
    for package in "${BUILD_ORDER[@]}"; do
        local spec_file="${PACKAGES[$package]}"
        if [[ ! -f "$spec_file" ]]; then
            missing_specs+=("$spec_file")
        fi
    done
    
    if [[ ${#missing_specs[@]} -gt 0 ]]; then
        log_error "Missing spec files:"
        for spec in "${missing_specs[@]}"; do
            echo "  - $spec"
        done
        exit 1
    fi
    
    # Install build dependencies
    install_build_deps
    
    # Check source files
    check_sources
    
    # Initialize RPM build environment
    rpmdev-setuptree
    
    # Build packages in dependency order
    for package in "${BUILD_ORDER[@]}"; do
        build_package "$package"
    done
    
    log_info "========================================"
    log_info "All packages built successfully! ✓"
    log_info "RPM packages are in ~/rpmbuild/RPMS/x86_64/"
    log_info ""
    log_info "To install Intel DL Streamer:"
    log_info "sudo rpm -Uvh ~/rpmbuild/RPMS/x86_64/intel-dlstreamer-*.rpm"
    log_info ""
    log_info "To setup environment:"
    log_info "source /etc/profile.d/intel-dlstreamer.sh"
}

# Handle command line arguments

case "${1:-}" in
    --help|-h)
        echo "Intel DL Streamer Modular Build Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h                Show this help message"
        echo "  --check-deps              Only check and install build dependencies"
        echo "  --check-sources           Only check if source files are present"
        echo "  --dlstreamer-deps-only    Build only DL Streamer dependencies (no intel-dlstreamer)"
        echo "  --install-deps            Install built dependency RPMs in BUILD_ORDER (no intel-dlstreamer)"
        echo "  --install-dlstreamer      Install built intel-dlstreamer RPM only"
        echo ""
        echo "Build order: ${BUILD_ORDER[*]}"
        echo ""
        echo "Spec file locations:"
        for package in "${BUILD_ORDER[@]}"; do
            echo "  $package -> ${PACKAGES[$package]}"
        done
        exit 0
        ;;
    --check-deps)
        install_build_deps
        exit 0
        ;;
    --check-sources)
        check_sources
        exit 0
        ;;
    --dlstreamer-deps-only)
        log_info "Building only DL Streamer dependencies (no intel-dlstreamer)"
        install_build_deps
        check_sources
        rpmdev-setuptree
        for package in "paho-mqtt-c" "ffmpeg" "gstreamer" "opencv"; do
            build_package "$package"
        done
        log_info "========================================"
        log_info "DL Streamer dependencies built successfully! ✓"
        log_info "RPM packages are in ~/rpmbuild/RPMS/x86_64/"
        exit 0
        ;;

    --install-deps)
        log_info "Installing dependency RPMs in BUILD_ORDER (excluding intel-dlstreamer)"
        for package in "paho-mqtt-c" "ffmpeg" "gstreamer" "opencv"; do
            spec_file="$SCRIPT_DIR/${PACKAGES[$package]}"
            actual_package_name=$(grep "^Name:" "$spec_file" | awk '{print $2}')
            rpm_path=~/rpmbuild/RPMS/x86_64/${actual_package_name}-*.rpm
            if ls $rpm_path 1> /dev/null 2>&1; then
                log_info "Installing (or re-installing) $actual_package_name RPM(s)..."
                sudo rpm -Uvh --replacepkgs $rpm_path

                # Also install (or re-install) devel RPMs if present
                devel_rpm_path=~/rpmbuild/RPMS/x86_64/${actual_package_name}-devel-*.rpm
                if ls $devel_rpm_path 1> /dev/null 2>&1; then
                    log_info "Installing (or re-installing) $actual_package_name-devel RPM(s)..."
                    sudo rpm -Uvh --replacepkgs $devel_rpm_path
                fi
            else
                log_warn "RPM for $actual_package_name not found: $rpm_path"
            fi
        done
        log_info "Dependency RPM installation complete."
        exit 0
        ;;

    --install-dlstreamer)
        log_info "Installing intel-dlstreamer RPM..."
        spec_file="$SCRIPT_DIR/${PACKAGES["intel-dlstreamer"]}"
        actual_package_name=$(grep "^Name:" "$spec_file" | awk '{print $2}')
        rpm_path=~/rpmbuild/RPMS/x86_64/${actual_package_name}-*.rpm
        if ls $rpm_path 1> /dev/null 2>&1; then
            sudo rpm -Uvh $rpm_path
            log_info "intel-dlstreamer RPM installation complete."
        else
            log_error "intel-dlstreamer RPM not found: $rpm_path"
        fi
        exit 0
        ;;

    "")
        main
        ;;
    *)
        log_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
