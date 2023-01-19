""" Test Windows """
import random

from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon, QCloseEvent, QPixmap, QFont, QColor
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
                             QPushButton, QComboBox, QFrame, QToolBox,
                             QCheckBox, QLabel, QProgressBar, QButtonGroup,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QScrollArea, QGridLayout)

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
                                          "entre chaques thèmes.\n\nR = Règlementation\nT = Technique")
        self.serie_detail_label = QLabel()
        self.serie_detail_label.setWordWrap(True)
        self.serie_detail_label.setAlignment(Qt.AlignCenter)
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
        text = "Série "
        serie = self.define_choice_combo.currentText()
        if serie.startswith("R"):
            text += "Règlementation "
            self.time_combo.setCurrentIndex(2)
        elif serie.startswith("T"):
            text += "Technique "
            self.time_combo.setCurrentIndex(4)

        text += serie[1] + serie[2] + "\n\n"

        count = 0
        for question, num_question in self.series[self.define_choice_combo.currentText()].items():
            if count % 2 == 0:
                text += f"{question}: {num_question}" + " " * 4
            else:
                text += f"{question}: {num_question}\n"
            count += 1
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
        for themes in SEPARATED_THEME_DICT.items():
                for theme in themes[1].items():
                    if theme:
                        if theme[0] in SEPARATED_THEME_DICT["Reglementation"]:
                            self.themes_checkbox_dict[f"{theme[0]}"].setChecked(event)

    def select_technique_themes(self, event):
        """ Select technique themes """
        for themes in SEPARATED_THEME_DICT.items():
            for theme in themes[1].items():
                if theme:
                    if theme[0] in SEPARATED_THEME_DICT["Technique"]:
                        self.themes_checkbox_dict[f"{theme[0]}"].setChecked(event)

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

    def __init__(self, master, candidat, themes,
                 timer_state, timer, number_of_questions,
                 questions, series, theme_type):
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
        self.stopped_by_user = False
        self.recap_win = None
        self.result_win = None

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

        # Info Layout Widgets Config
        self.timer_progressbar.setFixedWidth(250)

        if self.timer_state:
            self.timer_progressbar.setTextVisible(True)
            self.timer_progressbar.setMaximum(TIME_DICT[self.timer] * 60000)
            self.timer_progressbar.setMinimum(0)
            self.timer_progressbar.setValue(0)
            self.time_left_label = QLabel(self.time_left.toString("hh:mm:ss"))
        else:
            self.timer_progressbar.setTextVisible(False)
            self.timer_progressbar.setValue(0)
            self.time_left_label = QLabel("Compte à rebourd désactivé")

        # Info Layout Widgets Placement
        self.info_layout.addWidget(self.question_number_label, 1, Qt.AlignCenter)
        self.info_layout.addWidget(self.question_index_label, 2, Qt.AlignCenter)
        self.info_layout.addWidget(self.number_question_asked, 2, Qt.AlignCenter)
        self.info_layout.addWidget(self.time_left_label, 2, Qt.AlignCenter)
        if self.timer_state:
            self.info_layout.addWidget(self.timer_progressbar, 3, Qt.AlignCenter)

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
        self.recap_button.clicked.connect(self.display_recap)
        self.terminate_button.clicked.connect(self.stop_test_by_user)

        # ################# Timer
        self.countdown = QTimer()
        self.countdown.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.countdown.timeout.connect(self.stop_test_by_timer)
        self.countdown.setInterval(TIME_DICT[self.timer] * 60000)

        self.display_timer = QTimer()
        self.display_timer.setInterval(100)
        # noinspection PyUnresolvedReferences
        self.display_timer.timeout.connect(self.display_remaining_time)

        if self.timer_state:
            self.countdown.start()
            self.display_timer.start()

        self.init_test_questions()
        self.display_first_question()
        self.config_buttons()

    def display_recap(self):
        """ Display the recap Window """
        if self.recap_win is not None:
            return
        self.recap_win = RecapWindow(self, self.number_of_questions, self.responses_dict, self.choosen_questions_list)
        self.recap_win.show()

    def display_remaining_time(self):
        """ Display the remaining time """
        self.time_left = QTime(0, 0, 0)
        self.time_left = self.time_left.addMSecs(self.countdown.remainingTime())
        self.time_left_label.setText(self.time_left.toString("hh:mm:ss"))
        self.timer_progressbar.setValue(self.countdown.remainingTime())

    def stop_test_by_timer(self):
        """ Stopped by timer """
        self.stopped_by_timer = True
        self.close()

    def stop_test_by_user(self):
        """ Stopped by timer """
        self.stopped_by_user = True
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

        if self.recap_win is not None:
            self.recap_win.reload_table(self.responses_dict)

    def save_response(self):
        """ Save the response in the response dict """
        if self.no_response_checkbox.isChecked():
            return
        else:
            self.responses_dict[self.question_index] = {"button": self.responses_grp.checkedButton(),
                                                        "response": self.responses_grp.checkedId()}
        self.number_question_asked.setText(f"Répondu à: {len(self.responses_dict)}/{self.number_of_questions}")

        if self.recap_win is not None:
            self.recap_win.reload_table(self.responses_dict)

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
        if self.number_of_questions == 1:
            self.next_button.setDisabled(True)
            self.previous_button.setDisabled(True)
        elif self.question_index + 1 == int(self.number_of_questions):
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
            self.go_to_question.setCurrentIndex(self.question_index)
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

    def display_result_win(self):
        """ Display the resul Window """
        self.main_ui.result_win = ResultWindow(self.main_ui, self.candidat,
                                               self.choosen_questions_list,
                                               self.responses_dict,
                                               self.number_of_questions)
        self.main_ui.result_win.show()

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
            self.main_ui.show()
            self.display_result_win()

        elif self.stopped_by_user:
            dialog = QMessageBox()
            rep = dialog.question(self,
                                  "Terminer le test",
                                  f"{self.candidat}, voullez vous terminer l'épreuve et voir le résultat ?",
                                  dialog.StandardButton.Yes | dialog.StandardButton.No)
            if rep == dialog.StandardButton.Yes:
                self.countdown.stop()
                self.display_timer.stop()
                self.main_ui.show()
                self.display_result_win()
            elif rep == dialog.StandardButton.No:
                self.stopped_by_user = False
                QCloseEvent.ignore(a0)
                return

        else:
            dialog = QMessageBox()
            rep = dialog.question(self,
                                  "Arrèter le test",
                                  "Voullez vous arrêter le test,\n"
                                  "les résultats ne seront pas sauvegardé",
                                  dialog.StandardButton.Yes | dialog.StandardButton.No)
            if rep == dialog.StandardButton.Yes:
                self.countdown.stop()
                self.display_timer.stop()
                self.main_ui.enable_buttons()
                self.main_ui.show()
            elif rep == dialog.StandardButton.No:
                QCloseEvent.ignore(a0)
                return

        if self.recap_win is not None:
            self.recap_win.close()


