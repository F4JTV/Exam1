""" Contribute Window """
import json
import webbrowser

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QTableWidget, QHeaderView,
                             QTableWidgetItem)


class ContributeWindow(QWidget):
    """ Contribute Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        self.contributors_win = None
        self.detail_txt = "Nous sommes persuadés que le logiciel Exam'1 et les cours " \
                          "vidéo/PDF de Jean-Luc F6GPX vous ont aidés à devenir Radioamateur.\n\n" \
                          "Nous vous demandons simplement de nous envoyer un compte-rendu " \
                          "détaillé lors de votre passage de votre examen ainsi que le numéro d'examen.\n" \
                          "Avec ce compte-rendu, vous allez contribuer à l'améliorer la base de " \
                          "données des questions et les futurs Radioamateurs vous seront reconnaissants.\n\n" \
                          "Nous tenons également à remercier toutes personnes qui oeuvrent pour la " \
                          "formation Radioamateur, ils sont nombreux et nous avons tous le même but, " \
                          "vous permettre de rejoindre le monde merveilleux des Radioamateurs.\n\n" \
                          "Rejoignez la liste des participants en envoyant un mail au RadioClub F6KGL.\n\n"

        # ### Window config
        self.setFixedSize(700, 450)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Contribuez à l'amélioration d'Exam1")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_label = QLabel("Aidez-nous à améliorer la base de données")
        self.main_label.setFont(QFont("Lato", 20))
        self.detail_label = QLabel(self.detail_txt)
        self.detail_label.setWordWrap(True)
        self.detail_label.setAlignment(Qt.AlignJustify)

        self.main_layout.addWidget(self.main_label, 1, Qt.AlignCenter)
        self.main_layout.addWidget(self.detail_label, 3, Qt.AlignCenter)

        self.contributors_list_btn = QPushButton("Liste des contributeurs")
        self.send_message_btn = QPushButton("Contactez le Radio-Club F6KGL")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.contributors_list_btn)
        self.buttons_layout.addWidget(self.send_message_btn)

        self.send_message_btn.clicked.connect(lambda: webbrowser.open("https://f6kgl-f5kff.fr/contact/"))
        self.contributors_list_btn.clicked.connect(self.display_contributors_win)

        self.main_layout.addLayout(self.buttons_layout, 1)

    def display_contributors_win(self):
        """ Display the contributors table Window """
        self.contributors_win = ContributorsWindow(self)
        self.contributors_win.show()
        self.contributors_list_btn.setDisabled(True)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.contribute_win = None
        self.master.contribute_btn.setEnabled(True)
        self.master.show()

        if self.contributors_win is not None:
            self.contributors_win.close()


class ContributorsWindow(QWidget):
    """ All Questions Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(600, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Liste des contributeurs")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Main layout Widgets
        self.contributors_table = QTableWidget()
        self.contributors_table.setFixedSize(QSize(580, 580))
        self.contributors_table.setSortingEnabled(True)
        self.contributors_table.setColumnCount(2)
        self.contributors_table.horizontalHeader().setStretchLastSection(True)
        self.contributors_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.contributors_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.name_header = QTableWidgetItem("Nom")
        self.name_header.setFont(QFont("Lato", 12))
        self.indicatif_header = QTableWidgetItem("Indicatif")
        self.indicatif_header.setFont(QFont("Lato", 12))
        self.contributors_table.setHorizontalHeaderItem(0, self.name_header)
        self.contributors_table.setHorizontalHeaderItem(1, self.indicatif_header)
        self.contributors_table.verticalHeader().setVisible(False)
        self.contributors_table.setAlternatingRowColors(True)

        self.main_layout.addWidget(self.contributors_table, 1, Qt.AlignmentFlag.AlignCenter)

        try:
            with open("./files/contributors.json", "r", encoding="utf-8") as contributors_file:
                self.contributors = json.load(contributors_file)
                self.contributors_table.setRowCount(len(self.contributors.keys()))

                row = 0
                for nom, details in self.contributors.items():
                    name = nom
                    indicatif = details["indicatif"]
                    name_item = QTableWidgetItem(name)
                    indicatif_item = QTableWidgetItem(indicatif)
                    name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    indicatif_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    name_item.setTextAlignment(Qt.AlignCenter)
                    indicatif_item.setTextAlignment(Qt.AlignCenter)

                    self.contributors_table.setItem(row, 0, name_item)
                    self.contributors_table.setItem(row, 1, indicatif_item)
                    row += 1

            self.setWindowTitle(f"Liste des {row + 1} contributeurs")

        except FileNotFoundError as error:
            print(error)
        except KeyError as error:
            print(error)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.contributors_win = None
        # self.master.show()
        self.master.contributors_list_btn.setEnabled(True)
