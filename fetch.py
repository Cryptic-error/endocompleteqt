import sys
import os
import subprocess
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QTextEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QScrollArea, QFrame, QGridLayout, QScrollBar, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt,QDate
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Endoscopy Form")
        self.setGeometry(100, 100, 1100, 800)

        # Create central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Scroll Area
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # Create a widget to contain all scrollable content
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        # Create main layout for the scrollable content
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)

        # Header Frame
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_frame.setFrameShadow(QFrame.Raised)
        scroll_layout.addWidget(header_frame)

        header_layout = QGridLayout()
        header_frame.setLayout(header_layout)

        # Image Frame
        image_frame = QFrame()
        image_frame.setFixedSize(200, 200)
        header_layout.addWidget(image_frame, 0, 0, 3, 1)

        letterhead_image_path = "subha swastik.jpg"  # Update this path to your image file
        if os.path.exists(letterhead_image_path):
            letterhead_image = QPixmap(letterhead_image_path).scaled(200, 200, Qt.KeepAspectRatio)
            letterhead_label = QLabel()
            letterhead_label.setPixmap(letterhead_image)
            image_frame_layout = QVBoxLayout()
            image_frame.setLayout(image_frame_layout)
            image_frame_layout.addWidget(letterhead_label)

        # Header Texts
        large_header = QLabel("Subha Swastik Hospital PVT LTD")
        large_header.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(large_header, 0, 1, 1, 1)

        medium_header1 = QLabel("Bardibas-14,Mahottari")
        medium_header1.setStyleSheet("font-size: 16px;")
        header_layout.addWidget(medium_header1, 1, 1, 1, 1)

        medium_header2 = QLabel("Report of Sigmoidoscopy/Colonoscopy")
        medium_header2.setStyleSheet("font-size: 16px;")
        header_layout.addWidget(medium_header2, 2, 1, 1, 1)

        # Form fields
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setFrameShadow(QFrame.Raised)
        scroll_layout.addWidget(form_frame)

        form_layout = QGridLayout()
        form_frame.setLayout(form_layout)

        self.create_form_fields(form_layout)

        # Fetch Data Button
        fetch_button = QPushButton("Fetch Data")
        fetch_button.clicked.connect(self.fetch_data)
        form_layout.addWidget(fetch_button, 14, 0, 1, 6)

        # Open Video Button
        video_button = QPushButton("Open Video")
        video_button.clicked.connect(self.video_player)
        form_layout.addWidget(video_button, 15, 0, 1, 6)

        # Open Form Button
        form_button = QPushButton("Open form")
        form_button.clicked.connect(self.form)
        form_layout.addWidget(form_button, 16, 0, 1, 6)

    def create_form_fields(self, layout):
        # Creating form fields similar to Tkinter layout
        self.name_entry = QLineEdit()
        layout.addWidget(QLabel("Name:"), 1, 0)
        layout.addWidget(self.name_entry, 1, 1)

        self.bill_no_entry = QLineEdit()
        layout.addWidget(QLabel("Bill No:"), 1, 2)
        layout.addWidget(self.bill_no_entry, 1, 3)

        self.age_entry = QLineEdit()
        layout.addWidget(QLabel("Age:"), 1, 4)
        layout.addWidget(self.age_entry, 1, 5)

        self.sex_combo = QComboBox()
        self.sex_combo.addItems(["Male", "Female", "Other"])
        layout.addWidget(QLabel("Sex:"), 2, 2)
        layout.addWidget(self.sex_combo, 2, 3)

        self.phone_no_entry = QLineEdit()
        layout.addWidget(QLabel("Phone No:"), 2, 0)
        layout.addWidget(self.phone_no_entry, 2, 1)

        self.date_entry = QLineEdit()
        layout.addWidget(QLabel("Date:"), 2, 4)
        layout.addWidget(self.date_entry, 2, 5)

        self.indication_text = QTextEdit()
        layout.addWidget(QLabel("Indication:"), 3, 0)
        layout.addWidget(self.indication_text, 3, 1, 1, 4)

        self.referred_by_entry = QLineEdit()
        layout.addWidget(QLabel("Referred By:"), 3, 2)
        layout.addWidget(self.referred_by_entry, 3, 3)

        self.anus_combo = QComboBox()
        self.anus_combo.addItems(["Normal", "Abnormal"])
        layout.addWidget(QLabel("Anus:"), 7, 0)
        layout.addWidget(self.anus_combo, 7, 1)

        self.rectum_entry = QLineEdit()
        layout.addWidget(QLabel("Rectum:"), 7, 2)
        layout.addWidget(self.rectum_entry, 7, 3)

        self.sigmoid_colon_entry = QLineEdit()
        layout.addWidget(QLabel("Sigmoid colon:"), 7, 4)
        layout.addWidget(self.sigmoid_colon_entry, 7, 5)

        self.descending_colon_entry = QLineEdit()
        layout.addWidget(QLabel("Descending colon:"), 8, 0)
        layout.addWidget(self.descending_colon_entry, 8, 1)

        self.transverse_colon_entry = QLineEdit()
        layout.addWidget(QLabel("Transverse colon:"), 8, 2)
        layout.addWidget(self.transverse_colon_entry, 8, 3)

        self.ascending_colon_entry = QLineEdit()
        layout.addWidget(QLabel("Ascending colon:"), 8, 4)
        layout.addWidget(self.ascending_colon_entry, 8, 5)

        self.caecum_entry = QLineEdit()
        layout.addWidget(QLabel("Caecum:"), 9, 0)
        layout.addWidget(self.caecum_entry, 9, 1)

        self.endoscopist_entry = QLineEdit()
        layout.addWidget(QLabel("Endoscopist:"), 9, 2)
        layout.addWidget(self.endoscopist_entry, 9, 3)

        self.diagnosis_text = QTextEdit()
        layout.addWidget(QLabel("Diagnosis:"), 10, 0)
        layout.addWidget(self.diagnosis_text, 10, 1, 1, 4)

        self.comments_procedure_text = QTextEdit()
        layout.addWidget(QLabel("Comments on Procedure:"), 11, 0)
        layout.addWidget(self.comments_procedure_text, 11, 1, 1, 4)

        # Image labels
        self.signature_image = QLabel()
        layout.addWidget(QLabel("Signature:"), 12, 0)
        layout.addWidget(self.signature_image, 12, 1)

        self.picture1_image = QLabel()
        layout.addWidget(QLabel("Picture 1:"), 12, 2)
        layout.addWidget(self.picture1_image, 12, 3)

        self.picture2_image = QLabel()
        layout.addWidget(QLabel("Picture 2:"), 13, 0)
        layout.addWidget(self.picture2_image, 13, 1)

        self.picture3_image = QLabel()
        layout.addWidget(QLabel("Picture 3:"), 13, 2)
        layout.addWidget(self.picture3_image, 13, 3)

        self.picture4_image = QLabel()
        layout.addWidget(QLabel("Picture 4:"), 13, 4)
        layout.addWidget(self.picture4_image, 13, 5)

    def form(self):
        subprocess.Popen(['python', 'form.py'])

    def video_player(self):
        subprocess.Popen(['python', 'video.py'])

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ilovenepal123",
                database="endoscopy"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM endoscopy_form WHERE bill_no = %s", (self.bill_no_entry.text(),))
            row = cursor.fetchone()

            if row:
                self.name_entry.setText(row['name'])
                self.age_entry.setText(str(row['age']))
                self.sex_combo.setCurrentText(row['sex'])
                self.phone_no_entry.setText(row['phone_no'])
                self.referred_by_entry.setText(row['referred_by'])
                self.indication_text.setPlainText(row['indication'])
                date_obj = row['date']  # This is a datetime.date object

                # Convert the datetime.date object to a QDate object
                if date_obj:  # Check if the date_obj is not None
                    qdate = QDate(date_obj.year, date_obj.month, date_obj.day)

                    # Set the QDate object in the QDateEdit widget
                    self.date_entry.setText(str(qdate))
                else:
                    # Handle the case where date_obj is None
                    self.date_entry.text(str(QDate.currentDate()))
                self.anus_combo.setCurrentText(row['anus'])
                self.rectum_entry.setText(row['rectum'])
                self.sigmoid_colon_entry.setText(row['sigmoid_colon'])
                self.descending_colon_entry.setText(row['descending_colon'])
                self.transverse_colon_entry.setText(row['transverse_colon'])
                self.ascending_colon_entry.setText(row['ascending_colon'])
                self.caecum_entry.setText(row['caecum'])
                self.diagnosis_text.setPlainText(row['diagnosis'])
                self.comments_procedure_text.setPlainText(row['comments_procedure'])
                self.endoscopist_entry.setText(row['endoscopist'])

                # Load images
                self.load_image('signature', row['signature'])
                self.load_image('picture1', row['picture1'])
                self.load_image('picture2', row['picture2'])
                self.load_image('picture3', row['picture3'])
                self.load_image('picture4', row['picture4'])

                # Show success message
                self.show_message("Success", "Data fetched successfully!")
            else:
                self.show_message("Not Found", "No data found for the provided Bill No.")
        except mysql.connector.Error as err:
            self.show_message("Error", f"Error: {err}")


    def load_image(self, image_type, image_path):
        # Ensure image_path is a string
        if isinstance(image_path, bytes):
            image_path = image_path.decode('utf-8')

        if image_path:
            full_path = image_path
            print(f"Attempting to load image from: {full_path}")  # Print full path for debugging

            if os.path.exists(full_path):
                try:
                    image = QImage(full_path)
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
                    
                    # Update the appropriate image label
                    if image_type == 'signature':
                        self.signature_image.setPixmap(pixmap)
                    elif image_type == 'picture1':
                        self.picture1_image.setPixmap(pixmap)
                    elif image_type == 'picture2':
                        self.picture2_image.setPixmap(pixmap)
                    elif image_type == 'picture3':
                        self.picture3_image.setPixmap(pixmap)
                    elif image_type == 'picture4':
                        self.picture4_image.setPixmap(pixmap)
                    else:
                        self.show_message("Warning", f"Unknown image type: {image_type}.")
                except Exception as e:
                    self.show_message("Error", f"Error loading image: {e}")
            else:
                self.show_message("Warning", f"Image file does not exist at: {full_path}.")
        else:
            self.show_message("Warning", f"No image path provided for {image_type}.")

    def show_message(self, title, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, title, message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
