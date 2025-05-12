import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                               QDateEdit, QLineEdit, QTextEdit, QComboBox,
                               QFormLayout, QHBoxLayout, QMessageBox, QDialog)

from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from models.models import Manager


class EditManager(QDialog):

    def __init__(self, parent=None): 
        super().__init__(parent)
        with open("styles.css", "r") as styleFile:
            self.setStyleSheet(styleFile.read())
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(500, 350)
        self.setWindowTitle("Додати менеджера")
        self.setUpMainWindow()

    def setUpMainWindow(self):

        header_label = QLabel("Додавання менеджера")
        header_label.setFont(QFont("Arial", 18))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Ім'я")

        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Прізвище")

        name_h_box = QHBoxLayout()
        name_h_box.addWidget(self.first_name_edit)
        name_h_box.addWidget(self.last_name_edit)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Чоловік", "Жінка"])

        self.birthdate_edit = QDateEdit()
        self.birthdate_edit.setDisplayFormat("yyyy/MM/dd")
        self.birthdate_edit.setMaximumDate(QDate.currentDate())
        self.birthdate_edit.setCalendarPopup(True)
        self.birthdate_edit.setDate(QDate.currentDate())

        self.phone_edit = QLineEdit()
        self.phone_edit.setInputMask("(999) 999-9999;_")
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("username@domain.com")

        email_validator = QRegularExpressionValidator(
            QRegularExpression(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
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
        main_form.addRow("Стать", self.gender_combo)
        main_form.addRow("Дата народження", self.birthdate_edit)
        main_form.addRow("Телефон", self.phone_edit)
        main_form.addRow("Email", self.email_edit)
        main_form.addRow(QLabel("Додаткова інформація"))
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
            self.accept()
            
    def getManagerData(self):
        return Manager(
            name=self.first_name_edit.text() + " " + self.last_name_edit.text(),
            gender=self.gender_combo.currentText(),
            birthdate=self.birthdate_edit.date().toString("yyyy/MM/dd"),
            phone=self.phone_edit.text(),
            email=self.email_edit.text(),
            extra_info=self.extra_info_tedit.toPlainText()
        )
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditManager()
    window.show()
    sys.exit(app.exec())
