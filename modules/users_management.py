""" Users management and progression Windows """
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
            # self.hide()
            self.users_list_btn.setDisabled(True)
            self.tests_list_btn.setDisabled(True)
            self.users_tests_list_btn.setDisabled(True)
            self.users_tests_trial_list_btn.setDisabled(True)
            self.progress_users_trial_btn.setDisabled(True)

            self.users_list_win = UsersListWindow(self, 0)
            self.users_list_win.show()

    def display_progress_users_trial_win(self):
        """ Display Progress Users Trial Window """
        if self.progress_users_trial_win is not None:
            return
        else:
            # self.hide()
            self.users_list_btn.setDisabled(True)
            self.tests_list_btn.setDisabled(True)
            self.users_tests_list_btn.setDisabled(True)
            self.users_tests_trial_list_btn.setDisabled(True)
            self.progress_users_trial_btn.setDisabled(True)
            self.progress_users_trial_win = ProgressUsersTrialWindow(self)
            self.progress_users_trial_win.show()

    def display_users_tests_trial_list_win(self):
        """ Display Users Test Trial List Window """
        if self.users_tests_trial_list_win is not None:
            return
        else:
            # self.hide()
            self.users_list_btn.setDisabled(True)
            self.tests_list_btn.setDisabled(True)
            self.users_tests_list_btn.setDisabled(True)
            self.users_tests_trial_list_btn.setDisabled(True)
            self.progress_users_trial_btn.setDisabled(True)
            self.users_tests_trial_list_win = UsersTestsTrialListWindow(self)
            self.users_tests_trial_list_win.show()

    def display_users_tests_list(self):
        """ Display the tests list window """
        if self.users_test_list_win is not None:
            return
        else:
            # self.hide()
            self.users_list_btn.setDisabled(True)
            self.tests_list_btn.setDisabled(True)
            self.users_tests_list_btn.setDisabled(True)
            self.users_tests_trial_list_btn.setDisabled(True)
            self.progress_users_trial_btn.setDisabled(True)
            self.users_test_list_win = UsersTestsListWindow(self)
            self.users_test_list_win.show()

    def display_tests_list(self):
        """ Display the tests list window """
        if self.test_list_win is not None:
            return
        else:
            # self.hide()
            self.users_list_btn.setDisabled(True)
            self.tests_list_btn.setDisabled(True)
            self.users_tests_list_btn.setDisabled(True)
            self.users_tests_trial_list_btn.setDisabled(True)
            self.progress_users_trial_btn.setDisabled(True)
            self.test_list_win = TestsListWindow(self)
            self.test_list_win.show()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        if self.users_list_win is not None:
            self.users_list_win.close()
        if self.progress_users_trial_win is not None:
            self.progress_users_trial_win.close()
        if self.users_tests_trial_list_win is not None:
            self.users_tests_trial_list_win.close()
        if self.users_test_list_win is not None:
            self.users_test_list_win.close()
        if self.test_list_win is not None:
            self.test_list_win.close()
        # self.master.show()
        self.master.users_management_win = None
        self.master.enable_buttons()


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

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        # self.master.show()
        self.master.test_list_win = None
        self.master.tests_list_btn.setEnabled(True)
        self.master.users_list_btn.setEnabled(True)
        self.master.users_tests_list_btn.setEnabled(True)
        self.master.users_tests_trial_list_btn.setEnabled(True)
        self.master.progress_users_trial_btn.setEnabled(True)


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

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        # self.master.show()
        self.master.users_test_list_win = None
        self.master.tests_list_btn.setEnabled(True)
        self.master.users_list_btn.setEnabled(True)
        self.master.users_tests_list_btn.setEnabled(True)
        self.master.users_tests_trial_list_btn.setEnabled(True)
        self.master.progress_users_trial_btn.setEnabled(True)


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

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        # self.master.show()
        self.master.users_tests_trial_list_win = None
        self.master.tests_list_btn.setEnabled(True)
        self.master.users_list_btn.setEnabled(True)
        self.master.users_tests_list_btn.setEnabled(True)
        self.master.users_tests_trial_list_btn.setEnabled(True)
        self.master.progress_users_trial_btn.setEnabled(True)


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

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        # self.master.show()
        self.master.progress_users_trial_win = None
        self.master.tests_list_btn.setEnabled(True)
        self.master.users_list_btn.setEnabled(True)
        self.master.users_tests_list_btn.setEnabled(True)
        self.master.users_tests_trial_list_btn.setEnabled(True)
        self.master.progress_users_trial_btn.setEnabled(True)


