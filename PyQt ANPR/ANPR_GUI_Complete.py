#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ANPR GUI Complete System
========================

A complete, single-file ANPR (Automatic Number Plate Recognition) GUI application.
This file contains all components needed for a professional ANPR system.

Features:
- Real-time camera processing
- Multiple camera source support
- Region of Interest (ROI) configuration
- Vehicle whitelist/blacklist management
- Professional dark-themed interface
- Export capabilities
- System monitoring

Usage: python ANPR_GUI_Complete.py
"""

# Import required libraries
import sys
import os
import cv2
import numpy as np
import time
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from camera_thread import CameraThread
from PyQt5.QtWidgets import QHeaderView
from PyQt5 import QtCore
import logging
from logging.handlers import RotatingFileHandler

# ===== STYLESHEET =====
# Define the dark theme stylesheet for the application
DARK_THEME_STYLE = """
QMainWindow, QDialog {
    background: #2D2D30;
    color: #FFFFFF;
    font-family: "Segoe UI", Arial, sans-serif;
}

QWidget {
    background: #2D2D30;
    color: #FFFFFF;
}

QGroupBox {
    border: 1.5px solid #FFFFFF;
    border-radius: 8px;
    margin-top: 1em;
    padding-top: 10px;
    font-weight: bold;
    background: #232326;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 5px;
    color: #FFFFFF;
    font-size: 15px;
    letter-spacing: 1px;
}

QLabel {
    color: #FFFFFF;
}

QLabel#cameraDisplay {
    border: 2.5px solid #FFFFFF;
    border-radius: 8px;
    background: #1E1E1E;
    margin: 8px;
}

QPushButton {
    background: #094D69;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 5px 15px;
    min-height: 20px;
    font-weight: 500;
}

QPushButton:hover {
    background: #0A617F;
}

QPushButton:pressed {
    background: #083D54;
}

QPushButton:disabled {
    background: #2D2D30;
    color: #656565;
    border: 1px solid #3F3F46;
}

QComboBox {
    background: #1E1E1E;
    color: #FFFFFF;
    border: 1px solid #3F3F46;
    border-radius: 4px;
    padding: 3px 5px;
    min-height: 20px;
}

QComboBox QAbstractItemView {
    background: #1E1E1E;
    color: #FFFFFF;
    border: 1px solid #3F3F46;
    selection-background-color: #094D69;
}

QLineEdit {
    background: #1E1E1E;
    color: #FFFFFF;
    border: 1px solid #3F3F46;
    border-radius: 4px;
    padding: 3px 5px;
    min-height: 20px;
}

QLineEdit:focus {
    border: 1px solid #FFFFFF;
}

QCheckBox {
    color: #FFFFFF;
    spacing: 5px;
}

QListWidget {
    background: #1E1E1E;
    color: #FFFFFF;
    border: 1px solid #3F3F46;
    border-radius: 4px;
}

QListWidget::item {
    padding: 5px;
}

QListWidget::item:selected {
    background: #094D69;
    color: #FFFFFF;
}

QTableWidget {
    background: #1E1E1E;
    color: #FFFFFF;
    border: 1px solid #3F3F46;
    border-radius: 4px;
    gridline-color: #3F3F46;
    font-size: 14px;
}

QTableWidget::item {
    padding: 5px;
    border-bottom: 1px solid #232326;
}

QTableWidget::item:selected {
    background: #094D69;
    color: #FFFFFF;
}

