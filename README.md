# <img src="https://img.icons8.com/ios-filled/50/000000/license-plate.png" width="36" style="vertical-align:middle;"> ANPR GUI Complete System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6%2B-blue?logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/GUI-PyQt5-41b883" alt="PyQt5">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/674621/146652416-5e4c3c2b-6b7e-4b2e-8e2e-2e7e7e7e7e7e.png" width="600" alt="ANPR GUI Banner">
</p>

---

> **A modern, professional, and fully-featured Automatic Number Plate Recognition (ANPR) GUI system with real-time camera processing, advanced detection, and a beautiful dark-themed interface.**

---

## 📑 Table of Contents
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [File Descriptions](#-file-descriptions)
- [Requirements](#-requirements)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [GUI Architecture](#-gui-architecture)
- [Backend Integration](#-backend-integration)
- [Troubleshooting](#-troubleshooting)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)

---

## 🚀 Features

- **Real-time Camera Processing**: Live video feed with instant plate detection
- **Multiple Camera Sources**: Laptop webcam, USB, RTSP, and IP cameras
- **Region of Interest (ROI)**: Draw and configure detection zones
- **Vehicle Monitoring**: Whitelist/blacklist with customizable alerts
- **Professional UI**: Modern dark theme, responsive layout
- **Detection Dashboard**: Real-time results with confidence scores
- **Export**: Save results to CSV or PDF
- **System Monitoring**: CPU, memory, and disk usage
- **Audio Notifications**: Customizable sound alerts
- **Configurable Parameters**: Confidence thresholds, detection settings

---

## 📁 Project Structure

```
PyQt ANPR/
├── ANPR_GUI_Complete.py   # Main application (GUI, backend, logic)
├── camera_thread.py       # Camera threading for smooth video
├── test_opencv_camera.py  # Simple OpenCV camera test
└── README.md              # This documentation
```

---

## 🗂️ File Descriptions

### `ANPR_GUI_Complete.py`
- **Purpose**: Main application file. Contains the GUI, backend logic, and all user interactions.
- **Features**: Real-time video, ROI, vehicle list, results dashboard, export, system monitoring, dark theme.
- **Key Classes/Methods**:
  - `ANPRMainWindow`: Main GUI window, sets up all panels, controls, and event handling
  - `ANPRProcessor`: Handles frame processing, ROI, and simulated plate detection
  - `main()`: Application entry point

### `camera_thread.py`
- **Purpose**: Handles camera capture in a separate thread to keep the GUI responsive.
- **Features**: Starts/stops camera streams, emits frames as QImage, error handling, camera scanning.
- **Key Methods**:
  - `set_source(source)`, `start_streaming()`, `stop_streaming()`, `run()`, `get_available_cameras()`

### `test_opencv_camera.py`
- **Purpose**: Simple script to test if OpenCV can access the default camera.
- **Features**: Opens camera, displays live video, exits on 'q'.

---

## 🛠️ Requirements

- **Python**: 3.6 or higher
- **OS**: Windows, macOS, or Linux
- **Camera**: Built-in or USB (optional for testing)

**Python Dependencies:**
```bash
pip install PyQt5 opencv-python numpy
```

---

## ⚡ Installation & Setup

1. **Clone or Download** the repository
2. **Install dependencies**:
   ```bash
   pip install PyQt5 opencv-python numpy
   ```
3. **Run the application**:
   ```bash
   python ANPR_GUI_Complete.py
   ```

**(Optional)**: Create a virtual environment for isolation:
```bash
python -m venv anpr_env
source anpr_env/bin/activate  # On Windows: anpr_env\Scripts\activate
pip install PyQt5 opencv-python numpy
```

---

## 🎯 Usage Guide

### Basic Operation
1. **Start the Application**: `python ANPR_GUI_Complete.py`
2. **Configure Camera**: Select source (webcam, RTSP, IP)
3. **Set Detection Zone**: Click "Set Detection Area" and draw ROI
4. **Start Processing**: Click "Start Camera"
5. **Monitor Results**: View detected plates in the dashboard

### Advanced Features
- **Detection Zone**: Draw polygon on video feed for focused detection
- **Vehicle List**: Add/remove plates to monitor, search, and get alerts
- **Export**: Save results to CSV or PDF
- **System Monitoring**: View CPU, memory, and disk usage in real time
- **Custom Alerts**: Enable sound notifications for specific vehicles

---

## 🏗️ GUI Architecture

```
Main Window (ANPRMainWindow)
├── Left Panel (Controls)
│   ├── Camera Settings
│   ├── Detection Zone (ROI)
│   └── Vehicle List
├── Right Panel (Display)
│   ├── Camera Feed
│   ├── Detection Results Table
│   └── Vehicle Details
├── Menu Bar (File, Settings)
└── Status Bar (System/Camera status)
```

- **ANPRMainWindow**: Sets up all panels, controls, and event handling
- **ANPRProcessor**: Handles frame processing, ROI, and simulated plate detection
- **CameraThread**: (see `camera_thread.py`) Handles threaded camera capture

---

## 🔗 Backend Integration

- **Easy to integrate** with real ANPR APIs (OpenALPR, Google Cloud Vision, Azure, Tesseract, etc.)
- Replace the simulation in `ANPRProcessor` with your backend call for production use

---

## 🐛 Troubleshooting

### Camera Not Working
- Check permissions, try different indices (0, 1, 2...)
- Ensure no other app is using the camera

### GUI Not Loading
- Reinstall PyQt5: `pip uninstall PyQt5 && pip install PyQt5`
- Check Python version compatibility

### Performance Issues
- Lower camera resolution
- Use ROI to limit processing area
- Close other apps using the camera

---

## 📦 Deployment

- **Direct Python**: `python ANPR_GUI_Complete.py`
- **PyInstaller**: Create standalone executable
  ```bash
  pip install pyinstaller
  pyinstaller --onefile ANPR_GUI_Complete.py
  ```
- **Docker**: Containerize for consistent deployment
- **Cloud**: Deploy to cloud platforms

---

## 🔮 Future Enhancements

- Real ANPR integration (OpenALPR, Tesseract, etc.)
- Database storage for detection history
- Remote monitoring and control
- Advanced analytics and reporting
- Mobile app companion

---

<p align="center">
  <b>Made with ❤️ for smart vehicle monitoring and security</b>
</p>
