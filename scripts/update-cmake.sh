#!/bin/bash
# Script zum Aktualisieren der CMakeLists.txt Pfade

set -e

echo "🔧 Updating CMakeLists.txt paths..."

cd app/src/main/jni

# Backup der originalen Datei
cp CMakeLists.txt CMakeLists.txt.backup

# Aktuelle Versionen ermitteln
NCNN_DIR=$(find . -maxdepth 1 -type d -name "ncnn-*-android-vulkan" | head -1)
OPENCV_DIR=$(find . -maxdepth 1 -type d -name "opencv-mobile-*-android" | head -1)

if [ -z "$NCNN_DIR" ] || [ -z "$OPENCV_DIR" ]; then
    echo "❌ Dependencies not found. Run download-dependencies.sh first."
    exit 1
fi

echo "📁 Found ncnn: $NCNN_DIR"
echo "📁 Found OpenCV: $OPENCV_DIR"

# Pfade in CMakeLists.txt aktualisieren
sed -i "s|/path/to/opencv-mobile-.*-android|\${CMAKE_CURRENT_SOURCE_DIR}/$(basename $OPENCV_DIR)|g" CMakeLists.txt
sed -i "s|/path/to/ncnn-.*-android-vulkan|\${CMAKE_CURRENT_SOURCE_DIR}/$(basename $NCNN_DIR)|g" CMakeLists.txt

echo "✅ CMakeLists.txt updated successfully!"