""" Users Management Window """
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QToolButton


class UsersManagementWindow(QDialog):
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
        self.setModal(True)
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


    class TestsListWindow(QDialog):
        """  Test List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste complète des épreuves")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.test_list_win = None


    class UsersTestsListWindow(QDialog):
        """ Users Test List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des épreuves par candidat")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_test_list_win = None


    class UsersTestsTrialListWindow(QDialog):
        """ Users Test Trial List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des épreuves par candidats et par type d'épreuve")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_tests_trial_list_win = None


    class ProgressUsersTrialWindow(QDialog):
        """ Progress Users Trial Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Progression par type d'épreuve et par candidat")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.progress_users_trial_win = None


    class UsersListWindow(QDialog):
        """ Progress Users Trial Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste des candidats")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.master.geometry().x() + self.master.master.width() // 2 - self.width() // 2
            y = self.master.master.geometry().y() + self.master.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 400, 400)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_list_win = None