QHeaderView::section {
    background: #232326;
    color: #FFD700;
    font-weight: bold;
    font-size: 15px;
    padding: 7px;
    border: 1px solid #3F3F46;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    letter-spacing: 1px;
}
"""

# ===== ANPR PROCESSOR CLASS =====
class ANPRProcessor(QObject):
    """ANPR Processing Engine: Handles frame processing, ROI, and simulated plate detection."""
    
    processed_frame = pyqtSignal(QImage)
    plate_result = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.camera_thread = None
        self.confidence_threshold = 0.7
        self.enable_ocr_correction = True
        self.country_template = "EU"
        self.roi = None

    def start_stream(self, source):
        """Start ANPR processing stream from the given camera source."""
        try:
            # Stop any existing thread before starting a new one
            if self.camera_thread is not None and self.camera_thread.isRunning():
                self.camera_thread.stop_streaming()
                self.camera_thread = None
            self.camera_thread = CameraThread()
            self.camera_thread.set_source(source)
            self.camera_thread.frame_ready_raw.connect(self.process_frame)
            self.camera_thread.error_occurred.connect(self.handle_error)
            self.camera_thread.start_streaming()
            return True
        except Exception as e:
            print(f"Error starting stream: {str(e)}")
            return False

    def stop_stream(self):
        """Stop the ANPR processing stream and release resources."""
        if self.camera_thread and self.camera_thread.isRunning():
            self.camera_thread.stop_streaming()
            self.camera_thread = None

    def set_roi(self, points):
        """Set the region of interest (ROI) for detection as a polygon."""
        if len(points) >= 4:
            self.roi = np.array(points, dtype=np.int32)

    def process_frame(self, frame):
        """Process each frame for license plate detection (simulated)."""
        try:
            # Only show the raw camera feed, no detection or overlays
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qt_image = QImage(rgb_frame.data.tobytes(), w, h, w * ch, QImage.Format_RGB888)
            self.processed_frame.emit(qt_image)
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
    
    def generate_random_plate(self):
        """Generate a random license plate for simulation purposes."""
        if self.country_template == "EU":
            letters = ''.join(np.random.choice(list('ABCDEFGHJKLMNPQRSTUVWXYZ'), 3))
            numbers = ''.join(np.random.choice(list('0123456789'), 3))
            return f"{letters}-{numbers}"
        elif self.country_template == "US":
            letters = ''.join(np.random.choice(list('ABCDEFGHJKLMNPQRSTUVWXYZ'), 3))
            numbers = ''.join(np.random.choice(list('0123456789'), 4))
            return f"{numbers}{letters}"
        else:
            letters = ''.join(np.random.choice(list('ABCDEFGHJKLMNPQRSTUVWXYZ'), 2))
            numbers = ''.join(np.random.choice(list('0123456789'), 4))
            return f"{letters}{numbers}"
    
    def handle_error(self, error_msg):
        """Handle errors from the camera thread."""
        print(f"Camera error: {error_msg}")

# ===== MAIN WINDOW CLASS =====
class ANPRMainWindow(QMainWindow):
    """Main ANPR Application Window: Handles the GUI layout, user interaction, and backend integration."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANPR Vehicle Detection System")
        self.setMinimumSize(1200, 800)
        self.camera_thread = None
        self.anpr_processor = None
        self.is_streaming = False
        self.roi_drawing_mode = False
        self.roi_points = []
        self.available_cameras = []  # Store available camera indices
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
        self.init_backend()
        self.scan_and_update_cameras()  # Scan cameras on startup
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_monitor)
        self.monitor_timer.start(2000)
    
    def setup_ui(self):
        """Setup the main user interface layout and panels."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)
        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        # Left and right panels
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([300, 700])
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """Setup the left control panel with camera, ROI, and vehicle list controls."""
        # Camera Settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QGridLayout()
        
        camera_layout.addWidget(QLabel("Camera Source:"), 0, 0)
        self.camera_combo = QComboBox()
        camera_layout.addWidget(self.camera_combo, 0, 1)
        
        self.refresh_camera_btn = QPushButton("Refresh")
        self.refresh_camera_btn.setFixedWidth(80)
        camera_layout.addWidget(self.refresh_camera_btn, 0, 2)
        
        camera_layout.addWidget(QLabel("Stream URL:"), 2, 0)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("rtsp://username:password@ip:port/stream")
        self.url_input.setEnabled(True)
        camera_layout.addWidget(self.url_input, 2, 1, 1, 2)
        
        # Remove the resolution dropdown and set a fixed label
        camera_layout.addWidget(QLabel("Resolution:"), 3, 0)
        self.resolution_label = QLabel("1280x720 (fixed)")
        camera_layout.addWidget(self.resolution_label, 3, 1, 1, 2)
        
        button_layout = QHBoxLayout()
        self.stream_button = QPushButton("Start Camera")
        self.stream_button.setCheckable(True)
        button_layout.addWidget(self.stream_button)
        
        self.led_indicator = QLabel()
        self.led_indicator.setFixedSize(16, 16)
        self.led_indicator.setStyleSheet("background-color: red; border-radius: 8px;")
        button_layout.addWidget(self.led_indicator)
        
        camera_layout.addLayout(button_layout, 4, 0, 1, 3)
        camera_group.setLayout(camera_layout)
        self.left_layout.addWidget(camera_group)
        
        # Detection Zone
        roi_group = QGroupBox("Detection Zone")
        roi_layout = QVBoxLayout()
        
        self.roi_button = QPushButton("Set Detection Area")
        roi_layout.addWidget(self.roi_button)
        
        roi_layout.addWidget(QLabel("Area Preview:"))
        self.roi_preview = QLabel("No detection area configured")
        self.roi_preview.setFixedHeight(100)
        self.roi_preview.setStyleSheet("border: 1px solid #FFFFFF;")
        self.roi_preview.setAlignment(QtCore.Qt.AlignCenter)
        roi_layout.addWidget(self.roi_preview)
        
        roi_group.setLayout(roi_layout)
        self.left_layout.addWidget(roi_group)
        
        # Vehicle List
        alerts_group = QGroupBox("Vehicle List")
        alerts_layout = QVBoxLayout()
        
        # Add search layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search vehicle...")
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_button)
        alerts_layout.addLayout(search_layout)
        
        # List widget
        self.plate_list = QListWidget()
        alerts_layout.addWidget(self.plate_list)
        
        alerts_group.setLayout(alerts_layout)
        self.left_layout.addWidget(alerts_group)
        
        self.left_layout.addStretch()
    
    def setup_right_panel(self):
        """Setup the right display panel with camera feed, results, and vehicle details."""
        # Remove any existing layout to avoid layout warnings
        if self.right_panel.layout() is not None:
            QWidget().setLayout(self.right_panel.layout())
        right_main_layout = QVBoxLayout()
        right_main_layout.setSpacing(10)
        right_main_layout.setContentsMargins(0, 0, 0, 0)
        self.right_panel.setLayout(right_main_layout)

        # Camera Feed (even wider and squarish)
        self.camera_feed_group = QGroupBox("Camera Feed")
        camera_feed_layout = QVBoxLayout(self.camera_feed_group)
        self.camera_display = QLabel("No camera feed")
        self.camera_display.setObjectName("cameraDisplay")
        self.camera_display.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_display.setStyleSheet("border: 1px solid #FFFFFF; background-color: #1E1E1E;")
        self.camera_display.setMinimumHeight(500)
        self.camera_display.setMinimumWidth(800)
        camera_feed_layout.addWidget(self.camera_display)
        right_main_layout.addWidget(self.camera_feed_group, stretch=3)

        # Vehicle Detection Results
        results_group = QGroupBox("Vehicle Detection Results")
        results_layout = QVBoxLayout(results_group)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Time", "Vehicle Type", "License Plate", "Color"])
        header = self.results_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        results_layout.addWidget(self.results_table)
        self.export_button = QPushButton("Export Report")
        results_layout.addWidget(self.export_button)
        right_main_layout.addWidget(results_group, stretch=2)

        # Vehicle Details (bottom frame)
        details_group = QGroupBox("Vehicle Details")
        details_layout = QVBoxLayout(details_group)
        self.vehicle_info_label = QLabel("Vehicle Info: N/A")
        self.vehicle_status_label = QLabel("Detection Status:")
        self.vehicle_status_bar = QProgressBar()
        self.vehicle_status_bar.setValue(0)
        details_layout.addWidget(self.vehicle_info_label)
        details_layout.addWidget(self.vehicle_status_label)
        details_layout.addWidget(self.vehicle_status_bar)
        right_main_layout.addWidget(details_group, stretch=1)
    
    def setup_menu_bar(self):
        """Setup the menu bar with file and settings options."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        export_action = QAction("Export Results", self)
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        settings_menu = menubar.addMenu("Settings")
        config_action = QAction("Configuration", self)
        settings_menu.addAction(config_action)
    
    def setup_status_bar(self):
        """Setup the status bar for feedback and system monitoring."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def setup_connections(self):
        """Connect UI controls to their event handlers."""
        self.stream_button.toggled.connect(self.toggle_stream)
        self.roi_button.clicked.connect(self.toggle_roi_mode)
        self.search_button.clicked.connect(self.search_vehicle)
        self.search_input.returnPressed.connect(self.search_vehicle)
        self.export_button.clicked.connect(self.export_results)
        self.camera_combo.currentTextChanged.connect(self.on_camera_source_changed)
        self.refresh_camera_btn.clicked.connect(self.scan_and_update_cameras)
    
    def init_backend(self):
        """Initialize the ANPR backend and connect signals."""
        self.anpr_processor = ANPRProcessor()
        self.anpr_processor.processed_frame.connect(self.update_frame)
        self.anpr_processor.plate_result.connect(self.add_detection_result)
        self.anpr_processor.handle_error = self.show_camera_error  # Override error handler
        if hasattr(self.anpr_processor, 'camera_thread') and self.anpr_processor.camera_thread:
            self.anpr_processor.camera_thread.error_occurred.connect(self.show_camera_error)
    
    def toggle_stream(self, checked):
        """Start or stop the camera stream based on user action."""
        if checked:
            source = self.get_camera_source()
            if self.anpr_processor is not None and self.anpr_processor.start_stream(source):
                self.is_streaming = True
                self.stream_button.setText("Stop Camera")
                self.led_indicator.setStyleSheet("background-color: green; border-radius: 8px;")
                self.status_bar.showMessage("Camera started")
            else:
                self.stream_button.setChecked(False)
                self.status_bar.showMessage("Failed to start camera")
        else:
            if self.anpr_processor is not None:
                self.anpr_processor.stop_stream()
            self.is_streaming = False
            self.stream_button.setText("Start Camera")
            self.led_indicator.setStyleSheet("background-color: red; border-radius: 8px;")
            self.status_bar.showMessage("Camera stopped")
            # Show 'No camera feed' when stopped
            self.camera_display.clear()
            self.camera_display.setText("No camera feed")
            self.camera_display.setAlignment(QtCore.Qt.AlignCenter)
            self.camera_display.setStyleSheet("border: 1px solid #FFFFFF; background-color: #1E1E1E;")
    
    def get_camera_source(self):
        """Get the selected camera source from the dropdown."""
        text = self.camera_combo.currentText()
        if text.startswith("Camera "):
            return int(text.split(" ")[1])
        elif text == "RTSP Stream" or text == "IP Camera":
            return self.url_input.text()
        return 0
    
    def toggle_roi_mode(self):
        """Enable or disable ROI drawing mode."""
        self.roi_drawing_mode = not self.roi_drawing_mode
        if self.roi_drawing_mode:
            self.roi_button.setText("Exit Drawing Mode")
            self.status_bar.showMessage("Click on camera feed to draw ROI")
        else:
            self.roi_button.setText("Set Detection Area")
            self.status_bar.showMessage("ROI drawing mode disabled")
    
    def add_plate(self):
        """Add a license plate to the monitoring list."""
        plate, ok = QInputDialog.getText(self, "Add Plate", "Enter license plate:")
        if ok and plate:
            self.plate_list.addItem(plate)
    
    def remove_plate(self):
        """Remove the selected license plate from the list."""
        current_item = self.plate_list.currentItem()
        if current_item:
            self.plate_list.takeItem(self.plate_list.row(current_item))
    
    def update_frame(self, frame):
        """Update the camera feed display with a new frame."""
        pixmap = QPixmap.fromImage(frame)
        scaled_pixmap = pixmap.scaled(self.camera_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.camera_display.setPixmap(scaled_pixmap)
        self.camera_display.setAlignment(QtCore.Qt.AlignCenter)
    
    def add_detection_result(self, result):
        """Add a new detection result to the results table."""
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        # Ensure all columns are filled: Time, Vehicle Type, License Plate, Color
        self.results_table.setItem(row, 0, QTableWidgetItem(result.get('timestamp', '')))
        self.results_table.setItem(row, 1, QTableWidgetItem(result.get('vehicle_type', 'Unknown')))
        self.results_table.setItem(row, 2, QTableWidgetItem(result.get('plate', '')))
        self.results_table.setItem(row, 3, QTableWidgetItem(result.get('color', 'Unknown')))
        # Check if plate is in monitoring list
        for i in range(self.plate_list.count()):
            item = self.plate_list.item(i)
            if item and result.get('plate', '') and item.text() == result.get('plate', ''):
                self.status_bar.showMessage(f"Monitored vehicle detected: {result.get('plate', '')}")
                break
    
    def export_results(self):
        """Export detection results to a CSV file."""
        filename, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Timestamp,Plate,Confidence\n")
                    for row in range(self.results_table.rowCount()):
                        timestamp_item = self.results_table.item(row, 0)
                        plate_item = self.results_table.item(row, 1)
                        confidence_item = self.results_table.item(row, 2)
                        timestamp = timestamp_item.text() if timestamp_item else ""
                        plate = plate_item.text() if plate_item else ""
                        confidence = confidence_item.text() if confidence_item else ""
                        f.write(f"{timestamp},{plate},{confidence}\n")
                self.status_bar.showMessage(f"Results exported to {filename}")
            except Exception as e:
                self.status_bar.showMessage(f"Export failed: {str(e)}")
    
    def update_system_monitor(self):
        """Update the status bar with system resource usage."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            status_text = f"CPU: {cpu_percent}% | Memory: {memory_percent}% | Disk: {disk_percent}% | "
            if self.is_streaming:
                status_text += "Camera: Active | FPS: N/A"
            else:
                status_text += "Camera: Inactive"
                
            self.status_bar.showMessage(status_text)
        except Exception as e:
            logger.error(f"Error updating system monitor: {str(e)}")

    def on_camera_source_changed(self, source):
        """Enable/disable URL input based on camera type."""
        text = self.camera_combo.currentText()
        if text in ["RTSP Stream", "IP Camera"]:
            self.url_input.setEnabled(True)
        else:
            self.url_input.setEnabled(False)

    def search_vehicle(self):
        """Search for vehicles in the monitoring list."""
        search_text = self.search_input.text().lower()
        for i in range(self.plate_list.count()):
            item = self.plate_list.item(i)
            if item:
                if search_text in item.text().lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def scan_and_update_cameras(self):
        """Scan for available cameras and update the dropdown."""
        self.available_cameras = CameraThread().get_available_cameras()
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        for idx in self.available_cameras:
            self.camera_combo.addItem(f"Camera {idx}", idx)
        self.camera_combo.addItem("RTSP Stream")
        self.camera_combo.addItem("IP Camera")
        self.camera_combo.blockSignals(False)
        # Enable/disable Start Camera button
        if self.available_cameras:
            self.stream_button.setEnabled(True)
            self.camera_combo.setCurrentIndex(0)
        else:
            self.stream_button.setEnabled(False)

    def show_camera_error(self, error_msg):
        """Show camera errors in a message box and status bar."""
        QMessageBox.critical(self, "Camera Error", error_msg)
        self.status_bar.showMessage(error_msg)
        self.stream_button.setChecked(False)
        self.stream_button.setText("Start Camera")
        self.led_indicator.setStyleSheet("background-color: red; border-radius: 8px;")
        self.is_streaming = False
        self.camera_display.clear()
        self.camera_display.setText("No camera feed")
        self.camera_display.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_display.setStyleSheet("border: 1px solid #FFFFFF; background-color: #1E1E1E;")

