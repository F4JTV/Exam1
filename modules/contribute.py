""" Contribute Window """
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class ContributeWindow(QWidget):
    """ Contribute Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

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
        self.setFixedSize(600, 350)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Contribuez à l'amélioration d'Exam1")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 600, 350)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_label = QLabel("Aidez-nous à améliorer la base de données")
        self.main_label.setFont(QFont("Lato", 16))
        self.detail_label = QLabel(self.detail_txt)
        self.detail_label.setWordWrap(True)
        self.detail_label.setAlignment(Qt.AlignJustify)

        self.main_layout.addWidget(self.main_label, 1, Qt.AlignCenter)
        self.main_layout.addWidget(self.detail_label, 3, Qt.AlignCenter)

        self.contributors_list_btn = QPushButton("Liste des participants")
        self.send_message_btn = QPushButton("Contactez le RC F6KGL")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.contributors_list_btn)
        self.buttons_layout.addWidget(self.send_message_btn)

        self.send_message_btn.clicked.connect(lambda: webbrowser.open("https://f6kgl-f5kff.fr/contact/"))

        self.main_layout.addLayout(self.buttons_layout, 1)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.contribute_win = None
        self.master.show()
