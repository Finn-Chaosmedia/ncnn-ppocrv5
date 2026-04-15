#!/bin/bash
# Script zum automatischen Download von Abhängigkeiten

set -e

echo "📦 Downloading dependencies for ncnn-ppocrv5..."

# ncnn herunterladen
NCNN_VERSION="20250220"
NCNN_URL="https://github.com/Tencent/ncnn/releases/download/${NCNN_VERSION}/ncnn-${NCNN_VERSION}-android-vulkan.zip"
echo "📥 Downloading ncnn ${NCNN_VERSION}..."
wget -q $NCNN_URL
unzip -q "ncnn-${NCNN_VERSION}-android-vulkan.zip" -d app/src/main/jni/
echo "✅ ncnn downloaded"

# OpenCV Mobile herunterladen
OPENCV_VERSION="24.10"
OPENCV_URL="https://github.com/nihui/opencv-mobile/releases/download/${OPENCV_VERSION}/opencv-mobile-${OPENCV_VERSION}-android.zip"
echo "📥 Downloading OpenCV Mobile ${OPENCV_VERSION}..."
wget -q $OPENCV_URL
unzip -q "opencv-mobile-${OPENCV_VERSION}-android.zip" -d app/src/main/jni/
echo "✅ OpenCV Mobile downloaded"

echo "🎉 All dependencies downloaded successfully!"