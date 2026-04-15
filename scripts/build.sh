#!/bin/bash
# Main build script for OCR Scanner

set -e

echo "🚀 Starting OCR Scanner build..."

# Load configuration
if [ -f "scripts/config.sh" ]; then
    source scripts/config.sh
else
    BUILD_TYPE="debug"
    RUN_TESTS="false"
fi

# Download dependencies
echo "📦 Downloading dependencies..."
chmod +x scripts/download-dependencies.sh
./scripts/download-dependencies.sh

# Update CMake paths
echo "🔧 Updating build configuration..."
chmod +x scripts/update-cmake.sh
./scripts/update-cmake.sh

# Run Gradle build
echo "🏗️ Building APK..."
if [ "$BUILD_TYPE" = "release" ]; then
    ./gradlew assembleRelease
    echo "✅ Release APK built successfully!"
else
    ./gradlew assembleDebug
    echo "✅ Debug APK built successfully!"
fi

# Run tests if requested
if [ "$RUN_TESTS" = "true" ]; then
    echo "🧪 Running tests..."
    ./gradlew test
    echo "✅ Tests completed!"
fi

echo "🎉 Build completed successfully!"