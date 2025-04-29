import sys
import pickle
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QInputDialog, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from edit_ticket import EditTicket
from edit_viewer import EditViewer

DATA_FILE = "data.pkl"
MOVIES_FILE = "movies.pkl"
SESSIONS_FILE = "sessions.pkl"

def load_data(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return []

def save_data(file, data):
    with open(file, "wb") as f:
        pickle.dump(data, f)


class UserTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open("styles.css", "r") as styleFile:
            self.setStyleSheet(styleFile.read())
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Вибір користувача")
        self.setMinimumSize(300, 200)

        label = QLabel("Ви глядач чи менеджер?", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        viewer_button = QPushButton("Глядач")
        manager_button = QPushButton("Менеджер")

        viewer_button.clicked.connect(self.openViewerForm)
        manager_button.clicked.connect(self.openManagerWindow)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(viewer_button)
        layout.addWidget(manager_button)

        self.setLayout(layout)

    def openViewerForm(self):
        self.name_input = QLineEdit()
        dialog = QWidget()
        dialog.setWindowTitle("Введіть ім’я")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введіть ваше ім’я та прізвище:"))
        layout.addWidget(self.name_input)
        confirm_button = QPushButton("Продовжити")
        layout.addWidget(confirm_button)
        dialog.setLayout(layout)

        confirm_button.clicked.connect(lambda: self.launchViewer(dialog))
        dialog.setFixedSize(300, 150)
        dialog.show()
        self.name_dialog = dialog

    def launchViewer(self, dialog):
        name = self.name_input.text().strip()
        if name:
            self.main_window = MainWindow(role='viewer', viewer_name=name)
            self.main_window.show()
            dialog.close()
            self.close()

    def openManagerWindow(self):
        password, ok = QInputDialog.getText(self, 'Пароль менеджера', 'Введіть пароль:')
        if ok and password == 'admin123':
            self.main_window = MainWindow(role='manager')
            self.main_window.show()
            self.close()
        else:
            error = QLabel("Невірний пароль. Спробуйте ще раз.", self)
            error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout().addWidget(error)


class MainWindow(QWidget):
    def __init__(self, role, viewer_name=""):
        super().__init__()
        with open("styles.css", "r") as styleFile:
            self.setStyleSheet(styleFile.read())
        self.role = role
        self.viewer_name = viewer_name
        self.ticket_data = load_data(DATA_FILE)
        self.movies = load_data(MOVIES_FILE)
        self.sessions = load_data(SESSIONS_FILE)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Кінотеатр - Головне вікно")
        self.setMinimumSize(600, 400)
        self.setUpMainWindow()

    def setUpMainWindow(self):
        self.tab_bar = QTabWidget(self)

        if self.role == 'viewer':
            self.tickets_tab = QWidget()
            self.tab_bar.addTab(self.tickets_tab, "Купити квиток")
            self.ticketsTab()

        elif self.role == 'manager':
            self.viewers_tab = QWidget()
            self.sessions_tab = QWidget()
            self.movies_tab = QWidget()

            self.tab_bar.addTab(self.viewers_tab, "Глядачі")
            self.tab_bar.addTab(self.sessions_tab, "Сеанси")
            self.tab_bar.addTab(self.movies_tab, "Фільми")

            self.viewersTab()
            self.sessionsTab()
            self.moviesTab()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tab_bar)
        self.setLayout(main_layout)

    def ticketsTab(self):
        layout = QVBoxLayout()

        cinema_image = QLabel()
        pixmap = QPixmap("images/popcorn.png")
        cinema_image.setPixmap(pixmap.scaledToWidth(300))
        cinema_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie_box = QComboBox()
        self.movie_box.addItems(self.movies if self.movies else ['Титанік', 'Аватар'])

        self.session_box = QComboBox()
        self.session_box.addItems(self.sessions if self.sessions else ['Сеанс 1', 'Сеанс 2'])

        button_buy_ticket = QPushButton("Купити квиток")
        button_buy_ticket.clicked.connect(self.openEditTicketWindow)

        layout.addWidget(cinema_image)
        layout.addWidget(QLabel("Фільм:"))
        layout.addWidget(self.movie_box)
        layout.addWidget(QLabel("Сеанс:"))
        layout.addWidget(self.session_box)
        layout.addWidget(button_buy_ticket)
        self.tickets_tab.setLayout(layout)

    def openEditTicketWindow(self):
        self.edit_ticket_window = EditTicket()
        self.edit_ticket_window.show()
        self.edit_ticket_window.destroyed.connect(self.saveTicketInfo)

    def saveTicketInfo(self):
        row = getattr(self.edit_ticket_window, 'row', '-')
        seat = getattr(self.edit_ticket_window, 'seat', '-')
        self.ticket_data.append({
            'name': self.viewer_name,
            'row': row,
            'seat': seat,
            'movie': self.movie_box.currentText(),
            'session': self.session_box.currentText()
        })
        save_data(DATA_FILE, self.ticket_data)

    def sessionsTab(self):
        self.sessions_list = QListWidget()
        self.sessions_list.addItems(self.sessions)

        button_add_session = QPushButton('Додати сеанс')
        button_add_session.clicked.connect(self.addSession)
        button_delete_session = QPushButton('Видалити сеанс')
        button_delete_session.clicked.connect(lambda: self.deleteSelectedItem(self.sessions_list, SESSIONS_FILE, self.sessions))

        layout = QVBoxLayout()
        layout.addWidget(self.sessions_list)
        layout.addWidget(button_add_session)
        layout.addWidget(button_delete_session)
        self.sessions_tab.setLayout(layout)

    def moviesTab(self):
        self.movies_list = QListWidget()
        self.movies_list.addItems(self.movies)

        button_add_movie = QPushButton('Додати фільм')
        button_add_movie.clicked.connect(self.addMovie)
        button_delete_movie = QPushButton('Видалити фільм')
        button_delete_movie.clicked.connect(lambda: self.deleteSelectedItem(self.movies_list, MOVIES_FILE, self.movies))

        layout = QVBoxLayout()
        layout.addWidget(self.movies_list)
        layout.addWidget(button_add_movie)
        layout.addWidget(button_delete_movie)
        self.movies_tab.setLayout(layout)

    def viewersTab(self):
        self.viewers_list = QListWidget()
        for ticket in self.ticket_data:
            text = f"{ticket['name']} - {ticket['row']} ряд, {ticket['seat']} місце \"{ticket['movie']}\" - {ticket['session']}"
            self.viewers_list.addItem(QListWidgetItem(text))

        button_add_viewer = QPushButton('Додати глядача')
        button_add_viewer.clicked.connect(self.openEditViewerWindow)
        button_delete_viewer = QPushButton('Видалити глядача')
        button_delete_viewer.clicked.connect(self.deleteSelectedViewer)

        layout = QVBoxLayout()
        layout.addWidget(self.viewers_list)
        layout.addWidget(button_add_viewer)
        layout.addWidget(button_delete_viewer)
        self.viewers_tab.setLayout(layout)

    def deleteSelectedViewer(self):
        item = self.viewers_list.currentItem()
        if item:
            row = self.viewers_list.currentRow()
            self.viewers_list.takeItem(row)
            if 0 <= row < len(self.ticket_data):
                del self.ticket_data[row]
                save_data(DATA_FILE, self.ticket_data)

    def openEditViewerWindow(self):
        self.edit_viewer_window = EditViewer()
        self.edit_viewer_window.show()
        self.edit_viewer_window.destroyed.connect(self.refreshViewersListFromForm)

    def refreshViewersListFromForm(self):
        if hasattr(self.edit_viewer_window, 'first_name_edit') and hasattr(self.edit_viewer_window, 'last_name_edit'):
            first_name = self.edit_viewer_window.first_name_edit.text().strip()
            last_name = self.edit_viewer_window.last_name_edit.text().strip()
            full_name = f"{first_name} {last_name}"
            if full_name:
                new_data = {
                    'name': full_name,
                    'row': '-', 'seat': '-', 'movie': '-', 'session': '-'
                }
                self.ticket_data.append(new_data)
                save_data(DATA_FILE, self.ticket_data)
                self.viewers_list.addItem(QListWidgetItem(
                    f"{new_data['name']} - {new_data['row']} ряд, {new_data['seat']} місце \"{new_data['movie']}\" - {new_data['session']}"))

    def addSession(self):
        text, ok = QInputDialog.getText(self, 'Новий сеанс', 'Введіть опис сеансу:')
        if ok and text:
            self.sessions.append(text)
            self.sessions_list.addItem(QListWidgetItem(text))
            save_data(SESSIONS_FILE, self.sessions)

    def addMovie(self):
        text, ok = QInputDialog.getText(self, 'Новий фільм', 'Введіть назву фільму:')
        if ok and text:
            self.movies.append(text)
            self.movies_list.addItem(QListWidgetItem(text))
            save_data(MOVIES_FILE, self.movies)

    def deleteSelectedItem(self, list_widget, filename, data_list):
        item = list_widget.currentItem()
        if item:
            text = item.text()
            row = list_widget.currentRow()
            list_widget.takeItem(row)
            if text in data_list:
                data_list.remove(text)
                save_data(filename, data_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserTypeWindow()
    window.show()
    sys.exit(app.exec())
