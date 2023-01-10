""" All Questions Window """
import json

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QTableWidget, QWidget,
                             QTableWidgetItem, QHeaderView, QVBoxLayout,
                             QLabel, QGroupBox, QPushButton, QScrollBar,
                             QGridLayout, QComboBox)

from modules.contants import *


class AllQuestionsWindow(QWidget):
    """ All Questions Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # Variables
        self.questions = dict()
        self.question_win = None

        # ### Window config
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Liste complète des questions")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Combo themes
        self.themes_combo = QComboBox()
        self.themes_combo.addItem("Toutes les questions")
        for item in THEMES_LIST:
            self.themes_combo.addItem(THEMES_DICT[item])
        for i in range(0, self.themes_combo.count()):
            self.themes_combo.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)
        self.themes_combo.setEditable(True)
        self.themes_combo.lineEdit().setReadOnly(True)
        self.themes_combo.setMaxVisibleItems(21)
        self.themes_combo.lineEdit().setAlignment(Qt.AlignCenter)
        # noinspection PyUnresolvedReferences
        self.themes_combo.activated.connect(self.display_selected_theme)

        self.main_layout.addWidget(self.themes_combo)

        # Main layout Widgets
        self.questions_table = QTableWidget()
        self.questions_table.setFixedSize(QSize(780, 549))
        self.questions_table.setSortingEnabled(False)
        self.questions_table.setColumnCount(2)
        self.questions_table.horizontalHeader().setStretchLastSection(True)
        self.questions_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.questions_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.num_header = QTableWidgetItem("Numéro")
        self.num_header.setFont(QFont("Lato", 12))
        self.quest_header = QTableWidgetItem("Question")
        self.quest_header.setFont(QFont("Lato", 12))
        self.questions_table.setHorizontalHeaderItem(0, self.num_header)
        self.questions_table.setHorizontalHeaderItem(1, self.quest_header)
        self.questions_table.verticalHeader().setVisible(False)
        self.questions_table.setAlternatingRowColors(True)
        self.questions_table_scrollbar = QScrollBar()
        self.questions_table_scrollbar.setObjectName("QuestionScrollBar")
        self.questions_table.setVerticalScrollBar(self.questions_table_scrollbar)

        self.main_layout.addWidget(self.questions_table, 1, Qt.AlignmentFlag.AlignCenter)

        self.create_questions_table()
        self.questions_table.selectRow(0)
        self.questions_table.clicked.connect(lambda:
                                             self.open_selected_question(self.questions_table.currentIndex().row()))
        # noinspection PyUnresolvedReferences
        self.questions_table.activated.connect(lambda:
                                             self.open_selected_question(self.questions_table.currentIndex().row()))

    def open_selected_question(self, index):
        """ Open selected question in a new window """
        info_question = self.questions["questions"][index]
        question = info_question["question"]
        num = info_question["num"]
        propositions = info_question["propositions"]
        reponse = info_question["reponse"]
        theme_num = info_question["themeNum"]
        commentaire = info_question["commentaire"]
        cours = info_question["cours"]

        if self.question_win is not None:
            self.question_win.current_index = index
            self.question_win.display_question()
            self.question_win.config_btns()
            self.question_win.adjustSize()
            # self.question_win.close()
        else:
            self.question_win = QuestionWindow(self, question, num, propositions, reponse,
                                               theme_num, commentaire, cours, index)
            # self.hide()
            self.question_win.show()

    def display_selected_theme(self):
        """ Display questions according to the theme """
        if self.themes_combo.currentText() == "Toutes les questions":
            self.create_questions_table()
            return
        self.questions = {"questions": []}
        reverse_themes_dict = {}
        for key, value in THEMES_DICT.items():
            reverse_themes_dict[value] = key

        with open("./questions/questions.json", "r") as questions_file:
            questions = json.load(questions_file)

        for question in questions["questions"]:
            if int(question["themeNum"]) == int(reverse_themes_dict[self.themes_combo.currentText()]):
                self.questions["questions"].append(question)

        self.questions_table.setRowCount(len(self.questions["questions"]))

        row = 0
        for question in self.questions["questions"]:
            num = question["num"]
            quest = question["question"]
            num_item = QTableWidgetItem(num)
            quest_item = QTableWidgetItem(quest)
            num_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            quest_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            num_item.setTextAlignment(Qt.AlignCenter)
            quest_item.setTextAlignment(Qt.AlignCenter)

            self.questions_table.setItem(row, 0, num_item)
            self.questions_table.setItem(row, 1, quest_item)
            row += 1

        number_questions = len(self.questions["questions"])
        version = str(questions["version"].split("T")[0])
        self.setWindowTitle(f"{number_questions} questions dans ce thème- version: {version}")

        if self.question_win is not None:
            self.question_win.display_question()
            self.question_win.config_btns()

    def create_questions_table(self):
        """ Create the questions table """
        try:
            with open("./questions/questions.json", "r") as questions_file:
                self.questions = json.load(questions_file)
                self.questions_table.setRowCount(len(self.questions["questions"]))

                row = 0
                for question in self.questions["questions"]:
                    num = question["num"]
                    quest = question["question"]
                    num_item = QTableWidgetItem(num)
                    quest_item = QTableWidgetItem(quest)
                    num_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    quest_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    num_item.setTextAlignment(Qt.AlignCenter)
                    quest_item.setTextAlignment(Qt.AlignCenter)

                    self.questions_table.setItem(row, 0, num_item)
                    self.questions_table.setItem(row, 1, quest_item)
                    row += 1

            number_questions = self.questions["nbQuestions"]
            version = str(self.questions["version"].split("T")[0])
            self.setWindowTitle(f"Liste complète des {number_questions} questions - version: {version}")

        except FileNotFoundError as error:
            print(error)
        except KeyError as error:
            print(error)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        #self.master.show()
        if self.question_win is not None:
            self.question_win.close()
        self.master.all_questions_win = None
        self.master.enable_buttons()


class QuestionWindow(QWidget):
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

        # ### Window config
        self.setFixedSize(QSize(800, 850))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(f"Question numéro: {self.num}")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setUpdatesEnabled(True)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Image Label
        self.img_label = QLabel()
        self.img_label.setFixedSize(770, 350)
        self.img_label.setPixmap(QPixmap(f"./questions/{num}.png"))
        self.main_layout.addWidget(self.img_label, 5, Qt.AlignCenter)

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

        self.num_quest_label_1.setObjectName("BlackLabel")
        self.response_label_1.setObjectName("BlackLabel")
        self.family_label_1.setObjectName("BlackLabel")
        self.family_num_label_1.setObjectName("BlackLabel")
        self.num_quest_label_2.setObjectName("BlackLabel")
        self.response_label_2.setObjectName("BlackLabel")
        self.family_label_2.setObjectName("BlackLabel")
        self.family_num_label_2.setObjectName("BlackLabel")

        self.num_quest_label_2.setWordWrap(True)
        self.response_label_2.setWordWrap(True)
        self.family_label_2.setWordWrap(True)
        self.family_num_label_2.setWordWrap(True)
        # self.family_label_2.setFixedWidth(150)

        self.detail_layout.addWidget(self.num_quest_label_1, 0, 0, Qt.AlignLeft)
        self.detail_layout.addWidget( self.response_label_1, 1, 0, Qt.AlignLeft)
        self.detail_layout.addWidget( self.family_label_1, 3, 0, Qt.AlignLeft)
        self.detail_layout.addWidget(self.family_num_label_1, 2, 0, Qt.AlignLeft)
        self.detail_layout.addWidget(self.num_quest_label_2, 0, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.response_label_2, 1, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.family_num_label_2, 2, 1, Qt.AlignCenter)
        self.detail_layout.addWidget(self.family_label_2, 3, 1, Qt.AlignJustify)

        # Comment Layout
        self.comment_group = QGroupBox("Commentaire")
        self.comment_layout = QHBoxLayout()

        if self.commentaire is None:
            self.comment_label = QLabel(f"{self.cours}")
        else:
            self.comment_label = QLabel(f"{self.commentaire}\n{self.cours}")
        self.comment_label.setObjectName("BlackLabel")
        self.comment_label.setWordWrap(True)
        self.comment_label.setAlignment(Qt.AlignJustify)
        self.comment_group.setLayout(self.comment_layout)
        self.comment_layout.addWidget(self.comment_label, 1)
        self.detail_comment_layout.addWidget(self.comment_group, 2)

        # Response Layout
        self.responses_group = QGroupBox("Réponses")
        self.responses_layout = QVBoxLayout()
        self.responses_group.setLayout(self.responses_layout)
        self.main_layout.addWidget(self.responses_group, 1)

        self.choice_1 = QLabel(f"1:\t" + self.propositions[0].replace('\n', ''))
        self.choice_2 = QLabel(f"2:\t" + self.propositions[1].replace('\n', ''))
        self.choice_3 = QLabel(f"3:\t" + self.propositions[2].replace('\n', ''))
        self.choice_4 = QLabel(f"4:\t" + self.propositions[3].replace('\n', ''))
        self.choice_1.setObjectName("BlackLabel")
        self.choice_2.setObjectName("BlackLabel")
        self.choice_3.setObjectName("BlackLabel")
        self.choice_4.setObjectName("BlackLabel")
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
        if self.current_index >= len(self.master.questions["questions"]):
            self.current_index = len(self.master.questions["questions"]) - 1

        info_question = self.master.questions["questions"][self.current_index]
        num = info_question["num"]
        propositions = info_question["propositions"]
        reponse = info_question["reponse"]
        theme_num = info_question["themeNum"]
        commentaire = info_question["commentaire"]
        cours = info_question["cours"]

        self.img_label.setPixmap(QPixmap(f"./questions/{num}.png"))
        self.choice_1.setText(f"1:\t" + propositions[0].replace('\n', ''))
        self.choice_2.setText(f"2:\t" + propositions[1].replace('\n', ''))
        self.choice_3.setText(f"3:\t" + propositions[2].replace('\n', ''))
        self.choice_4.setText(f"4:\t" + propositions[3].replace('\n', ''))

        self.num_quest_label_2.setText(f"{num}")
        self.response_label_2.setText(f"{str(int(reponse) + 1)}")
        self.family_num_label_2.setText(f"{theme_num}")
        self.family_label_2.setText(f"{THEMES_DICT[theme_num]}")
        if commentaire is None:
            self.comment_label.setText(f"{cours}")
        else:
            self.comment_label.setText(f"{commentaire}\n{cours}")
        self.setWindowTitle(f"Question numéro: {num}")

        self.master.questions_table.selectRow(self.current_index)

    def config_btns(self):
        """ Enable or disable buttons according to the current index """
        if self.current_index == len(self.master.questions["questions"]) - 1:
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
        self.master.question_win = None
