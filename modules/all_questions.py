""" All Questions Window """
import json

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView)


class AllQuestionsWindow(QDialog):
    """ All Questions Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # Variables
        self.questions = dict()

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
        self.questions_table.setFixedSize(QSize(780, 580))
        self.questions_table.setSortingEnabled(True)
        self.questions_table.setColumnCount(2)
        self.questions_table.horizontalHeader().setStretchLastSection(True)
        self.questions_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.questions_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.questions_table.setHorizontalHeaderLabels(["Numéro", "Question"])
        self.questions_table.verticalHeader().setVisible(False)

        self.main_layout.addWidget(self.questions_table, 1, Qt.AlignmentFlag.AlignCenter)
        self.create_questions_table()


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
