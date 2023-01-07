""" Errors Management Window """
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolButton


class ErrorsManagementWindow(QWidget):
    """ Errors Management Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # Variables
        self.btn_size = QSize(370, 60)
        self.btn_font = QFont("Lato", 12)

        self.errors_list_win = None
        self.users_errors_list_win = None

        # ### Window config
        self.setFixedSize(400, 160)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Gestion des erreurs")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons
        self.errors_list_btn = QToolButton()
        self.errors_list_btn.setText("Liste complète")
        self.errors_list_btn.setFixedSize(self.btn_size)
        self.errors_list_btn.setFont(self.btn_font)
        self.errors_list_btn.clicked.connect(self.display_errors_list)

        self.users_errors_list_btn = QToolButton()
        self.users_errors_list_btn.setText("Liste par candidat")
        self.users_errors_list_btn.setFixedSize(self.btn_size)
        self.users_errors_list_btn.setFont(self.btn_font)
        self.users_errors_list_btn.clicked.connect(self.display_users_errors_list)

        self.main_layout.addWidget(self.errors_list_btn, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.users_errors_list_btn, 1, Qt.AlignmentFlag.AlignCenter)


    def display_errors_list(self):
        """ Display the tests list window """
        if self.errors_list_win is not None:
            return
        else:
            self.hide()
            self.errors_list_win = ErrorsManagementWindow.ErrorsListWindow(self)
            self.errors_list_win.show()

    def display_users_errors_list(self):
        """ Display the tests list window """
        if self.users_errors_list_win is not None:
            return
        else:
            self.hide()
            self.users_errors_list_win = ErrorsManagementWindow.UsersErrorsListWindow(self)
            self.users_errors_list_win.show()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.errors_management_win = None
        self.master.show()


    class UsersErrorsListWindow(QWidget):
        """  Users List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste complète des erreurs par candidat")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.users_errors_list_win = None


    class ErrorsListWindow(QWidget):
        """ Users Test List Window """

        def __init__(self, master):
            super().__init__()
            self.master = master

            # ### Window config
            self.setFixedSize(400, 400)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle("Liste complète des erreurs")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.errors_list_win = None