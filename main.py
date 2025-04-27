import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QTabWidget,
                             QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QInputDialog)
from PyQt6.QtCore import Qt


class CinemaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Облік квитків у кінотеатрі")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        tab_bar = QTabWidget(self)

        self.audience_tab = QWidget()
        self.tickets_tab = QWidget()
        self.sessions_tab = QWidget()
        self.movies_tab = QWidget()
        self.managers_tab = QWidget()

        tab_bar.addTab(self.audience_tab, "Глядачі")
        tab_bar.addTab(self.tickets_tab, "Квитки")
        tab_bar.addTab(self.sessions_tab, "Сеанси")
        tab_bar.addTab(self.movies_tab, "Фільми")
        tab_bar.addTab(self.managers_tab, "Менеджери")

        self.audienceTab()
        self.ticketsTab()
        self.sessionsTab()
        self.moviesTab()
        self.managersTab()

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(tab_bar)
        self.setLayout(main_h_box)

    def audienceTab(self):
        self.audience_list = ['Іван', 'Олена', 'Дмитро']
        self.audience_list_widget = QListWidget()
        for audience in self.audience_list:
            self.audience_list_widget.addItem(QListWidgetItem(audience))

        button_add_audience = QPushButton('Додати глядача')
        button_add_audience.clicked.connect(self.addAudienceClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.audience_list_widget)
        tab_v_box.addWidget(button_add_audience)
        self.audience_tab.setLayout(tab_v_box)

    def addAudienceClicked(self):
        name, ok = QInputDialog.getText(self, 'Новий глядач', "Введіть ім'я глядача:")
        if ok and name:
            self.audience_list.append(name)
            self.audience_list_widget.addItem(QListWidgetItem(name))

    def ticketsTab(self):
        self.tickets_list = ['Квиток #001', 'Квиток #002', 'Квиток #003']
        self.tickets_list_widget = QListWidget()
        for ticket in self.tickets_list:
            self.tickets_list_widget.addItem(QListWidgetItem(ticket))

        button_add_ticket = QPushButton('Додати квиток')
        button_add_ticket.clicked.connect(self.addTicketClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.tickets_list_widget)
        tab_v_box.addWidget(button_add_ticket)
        self.tickets_tab.setLayout(tab_v_box)

    def addTicketClicked(self):
        ticket, ok = QInputDialog.getText(self, 'Новий квиток', 'Введіть номер квитка:')
        if ok and ticket:
            self.tickets_list.append(ticket)
            self.tickets_list_widget.addItem(QListWidgetItem(ticket))

    def sessionsTab(self):
        self.sessions_list = ['Сеанс 1: 18:00', 'Сеанс 2: 20:30']
        self.sessions_list_widget = QListWidget()
        for session in self.sessions_list:
            self.sessions_list_widget.addItem(QListWidgetItem(session))

        button_add_session = QPushButton('Додати сеанс')
        button_add_session.clicked.connect(self.addSessionClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.sessions_list_widget)
        tab_v_box.addWidget(button_add_session)
        self.sessions_tab.setLayout(tab_v_box)

    def addSessionClicked(self):
        session, ok = QInputDialog.getText(self, 'Новий сеанс', 'Введіть час та назву сеансу:')
        if ok and session:
            self.sessions_list.append(session)
            self.sessions_list_widget.addItem(QListWidgetItem(session))

    def moviesTab(self):
        self.movies_list = ['Фільм "Аватар"', 'Фільм "Титанік"']
        self.movies_list_widget = QListWidget()
        for movie in self.movies_list:
            self.movies_list_widget.addItem(QListWidgetItem(movie))

        button_add_movie = QPushButton('Додати фільм')
        button_add_movie.clicked.connect(self.addMovieClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.movies_list_widget)
        tab_v_box.addWidget(button_add_movie)
        self.movies_tab.setLayout(tab_v_box)

    def addMovieClicked(self):
        movie, ok = QInputDialog.getText(self, 'Новий фільм', 'Введіть назву фільму:')
        if ok and movie:
            self.movies_list.append(movie)
            self.movies_list_widget.addItem(QListWidgetItem(movie))

    def managersTab(self):
        self.managers_list = ['Менеджер Анна', 'Менеджер Богдан']
        self.managers_list_widget = QListWidget()
        for manager in self.managers_list:
            self.managers_list_widget.addItem(QListWidgetItem(manager))

        button_add_manager = QPushButton('Додати менеджера')
        button_add_manager.clicked.connect(self.addManagerClicked)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(self.managers_list_widget)
        tab_v_box.addWidget(button_add_manager)
        self.managers_tab.setLayout(tab_v_box)

    def addManagerClicked(self):
        manager, ok = QInputDialog.getText(self, 'Новий менеджер', 'Введіть ім’я менеджера:')
        if ok and manager:
            self.managers_list.append(manager)
            self.managers_list_widget.addItem(QListWidgetItem(manager))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CinemaApp()
    sys.exit(app.exec())