# ===== MAIN APPLICATION ENTRY POINT =====
def main():
    """Main application entry point: sets up the app and launches the main window."""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setOrganizationName("ANPR Solutions")
    app.setApplicationName("ANPR GUI Complete")
    
    # Apply dark theme
    app.setStyleSheet(DARK_THEME_STYLE)
    
    # Create and show main window
    window = ANPRMainWindow()
    window.show()
    
    # Start application
    sys.exit(app.exec_())

# ===== LOGGING SETUP =====
def setup_logging():
    """Setup logging for the application."""
    logger = logging.getLogger('ANPR')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('anpr.log', maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()

# ===== EXPORT TO PDF FUNCTION =====
def export_to_pdf(self):
    """Export detection results to a PDF file (if reportlab is installed)."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        
        filename, _ = QFileDialog.getSaveFileName(self, "Export to PDF", "", "PDF Files (*.pdf)")
        if filename:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Collect table data
            data = [["Time", "Vehicle Type", "License Plate", "Color"]]
            for row in range(self.results_table.rowCount()):
                row_data = []
                for col in range(self.results_table.columnCount()):
                    item = self.results_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            # Build PDF
            doc.build(elements)
            self.status_bar.showMessage(f"Results exported to PDF: {filename}")
            
    except Exception as e:
        logger.error(f"Error exporting to PDF: {str(e)}")
        self.status_bar.showMessage("Failed to export PDF. Check if reportlab is installed.")

if __name__ == "__main__":
    main()