class UsersListWindow(QWidget):
    """ Progress Users Trial Window """

    def __init__(self, master, flag):
        super().__init__()
        self.master = master
        self.flag = flag

        self.new_user_win = None
        self.edit_user_win = None
        self.user_item = QTableWidgetItem()
        self.users_dict = dict()
        self.user_selected = str()

        # ### Window config
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Liste des candidats")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout, 1)
        self.add_user_btn = QPushButton("Nouveau Candidat")
        self.remove_user_btn = QPushButton("Supprimer")
        self.edit_user_btn = QPushButton("Modifier")

        self.add_user_btn.clicked.connect(self.display_new_user_win)
        self.remove_user_btn.clicked.connect(self.remove_user)
        self.edit_user_btn.clicked.connect(self.display_edit_user_win)

        self.buttons_layout.addWidget(self.add_user_btn)
        self.buttons_layout.addWidget(self.remove_user_btn)
        self.buttons_layout.addWidget(self.edit_user_btn)

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
            with open("./files/users.json", "r", encoding="utf-8") as users_file:
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
        """ Set the selected user in the table """
        self.user_selected = user

    def display_new_user_win(self):
        """ Display the new user Window """
        self.new_user_win = NewUserWindow(self)
        self.new_user_win.show()

    def display_edit_user_win(self):
        """ Display the edit user Window """
        if self.user_selected == "":
            return
        self.edit_user_win = EditUserWindow(self)
        self.edit_user_win.show()

    def create_user(self, user_name):
        """ Create the new user """
        try:
            with open("./files/users.json", "r", encoding="utf-8") as users_file:
                self.users_dict = json.load(users_file)

            user = {"épreuves": [],
                    "erreurs": []}
            self.users_dict[user_name] = user

            count = 0
            for user in self.users_dict.keys():
                self.user_item = QTableWidgetItem(user)
                self.user_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.user_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setRowCount(count + 1)
                self.users_table.setItem(count, 0, self.user_item)
                count += 1

            self.save_user_file()

        except FileNotFoundError as e:
            print(e)
        except KeyError as e:
            print(e)
        except IndexError as e:
            print(e)

    def remove_user(self):
        """ Remove the selected user """
        if self.user_selected == "":
            display_error(self, "Veuillez sélectionner un candidat")
            return
        else:
            dialog = QMessageBox()
            rep = dialog.question(self,
                                  "Supprimer Candidat",
                                  f"Voullez vous supprimer le candidat\n"
                                  f"{self.user_selected} et toutes ses données ?",
                                  dialog.StandardButton.Yes | dialog.StandardButton.No)
            if rep == dialog.StandardButton.Yes:
                pass
            elif rep == dialog.StandardButton.No:
                return

            try:
                with open("./files/users.json", "r", encoding="utf-8") as users_file:
                    self.users_dict = json.load(users_file)
            except FileNotFoundError as e:
                print(e)

            self.users_dict.pop(self.user_selected)
            self.user_selected = ""
            self.save_user_file()
            if len(self.users_dict.keys()) == 0:
                self.users_table.setRowCount(0)
            else:
                count = 0
                for user in self.users_dict.keys():
                    self.user_item = QTableWidgetItem(user)
                    self.user_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.user_item.setTextAlignment(Qt.AlignCenter)
                    self.users_table.setRowCount(count + 1)
                    self.users_table.setItem(count, 0, self.user_item)
                    count += 1

    def save_user_file(self):
        """ Save the users in users.json file """
        try:
            with open("./files/users.json", "w", encoding="utf-8") as users_file:
                json.dump(self.users_dict, users_file, indent=4,
                          sort_keys=True, ensure_ascii=False)
        except FileNotFoundError as e:
            print(e)

    def edit_user(self, new_name):
        """ Edit the selected username """
        if self.user_selected == "":
            display_error(self, "Veuillez sélectionner un candidat")
            return
        else:
            self.users_dict[new_name] = self.users_dict[self.user_selected]
            self.users_dict.pop(self.user_selected)
            self.user_selected = ""
            self.save_user_file()

            count = 0
            for user in self.users_dict.keys():
                self.user_item = QTableWidgetItem(user)
                self.user_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.user_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setRowCount(count + 1)
                self.users_table.setItem(count, 0, self.user_item)
                count += 1

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.users_list_win = None

        if self.flag == 0:
            self.master.tests_list_btn.setEnabled(True)
            self.master.users_list_btn.setEnabled(True)
            self.master.users_tests_list_btn.setEnabled(True)
            self.master.users_tests_trial_list_btn.setEnabled(True)
            self.master.progress_users_trial_btn.setEnabled(True)
        elif self.flag == 1:
            self.master.setEnabled(True)
            self.master.rebuild_users_combo()


class NewUserWindow(QDialog):
    """ New User Window """
    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(300, 90)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Nouveau Candidat")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setModal(True)

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
        """ Create the user """
        user = self.user_name.text().strip()
        for name in self.master.users_dict.keys():
            if name == user:
                display_error(self, "Le nom du candidat existe déjà.")
                return
        if user == "":
            display_error(self, "Le nom du candidat ne peux être vide.")
            return
        else:
            self.master.create_user(user)
            self.close()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.new_user_win = None


class EditUserWindow(QDialog):
    """ Edit User Window """
    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(300, 90)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Modifier Candidat")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setModal(True)

        # Main Layout
        self.main_layout = QFormLayout()
        self.setLayout(self.main_layout)

        # Form Layout
        self.user_name = QLineEdit()
        self.user_name.setPlaceholderText("Nom Prénom")
        self.user_name.setText(self.master.user_selected)
        self.user_name.setAlignment(Qt.AlignCenter)
        self.edit_user_btn = QPushButton("Modifier Candidat")

        self.edit_user_btn.clicked.connect(self.edit_user)

        self.main_layout.addWidget(self.user_name)
        self.main_layout.addWidget(self.edit_user_btn)

    def edit_user(self):
        """ Edit the selected username """
        user = self.user_name.text().strip()
        for name in self.master.users_dict.keys():
            if name == user:
                display_error(self, "Le nom du candidat existe déjà.")
                return
        if user == "":
            display_error(self, "Le nom du candidat ne peux être vide.")
            return
        else:
            self.master.edit_user(user)
            self.close()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.edit_user_win = None


def display_error(master, error):
    """ Display the given error """
    error_win = QMessageBox(master)
    error_win.setText(error)
    error_win.setWindowTitle("Erreur")
    error_win.setIcon(QMessageBox.Critical)
    error_win.setModal(True)
    error_win.exec_()
