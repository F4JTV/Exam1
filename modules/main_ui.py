""" Main UI """
import os.path
import sys
import webbrowser
from datetime import datetime

from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QCloseEvent
from PyQt5.QtWidgets import (QMainWindow, QMenuBar, QMenu, QAction,
                             QHBoxLayout, QLabel, QMessageBox, QWidget,
                             QVBoxLayout, QToolButton)

from modules.users_management import UsersManagementWindow
from modules.errors_management import ErrorsManagementWindow
from modules.asked_questions import AskedQuestionsWindow
from modules.all_questions import AllQuestionsWindow
from modules.contribute import ContributeWindow
from modules.test import TestLauncherWindow

VERSION = datetime.now().strftime("v%m%d%y")
APP_NAME = "Exam'1"
TITLE = f"{APP_NAME} - {VERSION}"
WIDTH = 840
HEIGHT = 400
MAIN_FONT = QFont("Lato", 11)
MAIN_BTN_FONT = QFont("Lato", 12)
MAIN_BTN_SIZE = QSize(125, 170)


class MainWindow(QMainWindow):
    """ Main Window """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ### Main Window config
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setObjectName("Main")

        # ### Variables
        self.opacity = 0
        self.test_launcher_win = None
        self.users_management_win = None
        self.errors_management_win = None
        self.asked_questions_win = None
        self.all_questions_win = None
        self.contribute_win = None

        # ### Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # ### Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.software_menu = QMenu("&Logiciels et cours")
        self.lesson_action = QAction("cours_radio.pdf")
        self.lesson_action.setIcon(QIcon(""))
        self.software_menu.addAction(self.lesson_action)
        # noinspection PyUnresolvedReferences
        pdf_path = os.path.realpath("./files/cours_radio.pdf")
        # noinspection PyUnresolvedReferences
        self.lesson_action.triggered.connect(lambda: webbrowser.open(f"file://{pdf_path}"))

        self.about_action = QAction("A propos")
        # noinspection PyUnresolvedReferences
        self.about_action.triggered.connect(lambda: print("A propos"))

        self.menu_bar.addMenu(self.software_menu)
        self.menu_bar.addAction(self.about_action)

        # ### Main Layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.buttons_layout = QHBoxLayout()
        self.title_layout = QVBoxLayout()

        self.main_layout.addLayout(self.buttons_layout, 1)
        self.main_layout.addLayout(self.title_layout, 1)

        # ## Buttons Layout
        self.start_test_btn = QToolButton()
        self.start_test_btn.setFixedSize(MAIN_BTN_SIZE)
        self.start_test_btn.setFont(MAIN_BTN_FONT)
        self.start_test_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.start_test_btn.setIcon(QIcon("./images/start_test.png"))
        self.start_test_btn.setIconSize(QSize(100, 100))
        self.start_test_btn.setText("Démarrer un\nquestionnaire")
        self.start_test_btn.clicked.connect(self.display_test_launcher_win)

        self.manage_users_btn = QToolButton()
        self.manage_users_btn.setFixedSize(MAIN_BTN_SIZE)
        self.manage_users_btn.setFont(MAIN_BTN_FONT)
        self.manage_users_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.manage_users_btn.setIcon(QIcon("./images/manage_users.png"))
        self.manage_users_btn.setIconSize(QSize(100, 100))
        self.manage_users_btn.setText("Gestion des\npoints et\ncandidats")
        self.manage_users_btn.clicked.connect(self.display_users_management_win)

        self.manage_errors_btn = QToolButton()
        self.manage_errors_btn.setFixedSize(MAIN_BTN_SIZE)
        self.manage_errors_btn.setFont(MAIN_BTN_FONT)
        self.manage_errors_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.manage_errors_btn.setIcon(QIcon("./images/manage_errors.png"))
        self.manage_errors_btn.setIconSize(QSize(100, 100))
        self.manage_errors_btn.setText("Gestion des\nerreurs")
        self.manage_errors_btn.clicked.connect(self.display_errors_management_win)

        self.asked_questions_btn = QToolButton()
        self.asked_questions_btn.setFixedSize(MAIN_BTN_SIZE)
        self.asked_questions_btn.setFont(MAIN_BTN_FONT)
        self.asked_questions_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.asked_questions_btn.setIcon(QIcon("./images/asked_questions.png"))
        self.asked_questions_btn.setIconSize(QSize(100, 100))
        self.asked_questions_btn.setText("Questions\nposées")
        self.asked_questions_btn.clicked.connect(self.display_asked_questions_win)

        self.show_questions_btn = QToolButton()
        self.show_questions_btn.setFixedSize(MAIN_BTN_SIZE)
        self.show_questions_btn.setFont(MAIN_BTN_FONT)
        self.show_questions_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.show_questions_btn.setIcon(QIcon("./images/show_questions.png"))
        self.show_questions_btn.setIconSize(QSize(100, 100))
        self.show_questions_btn.setText("Visu des\nquestions")
        self.show_questions_btn.clicked.connect(self.display_all_questions_win)

        self.contribute_btn = QToolButton()
        self.contribute_btn.setFixedSize(MAIN_BTN_SIZE)
        self.contribute_btn.setFont(MAIN_BTN_FONT)
        self.contribute_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.contribute_btn.setIcon(QIcon("./images/contribute.png"))
        self.contribute_btn.setIconSize(QSize(100, 100))
        self.contribute_btn.setText("Contribuez à\nl'amélioration\nd'Exam'1")
        self.contribute_btn.clicked.connect(self.display_contribute_win)

        self.buttons_layout.addWidget(self.start_test_btn, 1, Qt.AlignmentFlag.AlignJustify)
        self.buttons_layout.addWidget(self.manage_users_btn, 1, Qt.AlignmentFlag.AlignJustify)
        self.buttons_layout.addWidget(self.manage_errors_btn, 1, Qt.AlignmentFlag.AlignJustify)
        self.buttons_layout.addWidget(self.asked_questions_btn, 1, Qt.AlignmentFlag.AlignJustify)
        self.buttons_layout.addWidget(self.show_questions_btn, 1, Qt.AlignmentFlag.AlignJustify)
        self.buttons_layout.addWidget(self.contribute_btn, 1, Qt.AlignmentFlag.AlignJustify)

        # ### Title Layout
        self.main_label = QLabelClickable()
        # self.main_label.setPixmap(QPixmap("./images/exam1.png"))
        self.main_label.setText("Exam'1")
        self.main_label.setFont(QFont("Radio Space", 72))
        self.title_label = QLabel("Règlementation et Technique")
        self.subtitle_label = QLabel("Logiciel de simulation de l'examen Radioamateur Français")

        # noinspection PyUnresolvedReferences
        self.main_label.clicked.connect(lambda: webbrowser.open("https://f6kgl-f5kff.fr/exam1/", 2))
        self.title_label.setObjectName("TitleLabel")
        self.subtitle_label.setObjectName("SubTitleLabel")

        self.title_label.setFont(QFont("Lato", 15))
        self.subtitle_label.setFont(QFont("Lato", 11))

        self.title_layout.addWidget(self.main_label, 3, Qt.AlignmentFlag.AlignCenter)
        self.title_layout.addWidget(self.title_label, 1, Qt.AlignmentFlag.AlignCenter)
        self.title_layout.addWidget(self.subtitle_label, 1, Qt.AlignmentFlag.AlignCenter)

        self.main_label.setContentsMargins(0, 0, 0, 0)
        self.subtitle_label.setContentsMargins(0, 0, 0, 0)

        # Opacity Timer Open
        self.opacity_timer_open = QTimer(self)
        self.opacity_timer_open.setInterval(10)
        # noinspection PyUnresolvedReferences
        self.opacity_timer_open.timeout.connect(self.up_opacity)
        # Opacity Timer CLose
        self.opacity_timer_close = QTimer(self)
        self.opacity_timer_close.setInterval(10)
        # noinspection PyUnresolvedReferences
        self.opacity_timer_close.timeout.connect(self.down_opacity)

    def disable_buttons(self):
        """ Disable all toolbuttons """
        self.manage_users_btn.setDisabled(True)
        self.manage_errors_btn.setDisabled(True)
        self.asked_questions_btn.setDisabled(True)
        self.show_questions_btn.setDisabled(True)
        self.contribute_btn.setDisabled(True)
        self.start_test_btn.setDisabled(True)

    def enable_buttons(self):
        """ Enable all toolbuttons """
        self.manage_users_btn.setEnabled(True)
        self.manage_errors_btn.setEnabled(True)
        self.asked_questions_btn.setEnabled(True)
        self.show_questions_btn.setEnabled(True)
        self.contribute_btn.setEnabled(True)
        self.start_test_btn.setEnabled(True)

    def display_users_management_win(self):
        """ Display Management Window """
        if self.users_management_win is not None:
            self.users_management_win.close()
        else:
            self.disable_buttons()
            self.users_management_win = UsersManagementWindow(self)
            self.users_management_win.show()
            # self.hide()

    def display_errors_management_win(self):
        """ Display Management Window """
        if self.errors_management_win is not None:
            self.errors_management_win.close()
        else:
            self.disable_buttons()
            self.errors_management_win = ErrorsManagementWindow(self)
            self.errors_management_win.show()
            # self.hide()

    def display_asked_questions_win(self):
        """ Display Management Window """
        if self.asked_questions_win is not None:
            self.asked_questions_win.close()
        else:
            self.disable_buttons()
            self.asked_questions_win = AskedQuestionsWindow(self)
            self.asked_questions_win.show()
            # self.hide()

    def display_all_questions_win(self):
        """ Display Management Window """
        if self.all_questions_win is not None:
            self.all_questions_win.close()
        else:
            self.disable_buttons()
            self.all_questions_win = AllQuestionsWindow(self)
            self.all_questions_win.show()
            # self.hide()

    def display_contribute_win(self):
        """ Display Management Window """
        if self.contribute_win is not None:
            self.contribute_win.close()
        else:
            self.disable_buttons()
            self.contribute_win = ContributeWindow(self)
            self.contribute_win.show()
            # self.hide()

    def display_test_launcher_win(self):
        """ Display Management Window """
        if self.test_launcher_win is not None:
            self.test_launcher_win.close()
        else:
            self.disable_buttons()
            self.test_launcher_win = TestLauncherWindow(self)
            self.test_launcher_win.show()
            # self.hide()

    def up_opacity(self):
        """ Up the opacity """
        if self.opacity >= 1.00:
            self.opacity = 1.00
            self.opacity_timer_open.stop()
        else:
            self.opacity += 0.01
        self.setWindowOpacity(self.opacity)
        self.update()

    def down_opacity(self):
        """ Down the opacity """
        if self.opacity <= 0.00:
            self.opacity = 0.00
            self.opacity_timer_close.stop()
            sys.exit(0)
        else:
            self.opacity -= 0.01
        self.setWindowOpacity(self.opacity)
        self.update()

    def closeEvent(self, event):
        """Close event """
        dialog = QMessageBox()
        rep = dialog.question(self,
                              "Quitter",
                              "Voullez vous quittez Exam'1 ?",
                              dialog.StandardButton.Yes | dialog.StandardButton.No)
        if rep == dialog.StandardButton.Yes:
            QCloseEvent.ignore(event)
            self.opacity_timer_close.start()

            return
        elif rep == dialog.StandardButton.No:
            QCloseEvent.ignore(event)
            return


class QLabelClickable(QLabel):
    """Clickable QLabel"""
    # noinspection PyArgumentList
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        """Emit a clicked signal if there is Mouse Press Event"""
        # noinspection PyUnresolvedReferences
        self.clicked.emit()
