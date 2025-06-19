import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import numpy as np

# CameraThread is a QThread subclass for handling camera capture in a separate thread
class CameraThread(QThread):
    # Signal emitted when a new frame is ready (as a QImage)
    frame_ready = pyqtSignal(QImage)
    # Signal emitted when a new frame is ready (as a numpy array)
    frame_ready_raw = pyqtSignal(object)
    # Signal emitted when an error occurs (with error message)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Flag to control the running state of the thread
        self.running = False
        # OpenCV VideoCapture object
        self.cap = None
        # Camera source index (default 0)
        self.source = 0

    def set_source(self, source):
        # Set the camera source (index or video file path)
        self.source = source

    def start_streaming(self):
        # Start the camera stream in a new thread
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            # Emit error if camera cannot be opened
            self.error_occurred.emit(f"Failed to open camera source: {self.source}")
            return False
        # Set camera properties: resolution and FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.running = True
        self.start()  # Start the thread (calls run())
        return True

    def stop_streaming(self):
        # Stop the camera stream and release resources
        self.running = False
        self.wait()  # Wait for the thread to finish
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def run(self):
        # Main loop for capturing frames from the camera
        while self.running and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                # Emit error if frame cannot be read
                self.error_occurred.emit("Failed to read frame from camera.")
                break
            # Emit the raw frame for processing
            self.frame_ready_raw.emit(frame)
            # For backward compatibility, also emit QImage
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            # Use .tobytes() to get the image buffer as bytes
            qt_image = QImage(rgb_frame.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_ready.emit(qt_image)
        # Release the camera when done
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_available_cameras(self):
        # Scan and return a list of available camera indices (0-9)
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras 