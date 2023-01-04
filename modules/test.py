""" Test Windows """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QWidget


class TestLauncherWindow(QWidget):
    """ Test Launcher Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(600, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Choix du candidat et de l'épreuve")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 600, 600)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.test_launcher_win = None
        self.master.show()
