import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                               QDateEdit, QLineEdit, QTextEdit, QComboBox,
                               QFormLayout, QHBoxLayout, QMessageBox)

from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QFont, QRegularExpressionValidator


class EditViewer(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(500, 350)
        self.setWindowTitle("Додати глядача")  
        self.setUpMainWindow()

    def setUpMainWindow(self):

        header_label = QLabel("Додавання глядача")  
        header_label.setFont(QFont("Arial", 18))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Ім'я")

        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Прізвище")

        name_h_box = QHBoxLayout()
        name_h_box.addWidget(self.first_name_edit)
        name_h_box.addWidget(self.last_name_edit)

        self.phone_edit = QLineEdit()
        self.phone_edit.setInputMask("(999) 999-9999;_")
        
        self.inn_edit = QLineEdit()  
        self.inn_edit.setInputMask("0000000000")  

        self.card_number_edit = QLineEdit()  
        self.card_number_edit.setInputMask("0000 0000 0000 0000")  
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("username@domain.com")

        email_validator = QRegularExpressionValidator(
            QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            self.email_edit
        )
        self.email_edit.setValidator(email_validator)

        self.extra_info_tedit = QTextEdit()
        self.feedback_label = QLabel()

        submit_button = QPushButton("Зберегти")
        submit_button.setMaximumWidth(140)
        submit_button.clicked.connect(self.createNewClient)

        submit_h_box = QHBoxLayout()
        submit_h_box.addWidget(self.feedback_label)
        submit_h_box.addWidget(submit_button)
        
        main_form = QFormLayout()

        main_form.addRow(header_label)
        main_form.addRow("Ім'я та прізвище", name_h_box)
        main_form.addRow("Телефон", self.phone_edit)
        main_form.addRow("Номер картки", self.card_number_edit) 
        main_form.addRow("Email", self.email_edit)
        main_form.addRow(QLabel("Коментар")) 
        main_form.addRow(self.extra_info_tedit)
        main_form.addRow(submit_h_box)

        self.setLayout(main_form)
    
    
    def createNewClient(self):
        if self.first_name_edit.text() == "" or \
           self.last_name_edit.text() == "":
            self.feedback_label.setText("Пропущено ім'я або прізвище.")
        elif self.phone_edit.hasAcceptableInput() == False:
            self.feedback_label.setText("Неправильно введений номер телефону.")
        elif self.email_edit.hasAcceptableInput() == False:
            self.feedback_label.setText("Email введено невірно.")
        else:
            QMessageBox.information(self, "Повідомлення",
                                    "Дані користувача введені повністю.")
            self.close()
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditViewer()
    window.show()
    sys.exit(app.exec())
