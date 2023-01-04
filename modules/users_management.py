""" Users Management Window """
import json

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QToolButton, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDialog, QFormLayout, QLineEdit, QMessageBox)


class UsersManagementWindow(QWidget):
    """ Users Management Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # Variables
        self.btn_size = QSize(370, 60)
        self.btn_font = QFont("Lato", 12)

        self.test_list_win = None
        self.users_test_list_win = None
        self.users_tests_trial_list_win = None
        self.progress_users_trial_win = None
        self.users_list_win = None

        # ### Window config
        self.setFixedSize(400, 380)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Gestion des épreuves")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 400, 380)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons
        self.tests_list_btn = QToolButton()
        self.tests_list_btn.setText("Liste complète des épreuves")
        self.tests_list_btn.setFixedSize(self.btn_size)
        self.tests_list_btn.setFont(self.btn_font)
        self.tests_list_btn.clicked.connect(self.display_tests_list)

        self.users_tests_list_btn = QToolButton()
        self.users_tests_list_btn.setText("Liste des épreuves par candidat")
        self.users_tests_list_btn.setFixedSize(self.btn_size)
        self.users_tests_list_btn.setFont(self.btn_font)
        self.users_tests_list_btn.clicked.connect(self.display_users_tests_list)

        self.users_tests_trial_list_btn = QToolButton()
        self.users_tests_trial_list_btn.setText("Liste des épreuves par candidats\net par type d'épreuve")
        self.users_tests_trial_list_btn.setFixedSize(self.btn_size)
        self.users_tests_trial_list_btn.setFont(self.btn_font)
        self.users_tests_trial_list_btn.clicked.connect(self.display_users_tests_trial_list_win)

        self.progress_users_trial_btn = QToolButton()
        self.progress_users_trial_btn.setText("Progression par type d'épreuve\net par candidat")
        self.progress_users_trial_btn.setFixedSize(self.btn_size)
        self.progress_users_trial_btn.setFont(self.btn_font)
        self.progress_users_trial_btn.clicked.connect(self.display_progress_users_trial_win)

        self.users_list_btn = QToolButton()
        self.users_list_btn.setText("Liste des candidats")
        self.users_list_btn.setFixedSize(self.btn_size)
        self.users_list_btn.setFont(self.btn_font)
        self.users_list_btn.clicked.connect(self.display_users_list_win)

        self.main_layout.addWidget(self.tests_list_btn, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.users_tests_list_btn, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.users_tests_trial_list_btn, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.progress_users_trial_btn, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.users_list_btn, 1, Qt.AlignmentFlag.AlignCenter)

    def display_users_list_win(self):
        """ Display Users List Window """
        if self.users_list_win is not None:
            return
        else:
            self.hide()
            self.users_list_win = UsersManagementWindow.UsersListWindow(self)
            self.users_list_win.show()

    def display_progress_users_trial_win(self):
        """ Display Progress Users Trial Window """
        if self.progress_users_trial_win is not None:
            return
        else:
            self.hide()
            self.progress_users_trial_win = UsersManagementWindow.ProgressUsersTrialWindow(self)
            self.progress_users_trial_win.show()

    def display_users_tests_trial_list_win(self):
        """ Display Users Test Trial List Window """
        if self.users_tests_trial_list_win is not None:
            return
        else:
            self.hide()
            self.users_tests_trial_list_win = UsersManagementWindow.UsersTestsTrialListWindow(self)
            self.users_tests_trial_list_win.show()

    def display_users_tests_list(self):
        """ Display the tests list window """
        if self.users_test_list_win is not None:
            return
        else:
            self.hide()
            self.users_test_list_win = UsersManagementWindow.UsersTestsListWindow(self)
            self.users_test_list_win.show()

    def display_tests_list(self):
        """ Display the tests list window """
        if self.test_list_win is not None:
            return
        else:
            self.hide()
            self.test_list_win = UsersManagementWindow.TestsListWindow(self)
            self.test_list_win.show()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.users_management_win = None
        self.master.show()


    class TestsListWindow(QWidget):
        """  Test List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste complète des épreuves")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.test_list_win = None


    class UsersTestsListWindow(QWidget):
        """ Users Test List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des épreuves par candidat")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_test_list_win = None


    class UsersTestsTrialListWindow(QWidget):
        """ Users Test Trial List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des épreuves par candidats et par type d'épreuve")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_tests_trial_list_win = None


    class ProgressUsersTrialWindow(QWidget):
        """ Progress Users Trial Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Progression par type d'épreuve et par candidat")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.progress_users_trial_win = None


    class UsersListWindow(QWidget):
        """ Progress Users Trial Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            self.new_user_win = None
            self.user_item = QTableWidgetItem()
            self.users_dict = dict()
            self.user_selected = str()

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des candidats")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

            # Main Layout
            self.main_layout = QVBoxLayout()
            self.setLayout(self.main_layout)

            # Buttons Layout
            self.buttons_layout = QHBoxLayout()
            self.main_layout.addLayout(self.buttons_layout, 1)
            self.add_user_btn = QPushButton("Nouveau Candidat")
            self.remove_user = QPushButton("Modifier")
            self.edit_user = QPushButton("Supprimer")

            self.add_user_btn.clicked.connect(self.display_new_user_win)

            self.buttons_layout.addWidget(self.add_user_btn)
            self.buttons_layout.addWidget(self.remove_user)
            self.buttons_layout.addWidget(self.edit_user)
            
            # Users Table
            self.users_table = QTableWidget()
            self.users_table.setFixedSize(QSize(380, 350))
            self.users_table.setSortingEnabled(False)
            self.users_table.setColumnCount(1)
            self.users_table.horizontalHeader().setStretchLastSection(True)
            self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.header = QTableWidgetItem("Liste des Candidats")
            self.header.setFont(QFont("Lato", 12))
            self.users_table.setHorizontalHeaderItem(0, self.header)
            self.users_table.verticalHeader().setVisible(False)
            self.users_table.setAlternatingRowColors(True)
            self.users_table.clicked.connect(lambda: self.set_selected_user(self.users_table.currentItem().text()))
            # noinspection PyUnresolvedReferences
            self.users_table.activated.connect(lambda: self.set_selected_user(self.users_table.currentItem().text()))

            self.main_layout.addWidget(self.users_table, 4)

            try:
                with open("./files/users.json", "r") as users_file:
                    self.users_dict = json.load(users_file)

                count = 0
                for user in self.users_dict.keys():
                    self.user_item = QTableWidgetItem(user)
                    self.user_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.user_item.setTextAlignment(Qt.AlignCenter)
                    self.users_table.setRowCount(count + 1)
                    self.users_table.setItem(count, 0, self.user_item)
                    count += 1
            except FileNotFoundError as e:
                print(e)
            except KeyError as e:
                print(e)
            except IndexError as e:
                print(e)

        def set_selected_user(self, user):
            self.user_selected = user

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_list_win = None

        def display_new_user_win(self):
            self.new_user_win = UsersManagementWindow.UsersListWindow.NewUserWindow(self)
            self.new_user_win.show()

        def create_user(self, user_name):
            try:
                with open("./files/users.json", "r") as users_file:
                    self.users_dict = json.load(users_file)

                user = {"épreuves": []}
                self.users_dict[user_name] = user

                count = 0
                for user in self.users_dict.keys():
                    self.user_item = QTableWidgetItem(user)
                    self.user_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.user_item.setTextAlignment(Qt.AlignCenter)
                    self.users_table.setRowCount(count + 1)
                    self.users_table.setItem(count, 0, self.user_item)
                    count += 1

                with open("./files/users.json", "w") as users_file:
                    json.dump(self.users_dict, users_file, indent=4,
                              sort_keys=True, ensure_ascii=False)

            except FileNotFoundError as e:
                print(e)
            except KeyError as e:
                print(e)
            except IndexError as e:
                print(e)

        class NewUserWindow(QDialog):
            def __init__(self, master):
                super().__init__()
                self.master = master

                # ### Window config
                self.setFixedSize(300, 90)
                self.setWindowFlags(Qt.WindowCloseButtonHint)
                self.setWindowTitle("Nouveau Candidat")
                self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
                self.setModal(True)
                x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
                y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
                self.setGeometry(x, y, 300, 120)

                # Main Layout
                self.main_layout = QFormLayout()
                self.setLayout(self.main_layout)

                # Form Layout
                self.user_name = QLineEdit()
                self.user_name.setPlaceholderText("Nom Prénom")
                self.user_name.setAlignment(Qt.AlignCenter)
                self.create_user_btn = QPushButton("Créer Candidat")

                self.create_user_btn.clicked.connect(self.create_user)

                self.main_layout.addWidget(self.user_name)
                self.main_layout.addWidget(self.create_user_btn)

            def create_user(self):
                user = self.user_name.text().strip()
                if user == "":
                    error = QMessageBox(self)
                    error.setText("Le nom du candidat ne peux être vide.")
                    error.setWindowTitle("Erreur")
                    error.setIcon(QMessageBox.Critical)
                    error.setModal(True)
                    error.exec_()
                else:
                    self.master.create_user(user)

            def closeEvent(self, a0: QCloseEvent):
                """ Close Event """
                self.master.new_user_win = None
