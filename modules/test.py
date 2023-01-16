""" Test Windows """
import random

from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon, QCloseEvent, QPixmap
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
                             QPushButton, QComboBox, QFrame, QToolBox,
                             QCheckBox, QLabel, QProgressBar, QButtonGroup)

from modules.users_management import UsersListWindow
from modules.contants import *

IMAGE_SIZE = QSize(770, 420)
TIME_DICT = {"5 minutes": 5,
             "10 minutes": 10,
             "15 minutes - Règlementation": 15,
             "20 minutes": 20,
             "30 minutes - Technique": 30,
             "45 minutes - Règlementation aménagée": 45,
             "60 minutes": 60,
             "75 minutes": 75,
             "90 minutes - Technique aménagée": 90}


class TestLauncherWindow(QWidget):
    """ Test Launcher Window """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.series = get_series()
        self.users = get_users()
        self.questions = get_questions()
        self.users_list_win = None
        self.test_win = None
        self.exit_flag = False
        self.theme_type = 0

        # #################### Window config
        self.setFixedSize(900, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Choix du candidat et de l'épreuve")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # #################### Main Layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # #################### Theme Layout
        self.theme_layout = QVBoxLayout()
        self.theme_grp = QGroupBox("Theme")
        self.theme_grp.setLayout(self.theme_layout)
        # self.theme_grp.setFixedSize(500, 480)
        self.main_layout.addWidget(self.theme_grp)

        # #################### User/Options/start-button Layout
        self.user_opt_start_layout = QVBoxLayout()
        self.main_layout.addLayout(self.user_opt_start_layout)

        # #################### User Layout
        self.user_layout = QVBoxLayout()
        self.user_grp = QGroupBox("Candidat")
        self.user_grp.setLayout(self.user_layout)
        self.user_opt_start_layout.addWidget(self.user_grp, 3)

        # #################### Time Layout
        self.time_layout = QVBoxLayout()
        self.time_grp = QGroupBox("Compte à rebourd")
        self.time_grp.setLayout(self.time_layout)
        self.user_opt_start_layout.addWidget(self.time_grp, 2)

        # #################### Number of Questions Layout
        self.num_questions_layout = QVBoxLayout()
        self.num_questions_grp = QGroupBox("Nombre de questions")
        self.num_questions_grp.setLayout(self.num_questions_layout)
        self.user_opt_start_layout.addWidget(self.num_questions_grp, 2)

        # #################### Start Button
        self.start_test_btn = QPushButton("Démarrer le test")
        self.user_opt_start_layout.addWidget(self.start_test_btn, 1)
        self.start_test_btn.clicked.connect(self.launch_test)

        # #################### Theme
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
        self.define_choice_combo.activated.connect(self.display_serie_details)

        self.define_choice_label = QLabel("Les séries sont des questions prédéfinies pour la "
                                          "Règlementation ou la Technique, répartit équitablement "
                                          "entre chaques thèmes.\n\nT = Technique\nR = Règlementation")
        self.serie_detail_label = QLabel()
        self.serie_detail_label.setWordWrap(True)
        self.define_choice_label.setWordWrap(True)
        self.define_choice_layout.addWidget(self.define_choice_label)
        self.define_choice_layout.addWidget(self.serie_detail_label)

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

        # #################### Themes ToolBox
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
                    # noinspection PyUnresolvedReferences
                    self.themes_checkbox_dict[f"{theme[0]}"].stateChanged.connect(self.set_number_of_questions)
                    if theme[0] in SEPARATED_THEME_DICT["Reglementation"]:
                        self.reglementation_layout.addWidget(self.themes_checkbox_dict[f"{theme[0]}"])
                    elif theme[0] in SEPARATED_THEME_DICT["Technique"]:
                        self.technique_layout.addWidget(self.themes_checkbox_dict[f"{theme[0]}"])

        # #################### User
        self.users_combo = QComboBox()
        self.user_average_label = QLabel("Moyenne générale:")
        self.users_btn = QPushButton("Gestion des candidats")
        self.user_layout.addWidget(self.users_combo)
        self.user_layout.addWidget(self.user_average_label)
        self.user_layout.addWidget(self.users_btn)

        self.users_combo.setEditable(True)
        self.users_combo.lineEdit().setReadOnly(True)
        self.users_combo.lineEdit().setAlignment(Qt.AlignCenter)
        self.users_combo.addItems([user for user in self.users.keys()])
        for i in range(0, self.users_combo.count()):
            self.users_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.users_combo.activated.connect(lambda: self.user_average_label.setText("Moyenne générale: TODO"))
        self.users_btn.clicked.connect(self.display_users_win)

        # #################### Timer
        self.time_checkbox = QCheckBox("Activer le compte à rebourd")
        self.time_combo = QComboBox()
        self.time_layout.addWidget(self.time_checkbox)
        self.time_layout.addWidget(self.time_combo)
        self.time_combo.setEditable(True)
        self.time_combo.lineEdit().setReadOnly(True)
        self.time_combo.lineEdit().setAlignment(Qt.AlignCenter)
        self.time_combo.addItems([key for key in TIME_DICT.keys()])
        for i in range(0, self.time_combo.count()):
            self.time_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.time_checkbox.stateChanged.connect(lambda e: self.toggle_timer(e))
        self.time_checkbox.setChecked(True)

        # #################### Number of Questions
        self.num_questions_combo = QComboBox()
        self.num_questions_label = QLabel("Le nombre de question est un multiple du nombre de thèmes")
        self.num_questions_label.setWordWrap(True)
        self.num_questions_layout.addWidget(self.num_questions_combo)
        self.num_questions_layout.addWidget(self.num_questions_label)
        self.num_questions_combo.setEditable(True)
        self.num_questions_combo.lineEdit().setReadOnly(True)
        self.num_questions_combo.lineEdit().setAlignment(Qt.AlignCenter)

    def display_serie_details(self):
        """ Display the details for this serie """
        text = ""
        for question, num_question in self.series[self.define_choice_combo.currentText()].items():
            text += f"{question}: {num_question}\t"
        self.serie_detail_label.setText(text)

    def launch_test(self):
        """ Launch the test """
        try:
            candidat = self.users_combo.currentText()
            themes = []
            if self.free_choice_frame.isVisible():
                self.theme_type = 0
                for checkbox in self.themes_checkbox_dict.items():
                    if checkbox[1].isChecked():
                        themes.append(checkbox[0])

                if len(themes) == 0:
                    display_error(self, "Veuillez sélectionner au moins un thème")
                    return

            elif self.define_choice_frame.isVisible():
                self.theme_type = 1
                themes = [self.define_choice_combo.currentText()]

            timer_state = self.time_checkbox.isChecked()
            timer = self.time_combo.currentText()
            number_of_questions = self.num_questions_combo.currentText()

            if self.test_win is not None:
                self.test_win.close()
            else:
                dialog = QMessageBox()
                rep = dialog.question(self,
                                      "Commencer",
                                      f"{candidat},\nEtes vous prèt à commencer le test?",
                                      dialog.Yes | dialog.No)
                if rep == dialog.Yes:
                    pass
                elif rep == dialog.No:
                    return

                self.test_win = TestWindow(self, candidat, themes, timer_state, timer,
                                           number_of_questions, self.questions,
                                           self.series, self.theme_type)
                self.test_win.show()
                self.exit_flag = True
                self.master.hide()
                self.close()

        except Exception as e:
            print(e)

    def toggle_timer(self, event):
        """ Enable or disable timer """
        if event:
            self.time_combo.setEnabled(True)
        else:
            self.time_combo.setDisabled(True)

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

    def set_number_of_questions(self):
        """ Set  """
        number_themes = 0
        for checkbox in self.themes_checkbox_dict.values():
            if checkbox.isChecked():
                number_themes += 1

        num_questions_list = []
        if number_themes == 0:
            self.num_questions_combo.setDisabled(True)
        elif 0 < number_themes < 6:
            for i in range(number_themes, 50, 2):
                num_questions_list.append(str(i))
            self.num_questions_combo.setEnabled(True)
            self.num_questions_combo.clear()
            self.num_questions_combo.addItems(num_questions_list)
        else:
            for i in range(number_themes, number_themes * 6 + 1):
                if i % number_themes == 0:
                    num_questions_list.append(str(i))
            self.num_questions_combo.setEnabled(True)
            self.num_questions_combo.clear()
            self.num_questions_combo.addItems(num_questions_list)

        for i in range(0, self.num_questions_combo.count()):
            self.num_questions_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

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
            # self.theme_grp.setFixedSize(500, 480)
            self.set_number_of_questions()
        elif self.theme_combo.currentText() == "Choix d'une série":
            self.define_choice_frame.show()
            self.free_choice_frame.hide()
            # self.theme_grp.setFixedSize(500, 480)
            self.display_serie_details()
            self.num_questions_combo.setEnabled(True)
            self.num_questions_combo.clear()
            self.num_questions_combo.addItems(["20"])
            for i in range(0, self.num_questions_combo.count()):
                self.num_questions_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        if not self.exit_flag:
            self.master.enable_buttons()

        self.master.test_launcher_win = None


class TestWindow(QWidget):
    """ Test WIndow
    theme_type: 0 free / 1 serie
    """

    def __init__(self, master, candidat, themes, timer_state,
                 timer, number_of_questions, questions, series, theme_type):
        super().__init__()
        self.main_ui = master.master
        self.master = master
        self.candidat = candidat
        self.themes = themes
        self.theme_type = theme_type
        self.timer_state = timer_state
        self.timer = timer
        self.number_of_questions = number_of_questions
        self.questions = questions
        self.series = series

        self.test_questions_dict = dict()
        self.choosen_questions_list = list()
        self.question_index = 0
        self.responses_dict = dict()
        self.stopped_by_timer = False

        # #################### Window config
        # self.setFixedSize(820, 670)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(f"Examen du candidat: {self.candidat}")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # #################### Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # #################### Info Layout
        self.info_layout = QHBoxLayout()
        self.info_groupbox = QGroupBox()
        self.info_groupbox.setLayout(self.info_layout)
        self.main_layout.addWidget(self.info_groupbox, 1)

        # Info Layout Widgets
        self.question_number_label = QLabel()
        self.question_index_label = QLabel()
        self.number_question_asked = QLabel()
        self.time_left = QTime(0, 0, 0)
        self.time_left = self.time_left.addMSecs(TIME_DICT[self.timer] * 60000)
        self.timer_progressbar = QProgressBar()
        self.time_left_label = QLabel(self.time_left.toString("hh:mm:ss"))

        # Info Layout Widgets Config
        self.timer_progressbar.setFixedWidth(250)

        # Info Layout Widgets Placement
        self.info_layout.addWidget(self.question_number_label)
        self.info_layout.addWidget(self.question_index_label)
        self.info_layout.addWidget(self.number_question_asked)
        self.info_layout.addWidget(self.time_left_label)
        self.info_layout.addWidget(self.timer_progressbar)

        # #################### Image
        self.image_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_groupbox = QGroupBox()
        self.image_groupbox.setLayout(self.image_layout)
        self.image_layout.addWidget(self.image_label, 1, Qt.AlignCenter)
        self.main_layout.addWidget(self.image_groupbox, 5)

        # #################### Response Layout
        self.responses_layout = QVBoxLayout()
        self.responses_groupbox = QGroupBox("Réponses")
        self.responses_groupbox.setLayout(self.responses_layout)
        self.main_layout.addWidget(self.responses_groupbox, 2)

        # Response Layout Widgets
        self.responses_grp = QButtonGroup()
        self.response_1_checkbox = QCheckBox()
        self.response_2_checkbox = QCheckBox()
        self.response_3_checkbox = QCheckBox()
        self.response_4_checkbox = QCheckBox()
        self.no_response_checkbox = QCheckBox()
        self.responses_grp.addButton(self.response_1_checkbox, 0)
        self.responses_grp.addButton(self.response_2_checkbox, 1)
        self.responses_grp.addButton(self.response_3_checkbox, 2)
        self.responses_grp.addButton(self.response_4_checkbox, 3)
        self.responses_grp.addButton(self.no_response_checkbox, 5)
        # noinspection PyUnresolvedReferences
        self.responses_grp.buttonClicked.connect(self.save_response)

        # Response Layout Widgets Placement
        self.responses_layout.addWidget(self.response_1_checkbox)
        self.responses_layout.addWidget(self.response_2_checkbox)
        self.responses_layout.addWidget(self.response_3_checkbox)
        self.responses_layout.addWidget(self.response_4_checkbox)

        # #################### Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_groupbox = QGroupBox()
        self.buttons_groupbox.setLayout(self.buttons_layout)
        self.main_layout.addWidget(self.buttons_groupbox, 1)

        # Buttons Layout Widgets
        self.previous_button = QPushButton("Question précédente")
        self.recap_button = QPushButton("Récapitulatif")
        self.clear_response_button = QPushButton("Effacer réponse")
        self.terminate_button = QPushButton("Terminer")
        self.go_to_question = QComboBox()
        self.next_button = QPushButton("Question suivante")

        # Buttons Layout Widgets Placement
        self.buttons_layout.addWidget(self.previous_button)
        self.buttons_layout.addWidget(self.recap_button)
        self.buttons_layout.addWidget(self.clear_response_button)
        self.buttons_layout.addWidget(self.terminate_button)
        self.buttons_layout.addWidget(self.go_to_question)
        self.buttons_layout.addWidget(self.next_button)

        # Buttons config
        self.next_button.clicked.connect(self.increment_index)
        self.previous_button.clicked.connect(self.decrement_index)
        self.clear_response_button.clicked.connect(self.remove_response)
        self.go_to_question.setFixedWidth(60)
        self.go_to_question.addItems(str(i) for i in range(1, int(self.number_of_questions) + 1))
        self.go_to_question.setEditable(True)
        self.go_to_question.lineEdit().setReadOnly(True)
        self.go_to_question.lineEdit().setAlignment(Qt.AlignCenter)
        for i in range(0, self.go_to_question.count()):
            self.go_to_question.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        # noinspection PyUnresolvedReferences
        self.go_to_question.activated.connect(lambda: self.go_to(self.go_to_question.currentText()))

        # ################# Timer
        self.countdown = QTimer()
        self.countdown.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.countdown.timeout.connect(self.stop_test_by_timer)
        # self.countdown.setInterval(TIME_DICT[self.timer] * 60000)
        self.countdown.setInterval(3000)

        self.display_timer = QTimer()
        self.display_timer.setInterval(100)
        # noinspection PyUnresolvedReferences
        self.display_timer.timeout.connect(lambda: print(self.countdown.remainingTime()))

        if self.timer_state:
            self.countdown.start()
            self.display_timer.start()

        self.init_test_questions()
        self.display_first_question()

    def stop_test_by_timer(self):
        """ Stopped by timer """
        self.stopped_by_timer = True
        self.close()

    def go_to(self, index):
        """ Go to the index question """
        if int(index) - 1  < self.question_index or int(index) - 1 > self.question_index:
            self.question_index = int(index) - 1
            self.display_question()
        else:
            pass

    def remove_response(self):
        """ Remove response from responses_dict """
        self.no_response_checkbox.setChecked(True)
        if self.question_index in self.responses_dict:
            self.responses_dict.pop(self.question_index)
        self.number_question_asked.setText(f"Répondu à: {len(self.responses_dict)}/{self.number_of_questions}")

    def save_response(self):
        """ Save the response in the response dict """
        if self.no_response_checkbox.isChecked():
            return
        else:
            self.responses_dict[self.question_index] = {"button": self.responses_grp.checkedButton(),
                                                        "response": self.responses_grp.checkedId()}
        self.number_question_asked.setText(f"Répondu à: {len(self.responses_dict)}/{self.number_of_questions}")

    def display_first_question(self):
        """ Display the first question """
        self.previous_button.setDisabled(True)
        first = self.choosen_questions_list[0]
        self.question_number_label.setText(first["num"])
        self.question_index_label.setText(f"1/{self.number_of_questions}")
        self.number_question_asked.setText(f"Répondu à: 0/{self.number_of_questions}")
        pix = QPixmap(f"./questions/{first['num']}.png")
        pixmap = pix.scaled(IMAGE_SIZE, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.response_1_checkbox.setText(first["propositions"][0].replace('\n', ''))
        self.response_2_checkbox.setText(first["propositions"][1].replace('\n', ''))
        self.response_3_checkbox.setText(first["propositions"][2].replace('\n', ''))
        self.response_4_checkbox.setText(first["propositions"][3].replace('\n', ''))

    def increment_index(self):
        """ Increment Index """
        if self.question_index + 1 == int(self.number_of_questions):
            return
        else:
            self.question_index += 1
            self.display_question()

    def config_buttons(self):
        """ Enable/Disable Next/Previous Buttons """
        if self.question_index + 1 == int(self.number_of_questions):
            self.next_button.setDisabled(True)
            self.previous_button.setEnabled(True)
        elif self.question_index == 0:
            self.previous_button.setDisabled(True)
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(True)
            self.previous_button.setEnabled(True)

    def decrement_index(self):
        """ Decrement Index """
        if self.question_index == 0:
            return
        else:
            self.question_index -= 1
            self.display_question()

    def display_question(self):
        """ Display the next question """
        self.config_buttons()
        try:
            if self.question_index in self.responses_dict.keys():
                self.responses_dict[self.question_index]["button"].setChecked(True)
            else:
                self.no_response_checkbox.setChecked(True)

            next_question = self.choosen_questions_list[self.question_index]
            self.question_number_label.setText(next_question["num"])
            self.question_index_label.setText(f"{self.question_index + 1}/{self.number_of_questions}")
            pix = QPixmap(f"./questions/{next_question['num']}.png")
            pixmap = pix.scaled(IMAGE_SIZE, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.response_1_checkbox.setText(next_question["propositions"][0].replace('\n', ''))
            self.response_2_checkbox.setText(next_question["propositions"][1].replace('\n', ''))
            self.response_3_checkbox.setText(next_question["propositions"][2].replace('\n', ''))
            self.response_4_checkbox.setText(next_question["propositions"][3].replace('\n', ''))
            self.adjustSize()
            self.setFixedSize(self.width(), self.height())
        except Exception as e:
            print("display_question", e)

    def init_test_questions(self):
        """ Init questions """
        try:
            self.choosen_questions_list = []

            # if free themes choosen
            if self.theme_type == 0:
                # get the number of question by theme
                question_by_theme = int(self.number_of_questions) // len(self.themes)

                # get all the questions for each theme
                for theme in self.themes:
                    self.test_questions_dict[theme] = []
                    for question in self.questions["questions"]:
                        if str(question["themeNum"]) == theme:
                            self.test_questions_dict[theme].append(question)

                # get random questions for each theme
                for theme in self.themes:
                    choosen_question = []
                    for index in range(0, question_by_theme):
                        num = random.randint(0, len(self.test_questions_dict[theme]) - 1)
                        while num in choosen_question:
                            num = random.randint(0, len(self.test_questions_dict[theme]) - 1)
                        choosen_question.append(num)
                        q = self.test_questions_dict[theme][num]
                        self.choosen_questions_list.append(q)

            # if serie choosen
            elif self.theme_type == 1:
                for quest_num in self.series[self.themes[0]].values():
                    for question in self.questions["questions"]:
                        if question["num"] == quest_num:
                            self.choosen_questions_list.append(question)
        except Exception as e:
            print("init_test_questions", e)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        if self.stopped_by_timer:
            self.countdown.stop()
            self.display_timer.stop()
            timeout_win = QMessageBox(self)
            timeout_win.setText("Fin du temps rêglementaire,\n"
                                "voir les résultats.")
            timeout_win.setWindowTitle("Fin du temps")
            timeout_win.setIcon(QMessageBox.Icon.Information)
            timeout_win.setModal(True)
            timeout_win.exec_()
        else:
            dialog = QMessageBox()
            rep = dialog.question(self,
                                  "Arrèter le test",
                                  "Voullez vous arrèter le test,\n"
                                  "les résultats ne seront pas sauvegarder",
                                  dialog.StandardButton.Yes | dialog.StandardButton.No)
            if rep == dialog.StandardButton.Yes:
                self.countdown.stop()
                self.display_timer.stop()
            elif rep == dialog.StandardButton.No:
                QCloseEvent.ignore(a0)
                return

        self.main_ui.enable_buttons()
        self.main_ui.show()


class RecapWindow(QWidget):
    """ Recap Window """

    def __init__(self, master):
        super().__init__()
        self.master = master
