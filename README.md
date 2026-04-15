# ncnn-android-ppocrv5 - OCR Scanner 🤖

![Build Status](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/actions/workflows/build.yml/badge.svg)
![Tests](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/actions/workflows/test.yml/badge.svg)
![Release](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/actions/workflows/release.yml/badge.svg)

**PPOCRv5** - A high-performance OCR (Optical Character Recognition) scanner for Android using ncnn and OpenCV Mobile.

## 🚀 Features

- 📱 **Real-time OCR** using camera or images
- ⚡ **High performance** with ncnn neural network inference
- 🔋 **Offline operation** - no internet connection required
- 🎯 **Accurate text detection** with PPOCRv5 models
- 🔧 **Easy integration** with existing Android apps

## 📦 Automated Builds with GitHub Actions

This project now features **fully automated CI/CD** with GitHub Actions!

### 📱 Download Latest APK
1. Go to [Releases](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/releases)
2. Download the latest `.apk` file
3. Install on your Android device (Android 5.0+)

### 🔧 Local Development Setup

#### Prerequisites
- Java JDK 11 or higher
- Android SDK
- Git

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/Finn-Chaosmedia/ncnn-ppocrv5.git
cd ncnn-ppocrv5

# Make scripts executable
chmod +x scripts/*.sh

# Download dependencies automatically
./scripts/download-dependencies.sh

# Update build configuration
./scripts/update-cmake.sh

# Build the APK
./scripts/build.sh

# The APK will be in: app/build/outputs/apk/debug/
```

#### Advanced Build Options
```bash
# Build release version
BUILD_TYPE=release ./scripts/build.sh

# Build with tests
RUN_TESTS=true ./scripts/build.sh

# Clean build
./gradlew clean
```

## 🏗️ Project Structure

```
ncnn-ppocrv5/
├── .github/workflows/          # GitHub Actions CI/CD
│   ├── build.yml              # Automated APK builds
│   ├── test.yml               # Test execution
│   └── release.yml            # Release automation
├── scripts/                   # Build automation scripts
│   ├── download-dependencies.sh
│   ├── update-cmake.sh
│   ├── build.sh
│   └── config.sh
├── app/                       # Android application
│   ├── src/main/java/        # Java/Kotlin source code
│   ├── src/main/jni/         # Native C++ code
│   │   ├── CMakeLists.txt    # Native build configuration
│   │   ├── ppocrv5.cpp       # OCR implementation
│   │   └── ndkcamera.cpp     # Camera integration
│   └── build.gradle          # Android build configuration
├── gradle/                    # Gradle wrapper
└── README.md                 # This file
```

## 🤖 OCR Scanner Agent

This project is maintained by an **automated OCR Scanner Agent** that:

### ✅ Automated Tasks
- **Build Automation**: APK builds on every commit
- **Dependency Management**: Automatic updates for ncnn and OpenCV
- **Testing**: Runs tests to ensure quality
- **Release Management**: Creates releases when tags are pushed
- **Monitoring**: Checks for issues and updates

### 🔍 Agent Features
```bash
# Run the agent manually
python3 agent-monitor.py

# Agent will:
# 1. Check for dependency updates
# 2. Run automated builds
# 3. Report issues
# 4. Update configuration
```

## 📊 Performance

- **FPS**: 10-30 FPS on modern devices
- **Accuracy**: >95% on clear text
- **Languages**: English, Chinese, and more
- **Model Size**: ~10MB for mobile models

## 🔧 Customization

### Adding New Languages
1. Train or obtain PPOCRv5 models for your language
2. Convert to ncnn format using pnnx
3. Update `ppocrv5_dict.h` with new character set
4. Rebuild the app

### Model Optimization
```bash
# Convert your own models
pip install paddleocr paddlepaddle pnnx

# Export ONNX models
paddlex --paddle2onnx --paddle_model_dir your_model --onnx_model_dir output

# Convert to ncnn
pnnx your_model.onnx inputshape=[1,3,320,320]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Clean and rebuild
./gradlew clean
./scripts/build.sh

# Check Android SDK version
# Ensure Android SDK 33+ is installed
```

#### 2. Camera Issues
- Ensure camera permissions are granted
- Check if device supports Camera2 API
- Test with different camera resolutions

#### 3. Performance Issues
- Try CPU instead of GPU (some devices)
- Reduce image resolution
- Use lighter models

### Getting Help
1. Check [GitHub Issues](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/issues)
2. Review build logs in GitHub Actions
3. Test with sample images

## 📈 Roadmap

### Planned Features
- [ ] Batch image processing
- [ ] Multi-language support
- [ ] PDF export
- [ ] Cloud synchronization
- [ ] REST API for OCR
- [ ] Improved UI/UX

### Performance Improvements
- [ ] GPU optimization
- [ ] Model quantization
- [ ] Memory usage reduction
- [ ] Faster text detection

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create a feature branch**
3. **Make your changes**
4. **Run tests**: `./gradlew test`
5. **Submit a Pull Request**

### Development Guidelines
- Follow Android Kotlin/Java style guide
- Add tests for new features
- Update documentation
- Keep dependencies updated

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Tencent ncnn](https://github.com/Tencent/ncnn) - High-performance neural network inference
- [OpenCV Mobile](https://github.com/nihui/opencv-mobile) - Optimized OpenCV for mobile
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - OCR models and tools
- [nihui](https://github.com/nihui) - Original ncnn-android-ppocrv5 implementation

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Finn-Chaosmedia/ncnn-ppocrv5/issues)
- **Email**: finn@chaosmedia.de
- **Documentation**: This README and code comments

---

**Built with ❤️ by the OpenClaw community** 🦞

*Last updated: April 2026*