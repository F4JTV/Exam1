#!/usr/bin/python3
""" Management Window """
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QToolButton


class ManagementWindow(QDialog):
    """ Management Window """

    def __init__(self, master):
        super().__init__()
        self.master = master

        # ### Main Window config
        self.setFixedSize(400, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Gestion des épreuves")
        self.setWindowIcon(QIcon("./images/logocnfra80x80.jpg"))
        self.setModal(True)
        x = self.master.geometry().x() + self.master.width() // 2 - self.width() // 2
        y = self.master.geometry().y() + self.master.height() // 2 - self.height() // 2
        self.setGeometry(x, y, 400, 400)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Buttons
        self.complete_list_tests = QToolButton()

    def closeEvent(self, a0: QCloseEvent):
        """ Close Event """
        self.master.management_win = None