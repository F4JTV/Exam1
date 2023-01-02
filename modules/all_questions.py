""" All Questions Window """
import json

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont, QPixmap
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QVBoxLayout, QLabel, QGroupBox)


class AllQuestionsWindow(QDialog):
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
        self.setModal(True)
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 800, 600)

        # Main Layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Main layout Widgets
        self.questions_table = QTableWidget()
        self.questions_table.setFixedSize(QSize(780, 550))
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

        self.main_layout.addWidget(self.questions_table, 1, Qt.AlignmentFlag.AlignCenter)
        self.create_questions_table()
        self.questions_table.clicked.connect(lambda:
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
            self.question_win.close()
        else:
            self.question_win = AllQuestionsWindow.QuestionWindow(self, question, num, propositions, reponse,
                                                                  theme_num, commentaire, cours, index)
            self.hide()
            self.question_win.show()

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
        self.master.all_questions_win = None

    class QuestionWindow(QDialog):
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

            self.themes = {
                305: "Questions entrainement",
                206: "\u00c9lectricit\u00e9 de base",
                202: "Groupements de r\u00e9sistances",
                207: "Courants alternatifs",
                208: "Condensateurs et bobines (s\u00e9par\u00e9s)",
                209: "Transformateurs, ampli op, filtres RC LC RLC",
                205: "R\u00f4le des diff\u00e9rents \u00e9tages RF, haut-parleur, micro",
                203: "Diodes et transistors, classes d'amplification",
                210: "Antennes, couplage, propagation, ligne de transmis",
                204: "Synoptiques d'\u00e9metteurs et de r\u00e9cepteurs",
                201: "Code des couleurs des r\u00e9sistances",
                304: "Table d\u2019\u00e9pellation internationale",
                309: "Adaptation, ROS, affaiblissement lin\u00e9ique, calcul ",
                307: "Teneur des messages, mat\u00e9riel obligatoire, exposition",
                302: "Indicatifs d'appel fran\u00e7ais et pr\u00e9fixes europ\u00e9ens",
                306: "Sanctions,  examen, perturbation, bande passante",
                308: "Caract\u00e9ristiques des antennes, longueur d'onde-fr\u00e9quence",
                301: "D\u00e9finition et autorisation des classes d\u2019\u00e9mission",
                310: "Gammes d\u2019onde, d\u00e9cibels, CEM, protection",
                303: "Abr\u00e9viations en code Q"
            }

            # ### Window config
            self.setFixedSize(800, 600)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle(f"Question numéro: {self.num}")
            self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
            self.setModal(True)
            x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
            y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
            self.setGeometry(x, y, 800, 600)

            # Main Layout
            self.main_layout = QVBoxLayout()
            self.setLayout(self.main_layout)

            # Image Label
            self.img_label = QLabel()
            self.img_label.setPixmap(QPixmap(f"./questions/{num}.png"))
            self.main_layout.addWidget(self.img_label, 1, Qt.AlignCenter)

            # Details layout
            self.detail_group = QGroupBox("Détails")
            self.detail_layout = QVBoxLayout()
            self.detail_group.setLayout(self.detail_layout)
            self.main_layout.addWidget(self.detail_group, 1, Qt.AlignCenter)

            self.num_quest_layout = QLabel(f"N° Question: {self.num}")
            self.response_layout = QLabel(f"Réponse: {self.reponse}")
            self.family_num_layout = QLabel(f"Num Famille: {self.theme_num}")
            self.family_layout = QLabel(f"Famille: {self.themes[self.theme_num]}")

            self.detail_layout.addWidget(self.num_quest_layout, 1, Qt.AlignLeft)
            self.detail_layout.addWidget(self.response_layout, 1, Qt.AlignLeft)
            self.detail_layout.addWidget(self.family_num_layout, 1, Qt.AlignLeft)
            self.detail_layout.addWidget(self.family_layout, 1, Qt.AlignLeft)

        def closeEvent(self, a0: QCloseEvent):
            """ Close Event """
            self.master.show()
            self.master.question_win = None
