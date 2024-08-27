from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from PIL import Image
import numpy as np
import os
from PyQt5.QtGui import QImage
import sys

def pil_to_qt_image(pil_image):
    pil_image = pil_image.convert("RGB")
    data = np.array(pil_image)
    h, w, ch = data.shape
    bytes_per_line = ch * w
    q_image = QImage(data.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return q_image

class LiveMediaDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Media Display")
        self.setGeometry(100, 100, 1100, 800)

        # Layout and widgets setup
        layout = QtWidgets.QVBoxLayout(self)
        self.username_input = QtWidgets.QLineEdit()
        layout.addWidget(self.username_input)
        self.source_combo = QtWidgets.QComboBox()
        self.source_combo.addItems(["Camera", "USB Import"])
        self.source_combo.currentIndexChanged.connect(self.change_source)
        layout.addWidget(self.source_combo)
        self.cap = cv2.VideoCapture(0)
        self.label = QtWidgets.QLabel()
        self.label.setMinimumSize(1000, 700)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)
        capture_button = QtWidgets.QPushButton("Capture Image")
        capture_button.clicked.connect(self.capture_image)
        layout.addWidget(capture_button)
        form_button = QtWidgets.QPushButton("Open Form")
        form_button.clicked.connect(self.open_form)
        layout.addWidget(form_button)
        self.update_frame()

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+0"), self)
        self.shortcut.activated.connect(self.capture_image)

        self.update_frame()
        
    def open_form(self):
        try:
            from form import FormWindow
            self.form_window = FormWindow()
            self.form_window.show()
        except Exception as e:
            print(f"An error occurred while opening the form: {e}")

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
        try:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                qt_image = pil_to_qt_image(image)
                pixmap = QtGui.QPixmap.fromImage(qt_image)
                pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
                self.label.setPixmap(pixmap)
            else:
                print("Failed to grab frame.")
        except Exception as e:
            print(f"An error occurred while updating the frame: {e}")
        
        QtCore.QTimer.singleShot(10, self.update_frame)

    def capture_image(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                folder_path = self.get_username()
                if folder_path:
                    image_number = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]) + 1
                    filename = os.path.join(folder_path, f"captured_image_{image_number}.jpg")
                    cv2.imwrite(filename, frame)
                    QtWidgets.QMessageBox.information(self, "Image Captured", f"Image saved as {filename}")
            else:
                print("Failed to capture image.")
        except Exception as e:
            print(f"An error occurred while capturing the image: {e}")

    def change_source(self):
        try:
            source = self.source_combo.currentText()
            print(f"Changing source to: {source}")
            self.cap.release()
            if source == "Camera":
                self.cap = cv2.VideoCapture(0)
            elif source == "USB Import":
                self.cap = cv2.VideoCapture(1)
        except Exception as e:
            print(f"An error occurred while changing the source: {e}")

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
        super().closeEvent(event)

def run_video_app():
    try:
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        window = LiveMediaDisplay()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred while running the video app: {e}")

if __name__ == '__main__':
    run_video_app()