#!/usr/bin/python3
# -*- coding: UTF-8 -*-
""" Exam'1 for French HAM Radio Certificate Training """
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QSplashScreen

from modules.main_ui import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.instance().setAttribute(Qt.AA_DontShowIconsInMenus)

    try:
        with open("./style/style.qss", "r") as style:
            qss = style.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        pass

    # noinspection PyArgumentList
    QFontDatabase.addApplicationFont("./fonts/Lato-Regular.ttf")
    app.setFont(MAIN_FONT)
    splash = QSplashScreen(QPixmap("./images/logocnfra2004-36k.JPG"))
    splash.show()
    app.processEvents()
    window = MainWindow()
    window.setWindowOpacity(0.0)
    splash.finish(window)
    window.show()
    window.opacity_timer_open.start()
    sys.exit(app.exec_())