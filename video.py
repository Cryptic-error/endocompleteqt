from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from PIL import Image
import numpy as np
import os
import subprocess
from PyQt5.QtGui import QImage  # Make sure to import QImage

def pil_to_qt_image(pil_image):
    # Convert PIL image to a format suitable for QImage
    pil_image = pil_image.convert("RGB")  # Ensure image is in RGB mode
    data = np.array(pil_image)  # Convert PIL image to a NumPy array
    h, w, ch = data.shape
    bytes_per_line = ch * w
    q_image = QImage(data.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return q_image

class LiveMediaDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live Media Display")
        self.setGeometry(100, 100, 1100, 800)

        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # Username input
        username_label = QtWidgets.QLabel("Enter username:")
        layout.addWidget(username_label)
        self.username_input = QtWidgets.QLineEdit()
        layout.addWidget(self.username_input)

        # Media source selection
        self.source_combo = QtWidgets.QComboBox()
        self.source_combo.addItems(["Camera", "USB Import"])
        self.source_combo.currentIndexChanged.connect(self.change_source)
        layout.addWidget(self.source_combo)

        # Initialize OpenCV video capture (default to Camera)
        self.cap = cv2.VideoCapture(0)

        # Create a label to display the video frame with increased size
        self.label = QtWidgets.QLabel()
        self.label.setMinimumSize(1000, 700)
        self.label.setAlignment(QtCore.Qt.AlignCenter) # Set the desired size for the video display
        layout.addWidget(self.label)

        # Add a button to capture an image
        capture_button = QtWidgets.QPushButton("Capture Image")
        capture_button.setFont(QtGui.QFont("Helvetica", 12))
        capture_button.setStyleSheet("background-color: grey; color: white;")
        capture_button.clicked.connect(self.capture_image)
        layout.addWidget(capture_button)

        # Add a button to open the form
        form_button = QtWidgets.QPushButton("Open Form")
        form_button.setFont(QtGui.QFont("Helvetica", 12))
        form_button.setStyleSheet("background-color: grey; color: white;")
        form_button.clicked.connect(self.open_form)
        layout.addWidget(form_button)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+0"), self)
        shortcut.activated.connect(self.capture_image)

        # Start updating the frame
        self.update_frame()

    def open_form(self):
        subprocess.Popen(['python', 'form.py'])

    def get_username(self):
        username = self.username_input.text()
        if not username:
            QtWidgets.QMessageBox.warning(self, "Input Required", "Please enter a username.")
            return None
        folder_path = os.path.join(os.getcwd(), username)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            qt_image = pil_to_qt_image(image)  # Convert PIL image to Qt image
            pixmap = QtGui.QPixmap.fromImage(qt_image)

            # Resize pixmap to fit the label size
            pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
        else:
            print("Failed to grab frame.")  # Debugging line to indicate frame read failure
        
        # Update the frame every 10 ms
        QtCore.QTimer.singleShot(10, self.update_frame)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            folder_path = self.get_username()
            if folder_path:
                # Get the next image number
                image_number = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]) + 1
                filename = os.path.join(folder_path, f"captured_image_{image_number}.jpg")
                cv2.imwrite(filename, frame)
                QtWidgets.QMessageBox.information(self, "Image Captured", f"Image saved as {filename}")
        else:
            print("Failed to capture image.")  # Debugging line to indicate image capture failure

    def change_source(self):
        source = self.source_combo.currentText()
        print(f"Changing source to: {source}")  # Debugging line to show selected source
        self.cap.release()
        if source == "Camera":
            self.cap = cv2.VideoCapture(0)
        elif source == "USB Import":
            self.cap = cv2.VideoCapture(1)  # Assuming USB import is the second device
  # Assuming USB import is the second device

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = LiveMediaDisplay()
    window.show()

    app.exec_()

    # Release the video capture when done
    window.cap.release()
    cv2.destroyAllWindows()
