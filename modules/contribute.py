""" Contribute Window """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QWidget


class ContributeWindow(QWidget):
    """ Contribute Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Window config
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("Contribuez à l'amélioration d'Exam1")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 400, 400)

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.contribute_win = None
        self.master.show()
