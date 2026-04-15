#!/bin/bash
# Configuration for OCR Scanner build

# Build type: debug or release
BUILD_TYPE="debug"

# Run tests after build
RUN_TESTS="false"

# Android SDK configuration
ANDROID_SDK_VERSION="33"
ANDROID_NDK_VERSION="29.0.14206865"

# Dependency versions
NCNN_VERSION="20250220"
OPENCV_VERSION="24.10"

# Build flags
CMAKE_FLAGS="-DANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON"