import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QDateEdit, QLineEdit, QTextEdit, QComboBox,
                             QFormLayout, QHBoxLayout, QMessageBox)

from PyQt6.QtCore import Qt, QDate, QRegularExpression
from PyQt6.QtGui import QFont, QRegularExpressionValidator, QPixmap


class EditTicket(QWidget):

    def __init__(self):
        super().__init__()
        with open("styles.css", "r") as styleFile:
            self.setStyleSheet(styleFile.read())
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(600, 500)
        self.setWindowTitle("Оберіть місце")
        self.setUpMainWindow()

    def setUpMainWindow(self):

        header_label = QLabel("Оберіть місце")
        header_label.setFont(QFont("Arial", 18))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cinema_scheme_label = QLabel()
        pixmap = QPixmap('images/cinema.png')  
        cinema_scheme_label.setPixmap(pixmap.scaledToWidth(580))
        cinema_scheme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        instruction_label = QLabel("Оберіть ряд та місце (наприклад: 1, 1)")
        self.seat_input = QLineEdit()
        self.seat_input.setPlaceholderText("Ряд, Місце")

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
        main_form.addRow(cinema_scheme_label)
        main_form.addRow(instruction_label, self.seat_input)
        main_form.addRow(QLabel("Додаткова інформація"))
        main_form.addRow(self.extra_info_tedit)
        main_form.addRow(submit_h_box)

        self.setLayout(main_form)


    def createNewClient(self):
        seat_text = self.seat_input.text()
        if not seat_text:
            self.feedback_label.setText("Будь ласка, оберіть ряд та місце.")
            return

        parts = seat_text.split(',')
        if len(parts) != 2:
            self.feedback_label.setText("Неправильний формат введення. Введіть 'ряд, місце'.")
            return

        try:
            row, seat = map(str.strip, parts)
            self.row = row  
            self.seat = seat  
            QMessageBox.information(self, "Обрано місце",
                                        f"Ви обрали ряд: {row}, місце: {seat}")
            self.close()
        except ValueError:
            self.feedback_label.setText("Будь ласка, введіть числа для ряду та місця.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditTicket()
    window.show()
    sys.exit(app.exec())