class RecapWindow(QWidget):
    """ Recap Window """

    def __init__(self, master, number_of_questions,
                 responses_dict, questions_list):
        super().__init__()
        self.master = master
        self.number_of_questions = number_of_questions
        self.responses_dict = responses_dict
        self.questions_list = questions_list

        self.setFixedSize(320, 420)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Table responses
        self.table_response = QTableWidget()
        self.table_response.setFixedSize(QSize(300, 400))
        self.table_response.setSortingEnabled(False)
        self.table_response.setColumnCount(2)
        self.table_response.setRowCount(int(self.number_of_questions))
        self.table_response.horizontalHeader().setStretchLastSection(True)
        self.table_response.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_response.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.index_header = QTableWidgetItem("Numéro question")
        self.index_header.setFont(QFont("Lato", 12))
        self.awsered_header = QTableWidgetItem("Réponse")
        self.awsered_header.setFont(QFont("Lato", 12))
        self.table_response.setHorizontalHeaderItem(0, self.index_header)
        self.table_response.setHorizontalHeaderItem(1, self.awsered_header)
        self.table_response.verticalHeader().setVisible(False)
        self.table_response.setAlternatingRowColors(True)

        self.main_layout.addWidget(self.table_response)
        self.init_table()

    def reload_table(self, response):
        """ Reload the table  """
        self.responses_dict = response
        self.init_table()

    def init_table(self):
        """ Initialize the table """
        try:
            row = 0
            for question in self.questions_list:
                index_question = self.questions_list.index(question)
                index = QTableWidgetItem(str(index_question + 1))
                if index_question in self.responses_dict.keys():
                    indicatif_item = QTableWidgetItem("X")
                else:
                    indicatif_item = QTableWidgetItem("")

                indicatif_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                indicatif_item.setTextAlignment(Qt.AlignCenter)
                index.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                index.setTextAlignment(Qt.AlignCenter)

                self.table_response.setItem(row, 0, index)
                self.table_response.setItem(row, 1, indicatif_item)
                row += 1
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.recap_win = None


