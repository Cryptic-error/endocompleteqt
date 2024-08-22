from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDateEdit
from PyQt5.QtGui import QPixmap
import mysql.connector
from PIL import Image
import io
import os
from fpdf import FPDF

class EndoscopyForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
      

    
        self.setWindowTitle("Endoscopy Form")
        self.setGeometry(100, 100, 1100, 800)

        # Scroll Area for the form
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, 1100, 800)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area_content = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.scroll_area_content)
        self.scroll_area_content.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        # Header Frame
        self.header_frame = QtWidgets.QGroupBox("Header")
        self.header_layout = QtWidgets.QGridLayout()
        self.header_frame.setLayout(self.header_layout)
        self.scroll_area_layout.addWidget(self.header_frame)

        # Load the letterhead image


# Load the image
        letterhead_image_path = "subha swastik.jpg"
        letterhead_image = QtGui.QPixmap(letterhead_image_path)

        # Resize the image to 200x200 pixels
        letterhead_image = letterhead_image.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        # Create a QLabel to display the image
        letterhead_label = QtWidgets.QLabel(self.header_frame)
        letterhead_label.setPixmap(letterhead_image)

        # Set the fixed size of the QLabel to 200x200 pixels
        letterhead_label.setFixedSize(200, 200)

        # Add the QLabel to the layout
        self.header_layout.addWidget(letterhead_label, 0, 0, 3, 1)


        # Header Texts
        self.large_header = QtWidgets.QLabel("Subha Swastik Hospital PVT LTD", self.header_frame)
        self.large_header.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold))
        self.header_layout.addWidget(self.large_header, 0, 1)

        self.medium_header1 = QtWidgets.QLabel("Bardibas-14, Mahottari", self.header_frame)
        self.medium_header1.setFont(QtGui.QFont("Helvetica", 16))
        self.header_layout.addWidget(self.medium_header1, 1, 1)

        self.medium_header2 = QtWidgets.QLabel("Report of Sigmoidoscopy/Colonoscopy", self.header_frame)
        self.medium_header2.setFont(QtGui.QFont("Helvetica", 16))
        self.header_layout.addWidget(self.medium_header2, 2, 1)

        # Form fields
        form_layout = QtWidgets.QGridLayout()

        form_layout.addWidget(QtWidgets.QLabel("Name:"), 0, 0)
        self.entry_name = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_name, 0, 1)

        form_layout.addWidget(QtWidgets.QLabel("Bill No:"), 0, 2)
        self.entry_bill_no = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_bill_no, 0, 3)

        form_layout.addWidget(QtWidgets.QLabel("Age:"), 0, 4)
        self.entry_age = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_age, 0, 5)

        form_layout.addWidget(QtWidgets.QLabel("Sex:"), 1, 2)
        self.sex_var = QtWidgets.QComboBox()
        self.sex_var.addItems(["Male", "Female", "Other"])
        form_layout.addWidget(self.sex_var, 1, 3)

        form_layout.addWidget(QtWidgets.QLabel("Phone No:"), 1, 4)
        self.entry_phone_no = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_phone_no, 1, 5)

        form_layout.addWidget(QtWidgets.QLabel("Referred By:"), 1, 0)
        self.entry_referred_by = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_referred_by, 1, 1)

        form_layout.addWidget(QtWidgets.QLabel("Indication:"), 2, 0)
        self.entry_indication = QtWidgets.QTextEdit()
        form_layout.addWidget(self.entry_indication, 2, 1, 1, 3)

        form_layout.addWidget(QtWidgets.QLabel("Date:"), 2, 4)
        self.entry_date = QDateEdit() 
        form_layout.addWidget(self.entry_date, 2, 5)

        form_layout.addWidget(QtWidgets.QLabel("Anus:"), 3, 0)
        self.anus_var = QtWidgets.QComboBox()
        self.anus_var.addItems(["Normal", "Abnormal"])
        form_layout.addWidget(self.anus_var, 3, 1)

        form_layout.addWidget(QtWidgets.QLabel("Rectum:"), 3, 2)
        self.entry_rectum = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_rectum, 3, 3)

        form_layout.addWidget(QtWidgets.QLabel("Sigmoid Colon:"), 4, 0)
        self.entry_sigmoid_colon = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_sigmoid_colon, 4, 1)

        form_layout.addWidget(QtWidgets.QLabel("Descending Colon:"), 4, 2)
        self.entry_descending_colon = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_descending_colon, 4, 3)

        form_layout.addWidget(QtWidgets.QLabel("Transverse Colon:"), 5, 0)
        self.entry_transverse_colon = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_transverse_colon, 5, 1)

        form_layout.addWidget(QtWidgets.QLabel("Ascending Colon:"), 5, 2)
        self.entry_ascending_colon = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_ascending_colon, 5, 3)

        form_layout.addWidget(QtWidgets.QLabel("Caecum:"), 5, 4)
        self.entry_caecum = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_caecum, 5, 5)

        form_layout.addWidget(QtWidgets.QLabel("Diagnosis:"), 6, 0)
        self.entry_diagnosis = QtWidgets.QTextEdit()
        form_layout.addWidget(self.entry_diagnosis, 6, 1, 1, 3)

        form_layout.addWidget(QtWidgets.QLabel("Comments Procedure:"), 7, 0)
        self.entry_comments_procedure = QtWidgets.QTextEdit()
        form_layout.addWidget(self.entry_comments_procedure, 7, 1, 1, 3)

        form_layout.addWidget(QtWidgets.QLabel("Endoscopist:"), 8, 0)
        self.entry_endoscopist = QtWidgets.QLineEdit()
        form_layout.addWidget(self.entry_endoscopist, 8, 1)

        self.scroll_area_layout.addLayout(form_layout)

     # Signature and Pictures Upload Layout
        upload_layout = QtWidgets.QGridLayout()

        # Upload Signature Button
        self.upload_signature_btn = QtWidgets.QPushButton("Upload Signature")
        self.upload_signature_btn.clicked.connect(lambda: self.upload_image('signature'))
        upload_layout.addWidget(self.upload_signature_btn, 0, 0)

        # Display for Signature
        self.signature_label = QtWidgets.QLabel()
        upload_layout.addWidget(self.signature_label, 0, 1)

        # Upload Picture Buttons and Displays
        # 1st Picture
        self.upload_picture1_btn = QtWidgets.QPushButton("Upload Picture 1")
        self.upload_picture1_btn.clicked.connect(lambda: self.upload_image('picture1'))
        upload_layout.addWidget(self.upload_picture1_btn, 1, 0)

        self.picture1_label = QtWidgets.QLabel()
        upload_layout.addWidget(self.picture1_label, 1, 1)

        # 2nd Picture
        self.upload_picture2_btn = QtWidgets.QPushButton("Upload Picture 2")
        self.upload_picture2_btn.clicked.connect(lambda: self.upload_image('picture2'))
        upload_layout.addWidget(self.upload_picture2_btn, 2, 0)

        self.picture2_label = QtWidgets.QLabel()
        upload_layout.addWidget(self.picture2_label, 2, 1)

        # 3rd Picture
        self.upload_picture3_btn = QtWidgets.QPushButton("Upload Picture 3")
        self.upload_picture3_btn.clicked.connect(lambda: self.upload_image('picture3'))
        upload_layout.addWidget(self.upload_picture3_btn, 3, 0)

        self.picture3_label = QtWidgets.QLabel()
        upload_layout.addWidget(self.picture3_label, 3, 1)

        # 4th Picture
        self.upload_picture4_btn = QtWidgets.QPushButton("Upload Picture 4")
        self.upload_picture4_btn.clicked.connect(lambda: self.upload_image('picture4'))
        upload_layout.addWidget(self.upload_picture4_btn, 4, 0)

        self.picture4_label = QtWidgets.QLabel()
        upload_layout.addWidget(self.picture4_label, 4, 1)

        # Add upload layout to main layout
        self.scroll_area_layout.addLayout(upload_layout)

        # Initialize image placeholders
        self.signature_image = None
        self.picture1_image = None
        self.picture2_image = None
        self.picture3_image = None
        self.picture4_image = None

        self.save_data_btn = QtWidgets.QPushButton("SAVEFORM")
        self.save_data_btn.clicked.connect(self.save_data)
        self.scroll_area_layout.addWidget(self.save_data_btn)

        self.generate_pdf_btn = QtWidgets.QPushButton("Generate PDF")
        self.generate_pdf_btn.clicked.connect(self.generate_pdf)
        self.scroll_area_layout.addWidget(self.generate_pdf_btn)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())

    def save_data(self):
        user_name = self.entry_name.text().replace(" ", "_")
        bill =  self.entry_bill_no.text().replace(" ", "_")
        image_dir = os.path.join('saved_images', user_name + bill)
        os.makedirs(image_dir, exist_ok=True)

        # Prepare data, replacing missing fields with None or empty strings
        data = {
            'bill_no': self.entry_bill_no.text() or None,
            'name': self.entry_name.text() or None,
            'age': self.entry_age.text() or None,
            'sex': self.sex_var.currentText() or None,
            'phone_no': self.entry_phone_no.text() or None,
            'referred_by': self.entry_referred_by.text() or None,
            'indication': self.entry_indication.toPlainText() or None,
            'date': self.entry_date.date().toString('yyyy-MM-dd') or None,
            'anus': self.anus_var.currentText() or None,
            'rectum': self.entry_rectum.text() or None,
            'sigmoid_colon': self.entry_sigmoid_colon.text() or None,
            'descending_colon': self.entry_descending_colon.text() or None,
            'transverse_colon': self.entry_transverse_colon.text() or None,
            'ascending_colon': self.entry_ascending_colon.text() or None,
            'caecum': self.entry_caecum.text() or None,
            'diagnosis': self.entry_diagnosis.toPlainText() or None,
            'comments_procedure': self.entry_comments_procedure.toPlainText() or None,
            'signature': self.save_image(self.signature_image, os.path.join(image_dir, 'signature.jpg')) or None,
            'endoscopist': self.entry_endoscopist.text() or None,
            'picture1': self.save_image(self.picture1_image, os.path.join(image_dir, 'picture1.jpg')) or None,
            'picture2': self.save_image(self.picture2_image, os.path.join(image_dir, 'picture2.jpg')) or None,
            'picture3': self.save_image(self.picture3_image, os.path.join(image_dir, 'picture3.jpg')) or None,
            'picture4': self.save_image(self.picture4_image, os.path.join(image_dir, 'picture4.jpg')) or None
        }

        # Create SQL placeholders and corresponding values
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ilovenepal123",
                database="endoscopy"
            )
            cursor = conn.cursor()

            # Debugging output
            print("Number of values:", len(values))
            print("Values:", values)

            # Execute the insert statement
            cursor.execute(
                f"INSERT INTO endoscopy_form ({columns}) VALUES ({placeholders})",
                values
            )

            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Success", "Data saved successfully.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error: {err}")


    def save_image(self, image, path):
        if image:
            image.save(path)
            return path
        return None

    def upload_image(self, image_type):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            image = Image.open(file_path)
            q_image = QPixmap.fromImage(QtGui.QImage(image.tobytes(), image.width, image.height, image.width * 3, QtGui.QImage.Format_RGB888))
            if image_type == 'signature':
                self.signature_image = image
                self.signature_label.setPixmap(q_image)
            elif image_type == 'picture1':
                self.picture1_image = image
                self.picture1_label.setPixmap(q_image)
            elif image_type == 'picture2':
                self.picture2_image = image
                self.picture2_label.setPixmap(q_image)
            elif image_type == 'picture3':
                self.picture3_image = image
                self.picture3_label.setPixmap(q_image)
            elif image_type == 'picture4':
                self.picture4_image = image
                self.picture4_label.setPixmap(q_image)



    

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        # Set header image
        header_image_path = "subha swastik.jpg"  # Path to the header image
        if os.path.exists(header_image_path):
            pdf.image(header_image_path, x=10, y=10, w=50)  # Adjust x, y, and w as needed

        # Set title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Endoscopy Report", 0, 1, 'C')
        pdf.ln(10)

        # Add header text
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Subha Swastik Hospital PVT LTD", 0, 1, 'C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "Bardibas-14, Mahottari", 0, 1, 'C')
        pdf.cell(0, 10, "Report of Sigmoidoscopy/Colonoscopy", 0, 1, 'C')
        pdf.ln(10)

        # Add form data
        pdf.set_font("Arial", size=12)
        form_data = {
            'Bill No': self.entry_bill_no.text(),
            'Name': self.entry_name.text(),
            'Age': self.entry_age.text(),
            'Sex': self.sex_var.currentText(),
            'Phone No': self.entry_phone_no.text(),
            'Referred By': self.entry_referred_by.text(),
            'Indication': self.entry_indication.toPlainText(),
            'Date': self.entry_date.text(),
            'Anus': self.anus_var.currentText(),
            'Rectum': self.entry_rectum.text(),
            'Sigmoid Colon': self.entry_sigmoid_colon.text(),
            'Descending Colon': self.entry_descending_colon.text(),
            'Transverse Colon': self.entry_transverse_colon.text(),
            'Ascending Colon': self.entry_ascending_colon.text(),
            'Caecum': self.entry_caecum.text(),
            'Diagnosis': self.entry_diagnosis.toPlainText(),
            'Comments Procedure': self.entry_comments_procedure.toPlainText(),
            'Endoscopist': self.entry_endoscopist.text()
        }

        pdf.set_fill_color(200, 220, 255)
        col_width = pdf.get_string_width('Comments Procedure:') + 10

        for key, value in form_data.items():
            # Check if adding this content will overflow the page
            if pdf.get_y() > 270 - 10:  # Adjust the threshold based on your layout needs
                pdf.add_page()
            pdf.cell(col_width, 10, f"{key}:", border=1, fill=True)
            pdf.cell(0, 10, value, border=1, ln=True)

        # Construct the folder name and path with underscores instead of spaces
        folder_name = f"{self.entry_name.text().replace(' ', '_')}{self.entry_bill_no.text()}"
        signature_path = os.path.join('saved_images', folder_name, 'signature.jpg')
        print(signature_path)

        # Add the signature image
        if os.path.exists(signature_path):
            # Check if adding this image will overflow the page
            if pdf.get_y() + 60 > 270:  # Adjust based on the height of the image
                pdf.add_page()
            pdf.ln(10)  # Add a line break before the image
            pdf.image(signature_path, x=10, y=pdf.get_y(), w=100)
            pdf.ln(60)  # Add some space after the image

        # Add the four images
        image_paths = [
            os.path.join('saved_images', folder_name, 'picture1.jpg'),
            os.path.join('saved_images', folder_name, 'picture2.jpg'),
            os.path.join('saved_images', folder_name, 'picture3.jpg'),
            os.path.join('saved_images', folder_name, 'picture4.jpg')
        ]

        for image_path in image_paths:
            if os.path.exists(image_path):
                # Check if adding this image will overflow the page
                if pdf.get_y() + 60 > 270:  # Adjust based on the height of the image
                    pdf.add_page()
                pdf.ln(10)  # Add a line break before the image
                pdf.image(image_path, x=10, y=pdf.get_y(), w=100)
                pdf.ln(150)  # Add some space after each image

        # Save the PDF
        output_path = os.path.join('saved_pdfs', f"{self.entry_bill_no.text()}.pdf")
        pdf.output(output_path)

        # Save PDF with a properly formatted file name
        pdf_output_path = os.path.join('saved_pdfs', f"{self.entry_name.text().replace(' ', '_')}_endoscopy_form.pdf")
        os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)
        pdf.output(pdf_output_path)
        QtWidgets.QMessageBox.information(self, "PDF Generated", f"PDF saved as {pdf_output_path}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    window = EndoscopyForm()
    window.show()
    sys.exit(app.exec_())
