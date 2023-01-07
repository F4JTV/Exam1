""" Asked Questions Window """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QWidget


class AskedQuestionsWindow(QWidget):
    """ Asked Questions Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Liste des questions posées")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.asked_questions_win = None
        self.master.show()
