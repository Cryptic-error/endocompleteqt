from PyQt5 import QtWidgets, QtGui , QtCore
from PIL import Image
import io
import subprocess

class EndoscopyForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Endoscopy Form")
        self.setGeometry(100, 100, 1100, 800)

        # Main Layout
        layout = QtWidgets.QVBoxLayout(self)

        # Scroll Area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Header Frame
        header_frame = QtWidgets.QFrame()
        header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        header_frame.setFixedHeight(300)
        header_layout = QtWidgets.QHBoxLayout(header_frame)
        scroll_layout.addWidget(header_frame)

        # Image Frame
        image_frame = QtWidgets.QFrame()
        image_frame.setFixedSize(200, 200)
        image_layout = QtWidgets.QVBoxLayout(image_frame)
        header_layout.addWidget(image_frame)

        # Load and display letterhead image
        letterhead_image_path = "subha swastik.jpg"  # Update this path to your image file
        letterhead_image = Image.open(letterhead_image_path)
        letterhead_image = letterhead_image.resize((200, 200), Image.LANCZOS)  # Resize to fit the frame

        # Convert the PIL image to a format compatible with PyQt5
        qt_image = self.pil_to_qt_image(letterhead_image)
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(pixmap)
        image_layout.addWidget(image_label, alignment=QtCore.Qt.AlignCenter)

        # Header Texts Layout
        header_text_layout = QtWidgets.QVBoxLayout()
        header_layout.addLayout(header_text_layout)

        # Large Header
        large_header = QtWidgets.QLabel("Subha Swastik Hospital PVT LTD")
        large_header.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold))
        header_text_layout.addWidget(large_header, alignment=QtCore.Qt.AlignCenter)

        # Medium Header 1
        medium_header1 = QtWidgets.QLabel("Bardibas-14, Mahottari")
        medium_header1.setFont(QtGui.QFont("Helvetica", 16))
        header_text_layout.addWidget(medium_header1, alignment=QtCore.Qt.AlignCenter)

        # Medium Header 2
        medium_header2 = QtWidgets.QLabel("Report of Sigmoidoscopy/Colonoscopy")
        medium_header2.setFont(QtGui.QFont("Helvetica", 16))
        header_text_layout.addWidget(medium_header2, alignment=QtCore.Qt.AlignCenter)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        scroll_layout.addLayout(button_layout)

        video_button = QtWidgets.QPushButton("Open Video")
        video_button.clicked.connect(self.video_player)
        button_layout.addWidget(video_button)

        form_button = QtWidgets.QPushButton("Open Form")
        form_button.clicked.connect(self.form)
        button_layout.addWidget(form_button)

        fetch_button = QtWidgets.QPushButton("Get Data")
        fetch_button.clicked.connect(self.fetch)
        button_layout.addWidget(fetch_button)

    def pil_to_qt_image(self, pil_image):
        """ Convert a PIL image to QImage. """
        with io.BytesIO() as buffer:
            pil_image.save(buffer, format="PNG")
            buffer.seek(0)
            q_image = QtGui.QImage()
            q_image.loadFromData(buffer.getvalue())
        return q_image

    def video_player(self):
        subprocess.Popen(['python', 'video.py'])

    def fetch(self):
        subprocess.Popen(['python', 'fetch.py'])

    def form(self):
        subprocess.Popen(['python', 'form.py'])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = EndoscopyForm()
    window.show()

    app.exec_()