class ResultWindow(QWidget):
    """ Result Window """

    def __init__(self, master, candidat,
                 questions_list, responses_dict,
                 number_of_questions):
        super().__init__()

        self.main_ui = master
        self.candidat = candidat
        self.questions_list = questions_list
        self.responses_dict = responses_dict
        self.number_of_questions = number_of_questions

        self.details_win = None

        # #################### Window config
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Résultat de l'épreuve")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Widgets
        self.main_label = QLabel()
        self.secondary_label = QLabel("Félicitation, vous avez réussis l'épreuve.")
        self.result_table = QTableWidget()
        self.view_details_btn = QPushButton("Voir les résultats en détail")

        self.main_layout.addWidget(self.main_label, 0, Qt.AlignCenter)
        self.main_layout.addWidget(self.secondary_label, 0, Qt.AlignCenter)
        self.main_layout.addWidget(self.result_table)
        self.main_layout.addWidget(self.view_details_btn)

        main_label_font = self.main_label.font()
        main_label_font.setPointSize(40)
        self.main_label.setFont(main_label_font)

        self.result_table.setFixedSize(QSize(380, 270))
        self.result_table.setSortingEnabled(False)
        self.result_table.setColumnCount(1)
        self.result_table.setRowCount(int(self.number_of_questions))
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.index_header = QTableWidgetItem("Numéro question")
        self.index_header.setFont(QFont("Lato", 12))
        self.result_table.setHorizontalHeaderItem(0, self.index_header)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setAlternatingRowColors(True)

        self.view_details_btn.clicked.connect(self.display_details)

        self.make_result()
        self.init_table()

    def display_details(self):
        """ Display the detail result Window """
        try:
            if self.details_win is not None:
                self.details_win.close()

            question = self.questions_list[0]
            num = question["num"]
            propositions = question["propositions"]
            reponse = question["reponse"]
            theme_num = question["themeNum"]
            commentaire = question["commentaire"]
            cours = question["cours"]
            self.details_win = ResultDetailsWindow(self, question, num, propositions, reponse,
                                                   theme_num, commentaire, cours, 0)
            self.details_win.show()
            self.view_details_btn.setDisabled(True)
        except Exception as e:
            print(e)

    def init_table(self):
        """ Initialize the table """
        try:
            row = 0
            for question in self.questions_list:
                index_question = self.questions_list.index(question)
                index = QTableWidgetItem("Question numéro: " + str(index_question + 1))
                index.setFlags(Qt.ItemIsEnabled)
                index.setTextAlignment(Qt.AlignCenter)
                self.result_table.setItem(row, 0, index)
                self.result_table.item(row, 0).setForeground(QColor(255, 255, 255))

                if self.questions_list.index(question) in self.responses_dict.keys():
                    if self.responses_dict[index_question]["response"] == question["reponse"]:
                            self.result_table.item(row, 0).setBackground(QColor(0, 200, 0))
                    else:
                        self.result_table.item(row, 0).setBackground(QColor(200, 0, 0))
                else:
                    self.result_table.item(row, 0).setBackground(QColor(200, 0, 0))
                row += 1

        except Exception as e:
            print(e)

    def save_result(self):
        """ Save result  """
        pass

    def make_result(self):
        """ Calculate the average and display it """
        try:
            points = 0
            for question in self.questions_list:
                index_question = self.questions_list.index(question)
                if index_question in self.responses_dict.keys():
                    if self.responses_dict[index_question]["response"] == question["reponse"]:
                        points += 1

            average_int = (points * 20) // int(self.number_of_questions)
            average_float = (points * 20) / int(self.number_of_questions)
            rest = (points * 20) % int(self.number_of_questions)

            if rest == 0:
                self.main_label.setText(f"{average_int}/20")
            else:
                self.main_label.setText(f"{(round(average_float, 1))}/20")

            if average_float < 10:
                self.secondary_label.setText("Désolé, vous avez échoué à l'épreuve.")
            else:
                self.secondary_label.setText("Félicitation, vous avez réussis l'épreuve.")

        except Exception as e:
            print(e)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        if self.details_win is not None:
            self.details_win.close()
        self.main_ui.result_win = None
        self.main_ui.enable_buttons()


