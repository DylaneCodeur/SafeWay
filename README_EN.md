# 🚗 SafeWay - AI-Powered Driver Assistance System

> **Created by [dylanecodeur](https://github.com/dylanecodeur)**

## 📋 Project Description

**SafeWay** is an advanced artificial intelligence system designed to improve road safety by monitoring the driver's state in real-time. The system uses the device's camera (computer, tablet, or phone) to automatically detect signs of fatigue, distraction, and dangerous behaviors, triggering immediate alerts to prevent accidents.

### 🎯 Problem Statement

Road accidents caused by fatigue, distraction, or phone use while driving represent a major public safety issue. Existing driver monitoring systems in high-end vehicles are:

- 💰 **Expensive** : Inaccessible to most drivers
- 🌍 **Geographically limited** : Mainly available in developed countries
- 🚫 **Non-existent** : Absent for taxis, buses, motorcycles, and older vehicles

**SafeWay** provides a **low-cost, accessible, and portable** solution that works simply with a camera and AI, making road safety accessible to everyone.

## ✨ Key Features

### 🔍 Real-time Detection

- **Face Detection** : Precise identification of the driver's face
- **Eye Analysis** : Detection of eye state (open/closed)
- **Mouth Analysis** : Detection of yawns (fatigue sign)
- **Head Position** : Tracking of head orientation
- **Hand Detection** : Identification of gestures and positions
- **Object Detection** : Uses YOLOv11 to detect phones

### 🚨 Intelligent Alert System

#### Detected Alert Types:

1. **Drowsiness** ⚠️
   - Eyes closed > 1.2 seconds
   - Message: "Stay alert, do not sleep at the wheel"

2. **Fatigue** 😴
   - 2+ yawns in 60 seconds
   - Abnormally low blink rate
   - Message: "Signs of fatigue detected, take a break if needed"

3. **Distraction** 👀
   - Gaze diverted > 1.5 seconds
   - Excessive head movements
   - Message: "You are not looking ahead, focus on the road"

4. **Phone Use** 📱
   - Detection of phone in hands
   - Message: "Please do not use your phone while driving"

5. **Driver Absent** 🚫
   - Face absent from view > 2.5 seconds
   - Message: "Driver absent, please regain control of the vehicle"

#### Alert Modes:

- **Visual** : Blinking on-screen messages with color codes
- **Audio** : Alert beeps according to severity
- **Voice** : French text-to-speech with personalized messages

### 🔒 Privacy and Security

- ✅ **100% local processing** : No video sent to cloud
- ✅ **Private data** : All analysis performed on-device
- ✅ **Open-source** : Fully accessible and auditable source code

## 🛠️ Technologies Used

### Main Libraries

- **OpenCV** (4.8+) : Video processing and image manipulation
- **MediaPipe** (0.10+) : Face, hands detection and landmark analysis
- **Ultralytics YOLOv11** : Ultra-performing object detection
- **NumPy** : Mathematical calculations and array manipulation
- **PyGame** : Alert sound generation and playback
- **pyttsx3** : Text-to-Speech synthesis

### AI Architecture

- **MediaPipe Face Mesh** : 468 facial landmarks for precise analysis
- **YOLOv11** : State-of-the-art object detection model
- **Custom Algorithms** : EAR (Eye Aspect Ratio), MAR (Mouth Aspect Ratio)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Camera (webcam, front camera)
- 2GB+ RAM recommended
- macOS, Linux, or Windows

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/dylanecodeur/SafeWay.git
cd SafeWay/safeway
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Download models**

MediaPipe models are automatically downloaded on first launch.

For YOLOv11:
```bash
python3 download_yolo11.py
```

4. **Launch SafeWay**

```bash
python3 ui/cli_demo.py
```

## 🎮 Usage

### Basic Launch

```bash
cd safeway
python3 ui/cli_demo.py
```

### Controls

- **'q'** : Quit application
- Camera opens automatically
- Alerts appear in real-time

### Configuration

Modify settings in `config/settings.py`:

```python
# Detection thresholds
EYE_CLOSED_TIME_MS = 1200  # Time before drowsiness alert
YAWN_COUNT_THRESHOLD = 2   # Number of yawns
DISTRACTION_TIME_MS = 1500  # Time before distraction alert

# Camera resolution
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
```

## 📁 Project Structure

```
SafeWay/
├── README.md                 # This file (bilingual)
├── README_FR.md             # Detailed French version
├── README_EN.md             # Detailed English version
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guide
├── CHANGELOG.md             # Version history
│
└── safeway/                 # Main source code
    ├── README.md            # Technical documentation
    ├── GUIDE_ENTRAINEMENT.md # Training guide
    ├── requirements.txt     # Python dependencies
    │
    ├── config/              # Configuration
    │   └── settings.py     # Global parameters
    │
    ├── ai/                  # AI modules
    │   ├── video_stream.py      # Video stream management
    │   ├── face_detector.py     # Face detection (MediaPipe)
    │   ├── hand_detector.py     # Hand detection (MediaPipe)
    │   ├── yolo_detector.py     # Object detection (YOLOv11)
    │   ├── state_analyzer.py    # Driver state analysis
    │   └── alert_manager.py     # Alert management
    │
    ├── core/                # Utilities
    │   ├── logger.py        # Logging system
    │   └── utils.py         # Utility functions
    │
    ├── ui/                  # User interface
    │   └── cli_demo.py      # CLI demonstration
    │
    ├── data/                # Data and models
    │   ├── models/          # AI models (YOLOv11)
    │   ├── logs/            # Log files
    │   ├── samples/         # Example videos
    │   └── dataset/         # Training dataset
    │
    ├── train_yolo.py        # Training script
    ├── annotate_images.py   # Annotation tool
    └── download_yolo11.py   # Model download
```

## 🎓 Custom Training

SafeWay allows training YOLOv11 with your own data to improve detection.

### Complete Guide

See [GUIDE_ENTRAINEMENT.md](safeway/GUIDE_ENTRAINEMENT.md) for:
- Dataset preparation
- Image annotation
- Training launch
- Advanced optimizations

### Quick Start

```bash
# Create template
python3 train_yolo.py --create-template

# Annotate your images
python3 annotate_images.py

# Launch training
python3 train_yolo.py --epochs 100 --batch 16
```

## 📊 Performance

### Metrics

- **FPS** : 15+ frames per second
- **Latency** : <100ms per frame
- **Fatigue accuracy** : >90%
- **Phone accuracy** : >85% (YOLOv11)
- **CPU usage** : 30-50% (modern processor)

### Optimizations

- YOLO runs every 3 frames (fluidity optimization)
- Detection result caching
- YOLOv11 model optimized with `fuse()` and `compile()`
- NumPy vectorization for fast calculations

## 🔧 Development

### Adding New Detections

1. Create a new module in `ai/`
2. Integrate it in `state_analyzer.py`
3. Add alerts in `alert_manager.py`

### Testing

```bash
# Test imports
python3 test_imports.py

# Full test
python3 ui/cli_demo.py
```

## 🐛 Troubleshooting

### Camera won't open

- Check camera permissions
- Change `CAMERA_INDEX` in `config/settings.py`
- Verify no other app is using the camera

### MediaPipe errors

- Reinstall: `pip install --upgrade mediapipe`
- Check Python 3.8+

### YOLO errors

- Check internet connection (automatic download)
- Reinstall: `pip install --upgrade ultralytics`

## 📈 Roadmap

- [ ] Graphical interface (GUI) with PyQt/Tkinter
- [ ] Multi-camera support
- [ ] Statistics export (CSV, JSON)
- [ ] Night mode optimization
- [ ] Seatbelt detection
- [ ] Navigation system integration
- [ ] Mobile application (Flutter/React Native)

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 👨‍💻 Author

**Created by [dylanecodeur](https://github.com/dylanecodeur)**

- GitHub: [@dylanecodeur](https://github.com/dylanecodeur)
- Project: SafeWay - Driver Assistance System

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv11
- **Google MediaPipe** for detection tools
- **OpenCV** for video processing
- The open-source community

## ⭐ Support

If this project helped you, feel free to:
- ⭐ Star on GitHub
- 🐛 Report bugs
- 💡 Suggest improvements
- 📢 Share the project

---

**SafeWay** - Drive safely! 🛡️

*Created with ❤️ by dylanecodeur*

