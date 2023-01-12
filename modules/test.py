""" Test Windows """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QComboBox, QFrame, QToolBox, \
    QCheckBox, QLabel

from modules.users_management import UsersListWindow
from modules.contants import *


class TestLauncherWindow(QWidget):
    """ Test Launcher Window """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.series = get_series()
        self.users = get_users()
        self.users_list_win = None

        # ### Window config
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Choix du candidat et de l'épreuve")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Theme Layout
        self.theme_layout = QVBoxLayout()
        self.theme_grp = QGroupBox("Theme")
        self.theme_grp.setLayout(self.theme_layout)
        self.theme_grp.setFixedSize(500, 480)
        self.main_layout.addWidget(self.theme_grp)

        # User/Options/start-button Layout
        self.user_opt_start_layout = QVBoxLayout()
        self.main_layout.addLayout(self.user_opt_start_layout)

        # User Layout
        self.user_layout = QVBoxLayout()
        self.user_grp = QGroupBox("Candidat")
        self.user_grp.setLayout(self.user_layout)
        self.user_opt_start_layout.addWidget(self.user_grp)

        # Time Layout
        self.time_layout = QVBoxLayout()
        self.time_grp = QGroupBox("Compte à rebourd")
        self.time_grp.setLayout(self.time_layout)
        self.user_opt_start_layout.addWidget(self.time_grp)

        # Number of Questions Layout
        self.num_questions_layout = QVBoxLayout()
        self.num_questions_grp = QGroupBox("Nombre de questions")
        self.num_questions_grp.setLayout(self.num_questions_layout)
        self.user_opt_start_layout.addWidget(self.num_questions_grp)

        # Start Button
        self.start_test_btn = QPushButton("Démarrer le test")
        self.user_opt_start_layout.addWidget(self.start_test_btn)

        # Theme
        self.theme_combo = QComboBox()
        self.theme_layout.addWidget(self.theme_combo)
        self.theme_combo.addItems(["Choix des thèmes", "Choix d'une série"])
        # self.theme_combo.setFixedWidth(250)
        self.theme_combo.setEditable(True)
        self.theme_combo.lineEdit().setReadOnly(True)
        self.theme_combo.lineEdit().setAlignment(Qt.AlignCenter)
        for i in range(0, self.theme_combo.count()):
            self.theme_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.theme_combo.activated.connect(self.set_theme_type)
        self.theme_combo.setCurrentIndex(0)

        self.free_choice_frame = QFrame()
        self.free_choice_layout = QVBoxLayout()
        self.free_choice_frame.setLayout(self.free_choice_layout)
        self.theme_layout.addWidget(self.free_choice_frame)

        self.define_choice_frame = QFrame()
        self.define_choice_layout = QVBoxLayout()
        self.define_choice_frame.setLayout(self.define_choice_layout)
        self.theme_layout.addWidget(self.define_choice_frame)
        self.define_choice_frame.hide()

        self.define_choice_combo = QComboBox()
        self.define_choice_layout.addWidget(self.define_choice_combo)
        self.define_choice_combo.addItems([key for key in self.series.keys()])
        # self.theme_combo.setFixedWidth(250)
        self.define_choice_combo.setEditable(True)
        self.define_choice_combo.lineEdit().setReadOnly(True)
        self.define_choice_combo.lineEdit().setAlignment(Qt.AlignCenter)
        for i in range(0, self.define_choice_combo.count()):
            self.define_choice_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.define_choice_combo.activated.connect(lambda: print("TODO"))

        self.define_choice_label = QLabel("Les séries sont des questions prédéfinies pour la "
                                          "Règlementation ou la Technique, répartit équitablement "
                                          "entre chaques thèmes.")
        self.define_choice_label.setWordWrap(True)
        self.define_choice_layout.addWidget(self.define_choice_label)

        self.themes_toolbox = QToolBox()
        self.free_choice_layout.addWidget(self.themes_toolbox)

        self.themes_checkbox_layout = QHBoxLayout()
        self.free_choice_layout.addLayout(self.themes_checkbox_layout)
        self.reglementation_checkbox = QCheckBox("Toute la Règlementation")
        self.technique_checkbox = QCheckBox("Toute la Technique")
        self.themes_checkbox_layout.addWidget(self.reglementation_checkbox, 1, Qt.AlignCenter)
        self.themes_checkbox_layout.addWidget(self.technique_checkbox, 1, Qt.AlignCenter)
        # noinspection PyUnresolvedReferences
        self.reglementation_checkbox.stateChanged.connect(lambda e: self.select_reglementation_themes(e))
        # noinspection PyUnresolvedReferences
        self.technique_checkbox.stateChanged.connect(lambda e: self.select_technique_themes(e))

        self.themes_buttons_layout = QHBoxLayout()
        self.free_choice_layout.addLayout(self.themes_buttons_layout)
        self.select_all_btn = QPushButton("Tout cocher")
        self.deselect_all_btn = QPushButton("Tout décocher")
        self.themes_buttons_layout.addWidget(self.select_all_btn)
        self.themes_buttons_layout.addWidget(self.deselect_all_btn)
        self.select_all_btn.clicked.connect(self.select_all_themes)
        self.deselect_all_btn.clicked.connect(self.deselect_all_themes)

        # Themes ToolBox
        self.themes_checkbox_dict = {}
        self.reglementation_layout = QVBoxLayout()
        self.technique_layout = QVBoxLayout()
        self.reglementation_widget = QWidget()
        self.technique_widget = QWidget()
        self.reglementation_widget.setLayout(self.reglementation_layout)
        self.technique_widget.setLayout(self.technique_layout)
        self.themes_toolbox.addItem(self.reglementation_widget, "Règlementation")
        self.themes_toolbox.addItem(self.technique_widget, "Technique")
        for themes in SEPARATED_THEME_DICT.items():
            for theme in themes[1].items():
                if theme:
                    self.themes_checkbox_dict[f"{theme[0]}"] = QCheckBox(f"{theme[1]}")
                    if theme[0] in SEPARATED_THEME_DICT["Reglementation"]:
                        self.reglementation_layout.addWidget(self.themes_checkbox_dict[f"{theme[0]}"])
                    elif theme[0] in SEPARATED_THEME_DICT["Technique"]:
                        self.technique_layout.addWidget(self.themes_checkbox_dict[f"{theme[0]}"])

        # User
        self.users_combo = QComboBox()
        self.users_btn = QPushButton("Gestion des candidats")
        self.user_layout.addWidget(self.users_combo)
        self.user_layout.addWidget(self.users_btn)

        self.users_combo.setEditable(True)
        self.users_combo.lineEdit().setReadOnly(True)
        self.users_combo.lineEdit().setAlignment(Qt.AlignCenter)
        self.users_combo.addItems([user for user in self.users.keys()])
        for i in range(0, self.users_combo.count()):
            self.users_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.users_combo.activated.connect(lambda: print("TODO: afficher moyenne candidat si existe"))
        self.users_btn.clicked.connect(self.display_users_win)

        # Timer
        self.time_checkbox = QCheckBox("Activer le compte à rebourd")
        self.handi_checkbox = QCheckBox("Session handicapé")
        self.time_combo = QComboBox()
        self.time_layout.addWidget(self.time_checkbox)
        self.time_layout.addWidget(self.handi_checkbox)
        self.time_layout.addWidget(self.time_combo)

        # Number of Questions
        self.num_questions_combo = QComboBox()
        self.num_questions_layout.addWidget(self.num_questions_combo)

    def rebuild_users_combo(self):
        """ Rebuild users combobox """
        self.users = get_users()
        self.users_combo.clear()
        self.users_combo.addItems([user for user in self.users.keys()])
        for i in range(0, self.users_combo.count()):
            self.users_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

    def display_users_win(self):
        """ Display the Users List Window """
        if self.users_list_win is not None:
            self.users_list_win.close()
        self.users_list_win = UsersListWindow(self, 1)
        self.users_list_win.show()
        self.setDisabled(True)

    def select_all_themes(self):
        """ Select all themes """
        for checkbox in self.themes_checkbox_dict.values():
            checkbox.setChecked(True)
        self.reglementation_checkbox.setChecked(True)
        self.technique_checkbox.setChecked(True)

    def deselect_all_themes(self):
        """ Deselect all themes """
        for checkbox in self.themes_checkbox_dict.values():
            checkbox.setChecked(False)
        self.reglementation_checkbox.setChecked(False)
        self.technique_checkbox.setChecked(False)

    def select_reglementation_themes(self, event):
        """ Select reglementation themes """
        if event:
            for themes in SEPARATED_THEME_DICT.items():
                for theme in themes[1].items():
                    if theme:
                        if theme[0] in SEPARATED_THEME_DICT["Reglementation"]:
                            self.themes_checkbox_dict[f"{theme[0]}"].setChecked(True)
        else:
            for themes in SEPARATED_THEME_DICT.items():
                for theme in themes[1].items():
                    if theme:
                        if theme[0] in SEPARATED_THEME_DICT["Reglementation"]:
                            self.themes_checkbox_dict[f"{theme[0]}"].setChecked(False)

    def select_technique_themes(self, event):
        """ Select technique themes """
        if event:
            for themes in SEPARATED_THEME_DICT.items():
                for theme in themes[1].items():
                    if theme:
                        if theme[0] in SEPARATED_THEME_DICT["Technique"]:
                            self.themes_checkbox_dict[f"{theme[0]}"].setChecked(True)
        else:
            for themes in SEPARATED_THEME_DICT.items():
                for theme in themes[1].items():
                    if theme:
                        if theme[0] in SEPARATED_THEME_DICT["Technique"]:
                            self.themes_checkbox_dict[f"{theme[0]}"].setChecked(False)

    def set_theme_type(self):
        """ Select the theme type """
        if self.theme_combo.currentText() == "Choix des thèmes":
            self.define_choice_frame.hide()
            self.free_choice_frame.show()
            self.theme_grp.setFixedSize(500, 480)
        elif self.theme_combo.currentText() == "Choix d'une série":
            self.define_choice_frame.show()
            self.free_choice_frame.hide()
            self.theme_grp.setFixedSize(500, 280)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.test_launcher_win = None
        self.master.enable_buttons()
        # self.master.show()