class ResultDetailsWindow(QWidget):
    """ Question Window """

    def __init__(self, master, question, num, propositions,
                 reponse, theme_num, commentaire, cours, index):
        super().__init__()
        self.master = master
        self.num = num
        self.question = question
        self.propositions = propositions
        self.reponse = reponse
        self.theme_num = theme_num
        self.commentaire = commentaire
        self.cours = cours
        self.current_index = index

        self.questions_list = self.master.questions_list
        self.responses_dict = self.master.responses_dict

        # ### Window config
        self.setFixedSize(QSize(820, 800))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(f"Question numéro: {self.current_index + 1}")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setUpdatesEnabled(True)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Image Label
        self.img_groupbox = QGroupBox()
        self.img_label = QLabel()
        self.img_layout = QVBoxLayout()
        self.img_groupbox.setLayout(self.img_layout)
        self.img_layout.addWidget(self.img_label)
        # self.img_label.setFixedSize(770, 350)
        pix = QPixmap(f"./questions/{num}.png")
        pixmap = pix.scaled(IMAGE_SIZE, Qt.KeepAspectRatio)
        self.img_label.setPixmap(pixmap)
        self.main_layout.addWidget(self.img_groupbox, 5, Qt.AlignCenter)

        # Detail Comment Layout
        self.detail_comment_layout = QHBoxLayout()
        self.main_layout.addLayout(self.detail_comment_layout, 3)

        # Details layout
        self.detail_group = QGroupBox("Détails")
        self.detail_layout = QGridLayout()
        self.detail_group.setLayout(self.detail_layout)
        self.detail_comment_layout.addWidget(self.detail_group, 1)

        self.num_quest_label_1 = QLabel("N° Question:")
        self.response_label_1 = QLabel(f"Réponse:")
        self.family_num_label_1 = QLabel(f"Num Famille:")
        self.family_label_1 = QLabel(f"Famille:")
        self.num_quest_label_2 = QLabel(f"{self.num}")
        self.response_label_2 = QLabel(f"{str(int(self.reponse) + 1)}")
        self.family_num_label_2 = QLabel(f"{self.theme_num}")
        self.family_label_2 = QLabel(THEMES_DICT[self.theme_num])

        self.num_quest_label_2.setWordWrap(True)
        self.response_label_2.setWordWrap(True)
        self.family_label_2.setWordWrap(True)
        self.family_num_label_2.setWordWrap(True)
        self.family_label_2.setAlignment(Qt.AlignCenter)
        # self.family_label_2.setFixedSize(150, 0)

        self.detail_layout.addWidget(self.num_quest_label_1, 0, 0, Qt.AlignLeft)
        self.detail_layout.addWidget( self.response_label_1, 1, 0, Qt.AlignLeft)
        self.detail_layout.addWidget( self.family_label_1, 3, 0, Qt.AlignLeft)
        self.detail_layout.addWidget(self.family_num_label_1, 2, 0, Qt.AlignLeft)
        self.detail_layout.addWidget(self.num_quest_label_2, 0, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.response_label_2, 1, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.family_num_label_2, 2, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.family_label_2, 3, 1, Qt.AlignCenter)

        # Comment Layout
        self.comment_group = QGroupBox("Commentaire")
        self.comment_layout = QHBoxLayout()
        self.comment_layout.setContentsMargins(1, 1, 1, 1)

        if self.commentaire is None:
            self.comment_label = QLabel(f"{self.cours}")
        else:
            self.comment_label = QLabel(f"{self.commentaire}\n{self.cours}")
        self.scroll = QScrollArea()
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.comment_label)
        self.comment_label.setObjectName("BlackLabel")
        self.comment_label.setContentsMargins(10, 10, 10, 10)
        self.comment_label.setWordWrap(True)
        self.comment_label.setAlignment(Qt.AlignJustify)
        self.comment_group.setLayout(self.comment_layout)
        self.comment_layout.addWidget(self.scroll, 1)
        self.detail_comment_layout.addWidget(self.comment_group, 2)

        # Response Layout
        self.responses_group = QGroupBox("Réponses")
        self.responses_layout = QVBoxLayout()
        self.responses_group.setLayout(self.responses_layout)
        self.main_layout.addWidget(self.responses_group, 1)

        self.choice_1 = QLabel(f"1: " + self.propositions[0].replace('\n', ''))
        self.choice_2 = QLabel(f"2: " + self.propositions[1].replace('\n', ''))
        self.choice_3 = QLabel(f"3: " + self.propositions[2].replace('\n', ''))
        self.choice_4 = QLabel(f"4: " + self.propositions[3].replace('\n', ''))

        self.responses_layout.addWidget(self.choice_1, 1, Qt.AlignLeft)
        self.responses_layout.addWidget(self.choice_2, 1, Qt.AlignLeft)
        self.responses_layout.addWidget(self.choice_3, 1, Qt.AlignLeft)
        self.responses_layout.addWidget(self.choice_4, 1, Qt.AlignLeft)

        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)
        self.previous_btn = QPushButton("Précédente question")
        self.next_btn = QPushButton("Prochaine question")
        self.buttons_layout.addWidget(self.previous_btn, 1)
        self.buttons_layout.addWidget(self.next_btn, 1)
        self.next_btn.clicked.connect(self.display_next_question)
        self.previous_btn.clicked.connect(self.display_previous_question)

        self.config_btns()
        self.set_response_color()

    def display_next_question(self):
        """ Display the next question """
        self.current_index += 1
        self.display_question()
        self.config_btns()
        self.adjustSize()
        # self.setFixedSize(self.width(), self.height())

    def display_previous_question(self):
        """ Display the previous question """
        self.current_index -= 1
        self.display_question()
        self.config_btns()
        self.adjustSize()
        # self.setFixedSize(self.width(), self.height())

    def display_question(self):
        """ Get the info and display it """
        if self.current_index >= len(self.questions_list):
            self.current_index = len(self.questions_list)

        info_question = self.questions_list[self.current_index]
        num = info_question["num"]
        propositions = info_question["propositions"]
        reponse = info_question["reponse"]
        theme_num = info_question["themeNum"]
        commentaire = info_question["commentaire"]
        cours = info_question["cours"]
        pix = QPixmap(f"./questions/{num}.png")
        pixmap = pix.scaled(IMAGE_SIZE, Qt.KeepAspectRatio)

        self.img_label.setPixmap(pixmap)
        self.choice_1.setText(f"1: " + propositions[0].replace('\n', ''))
        self.choice_2.setText(f"2: " + propositions[1].replace('\n', ''))
        self.choice_3.setText(f"3: " + propositions[2].replace('\n', ''))
        self.choice_4.setText(f"4: " + propositions[3].replace('\n', ''))

        self.num_quest_label_2.setText(f"{num}")
        self.response_label_2.setText(f"{str(int(reponse) + 1)}")
        self.family_num_label_2.setText(f"{theme_num}")
        self.family_label_2.setText(f"{THEMES_DICT[theme_num]}")
        if commentaire is None:
            self.comment_label.setText(f"{cours}")
        else:
            self.comment_label.setText(f"{commentaire}\n{cours}")
        self.setWindowTitle(f"Question numéro: {self.current_index + 1}")
        self.set_response_color()

    def set_response_color(self):
        """ Set the color of the good and bad responses """
        reponse = self.questions_list[self.current_index]["reponse"]
        try:
            if reponse == 0:
                self.choice_1.setStyleSheet("color: white; background-color: green")
            elif self.responses_dict[self.current_index]["response"] == 0 and reponse != 0:
                self.choice_1.setStyleSheet("color: white; background-color: red")
            else:
                self.choice_1.setStyleSheet("")
        except KeyError:
            self.choice_1.setStyleSheet("")
            self.setWindowTitle(f"Question numéro: {self.current_index + 1} - "
                                f"Vous n'avez pas répondu à cette question")

        try:
            if reponse == 1:
                self.choice_2.setStyleSheet("color: white; background-color: green")
            elif self.responses_dict[self.current_index]["response"] == 1 and reponse != 1:
                self.choice_2.setStyleSheet("color: white; background-color: red")
            else:
                self.choice_2.setStyleSheet("")
        except KeyError:
            self.choice_2.setStyleSheet("")
            self.setWindowTitle(f"Question numéro: {self.current_index + 1} - "
                                f"Vous n'avez pas répondu à cette question")

        try:
            if reponse == 2:
                self.choice_3.setStyleSheet("color: white; background-color: green")
            elif self.responses_dict[self.current_index]["response"] == 2 and reponse != 2:
                self.choice_3.setStyleSheet("color: white; background-color: red")
            else:
                self.choice_3.setStyleSheet("")
        except KeyError:
            self.choice_3.setStyleSheet("")
            self.setWindowTitle(f"Question numéro: {self.current_index + 1} - "
                                f"Vous n'avez pas répondu à cette question")

        try:
            if reponse == 3:
                self.choice_4.setStyleSheet("color: white; background-color: green")
            elif self.responses_dict[self.current_index]["response"] == 3 and reponse != 3:
                self.choice_4.setStyleSheet("color: white; background-color: red")
            else:
                self.choice_4.setStyleSheet("")
        except KeyError:
            self.choice_4.setStyleSheet("")
            self.setWindowTitle(f"Question numéro: {self.current_index + 1} - "
                                f"Vous n'avez pas répondu à cette question")

    def config_btns(self):
        """ Enable or disable buttons according to the current index """
        if self.current_index == len(self.questions_list) - 1:
            self.next_btn.setDisabled(True)
        else:
            self.next_btn.setDisabled(False)

        if self.current_index == 0:
            self.previous_btn.setDisabled(True)
        else:
            self.previous_btn.setDisabled(False)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        #self.master.show()
        self.master.view_details_btn.setEnabled(True)
        self.master.details_win = None
