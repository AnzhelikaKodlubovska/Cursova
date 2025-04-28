import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from edit_manager import EditManager
from edit_ticket import EditTicket
from edit_viewer import EditViewer


class UserTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Вибір користувача")
        self.setMinimumSize(300, 200)

        label = QLabel("Ви глядач чи менеджер?", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        viewer_button = QPushButton("Глядач")
        manager_button = QPushButton("Менеджер")

        viewer_button.clicked.connect(self.openViewerWindow)
        manager_button.clicked.connect(self.openManagerWindow)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(viewer_button)
        layout.addWidget(manager_button)

        self.setLayout(layout)

    def openViewerWindow(self):
        self.main_window = MainWindow(role='viewer')
        self.main_window.show()
        self.close()

    def openManagerWindow(self):
        self.main_window = MainWindow(role='manager')
        self.main_window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Кінотеатр - Головне вікно")
        self.setMinimumSize(600, 400)
        self.setUpMainWindow()

    def setUpMainWindow(self):
        self.tab_bar = QTabWidget(self)

        if self.role == 'viewer':
            self.tickets_tab = QWidget()
            self.sessions_tab = QWidget()
            self.movies_tab = QWidget()

            self.tab_bar.addTab(self.tickets_tab, "Квитки")
            self.tab_bar.addTab(self.sessions_tab, "Сеанси")
            self.tab_bar.addTab(self.movies_tab, "Фільми")

            self.ticketsTab()
            self.sessionsTab()
            self.moviesTab()

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
        pixmap = QPixmap("images/cinema1.png")
        cinema_image.setPixmap(pixmap.scaledToWidth(500))
        cinema_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_buy_ticket = QPushButton("Купити квиток")
        button_buy_ticket.clicked.connect(self.openEditTicketWindow)

        layout.addWidget(cinema_image)
        layout.addWidget(button_buy_ticket)
        self.tickets_tab.setLayout(layout)

    def openEditTicketWindow(self):
        self.edit_ticket_window = EditTicket()
        self.edit_ticket_window.show()

    def sessionsTab(self):
        self.sessions_list = QListWidget()
        self.sessions_list.addItems(['Сеанс 1: 18:00', 'Сеанс 2: 20:30'])

        if self.role == 'manager':
            button_add_session = QPushButton('Додати сеанс')
            button_add_session.clicked.connect(self.addSession)

            layout = QVBoxLayout()
            layout.addWidget(self.sessions_list)
            layout.addWidget(button_add_session)
            self.sessions_tab.setLayout(layout)
        else:
            layout = QVBoxLayout()
            layout.addWidget(self.sessions_list)
            self.sessions_tab.setLayout(layout)

    def moviesTab(self):
        self.movies_list = QListWidget()
        self.movies_list.addItems(['Аватар', 'Титанік'])

        if self.role == 'manager':
            button_add_movie = QPushButton('Додати фільм')
            button_add_movie.clicked.connect(self.addMovie)

            layout = QVBoxLayout()
            layout.addWidget(self.movies_list)
            layout.addWidget(button_add_movie)
            self.movies_tab.setLayout(layout)
        else:
            layout = QVBoxLayout()
            layout.addWidget(self.movies_list)
            self.movies_tab.setLayout(layout)

    def viewersTab(self):
        self.viewers_list = QListWidget()
        self.viewers_list.addItems(['Іван', 'Олена'])

        button_add_viewer = QPushButton('Додати глядача')
        button_add_viewer.clicked.connect(self.openEditViewerWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.viewers_list)
        layout.addWidget(button_add_viewer)
        self.viewers_tab.setLayout(layout)

    def openEditViewerWindow(self):
        self.edit_viewer_window = EditViewer()
        self.edit_viewer_window.show()
        self.edit_viewer_window.destroyed.connect(self.refreshViewersList)

    def refreshViewersList(self):
        self.viewers_list.addItem(QListWidgetItem("Новий глядач"))

    def addSession(self):
        text, ok = QInputDialog.getText(self, 'Новий сеанс', 'Введіть опис сеансу:')
        if ok and text:
            self.sessions_list.addItem(QListWidgetItem(text))

    def addMovie(self):
        text, ok = QInputDialog.getText(self, 'Новий фільм', 'Введіть назву фільму:')
        if ok and text:
            self.movies_list.addItem(QListWidgetItem(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserTypeWindow()
    window.show()
    sys.exit(app.exec())
