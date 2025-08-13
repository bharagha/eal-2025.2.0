#!/bin/bash
# Source Download Script for Intel DL Streamer Modular Build
set -ex

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

download_file() {
    local url="$1"
    local output="$2"
    
    if [[ -f "$output" ]]; then
        log_warn "File $output already exists, skipping..."
        return 0
    fi
    
    log_info "Downloading $output..."
    if command -v wget &> /dev/null; then
        wget -O "$output" "$url"
    elif command -v curl &> /dev/null; then
        curl -L -o "$output" "$url"
    else
        log_error "Neither wget nor curl found. Please install one of them."
        exit 1
    fi
}

main() {
    log_info "Downloading source files for Intel DL Streamer modular build..."
    log_info "================================================================="
    
    # Define sources
    declare -A sources=(
        ["https://github.com/eclipse/paho.mqtt.c/archive/v1.3.4.tar.gz"]="paho.mqtt.c-1.3.4.tar.gz"
        ["https://ffmpeg.org/releases/ffmpeg-6.1.1.tar.gz"]="ffmpeg-6.1.1.tar.gz"
        ["https://github.com/opencv/opencv/archive/4.10.0.tar.gz"]="opencv-4.10.0.tar.gz"
        ["https://gitlab.freedesktop.org/gstreamer/gstreamer/-/archive/1.26.1/gstreamer-1.26.1.tar.gz"]="gstreamer-1.26.1.tar.gz"
    )
    
    # Download each source
    for url in "${!sources[@]}"; do
        download_file "$url" "${sources[$url]}"
    done

    # Download the DL Streamer src code
    cd ../..
    git submodule update --init libraries/dl-streamer/thirdparty/spdlog
    tar czf intel-dlstreamer-2025.2.0.tar.gz libraries/dl-streamer
    mv intel-dlstreamer-2025.2.0.tar.gz libraries/SPECS
    
    # Note about proprietary sources
    log_info ""
    log_warn "Manual download required for:"
    log_warn "1. intel-dlstreamer-2025.2.0.tar.gz"
    log_warn "   - Create this from your DL Streamer source code"
    log_warn "   - tar czf intel-dlstreamer-2025.2.0.tar.gz dlstreamer-source/"
    log_warn ""
    log_info ""
    log_info "================================================================="
    log_info "Source download completed!"
    log_info "Next step: ./build_all_packages.sh"
}

main "$@"
