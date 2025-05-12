import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QLineEdit, QFormLayout, QHBoxLayout, QMessageBox,
                             QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class EditViewer(QWidget):
    viewer_added = pyqtSignal(dict)

    def __init__(self, movies, sessions):
        super().__init__()
        self.movies = movies
        self.sessions = sessions
        self.first_name_edit = None
        self.last_name_edit = None
        self.row_edit = None
        self.seat_edit = None
        self.movie_combo = None
        self.session_combo = None
        self.feedback_label = None
        with open("styles.css", "r") as styleFile:
            self.setStyleSheet(styleFile.read())
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(400, 250)
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

        self.row_edit = QLineEdit()
        self.row_edit.setPlaceholderText("Ряд")

        self.seat_edit = QLineEdit()
        self.seat_edit.setPlaceholderText("Місце")

        self.movie_combo = QComboBox()
        self.movie_combo.addItem("-")
        self.movie_combo.addItems(self.movies)

        self.session_combo = QComboBox()
        self.session_combo.addItem("-")
        self.session_combo.addItems(self.sessions)

        self.feedback_label = QLabel()

        submit_button = QPushButton("Зберегти")
        submit_button.setMaximumWidth(140)
        submit_button.clicked.connect(self.saveViewerInfo)

        submit_h_box = QHBoxLayout()
        submit_h_box.addWidget(self.feedback_label)
        submit_h_box.addWidget(submit_button)

        main_form = QFormLayout()

        main_form.addRow(header_label)
        main_form.addRow("Ім'я та прізвище", name_h_box)
        main_form.addRow("Ряд", self.row_edit)
        main_form.addRow("Місце", self.seat_edit)
        main_form.addRow("Фільм", self.movie_combo)
        main_form.addRow("Сеанс", self.session_combo)
        main_form.addRow(submit_h_box)

        self.setLayout(main_form)

    def saveViewerInfo(self):
        first_name = self.first_name_edit.text().strip()
        last_name = self.last_name_edit.text().strip()
        row = self.row_edit.text().strip()
        seat = self.seat_edit.text().strip()
        movie = self.movie_combo.currentText()
        session = self.session_combo.currentText()

        if not first_name or not last_name:
            self.feedback_label.setText("Пропущено ім'я або прізвище.")
        else:
            viewer_data = {
                'name': f"{first_name} {last_name}",
                'row': row if row else '-',
                'seat': seat if seat else '-',
                'movie': movie if movie != "-" else "-",
                'session': session if session != "-" else "-"
            }
            self.viewer_added.emit(viewer_data)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditViewer(movies=["Фільм 1", "Фільм 2"], sessions=["Сеанс A", "Сеанс B"])
    window.show()
    sys.exit(app.exec())