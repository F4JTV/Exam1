#!/usr/bin/python3
# -*- coding: UTF-8 -*-
""" Exam'1 for French HAM Radio Certificate Training """
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt5.QtGui import QFontDatabase, QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from modules.main_ui import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Contextual menu translation
    translator = QTranslator()
    translator.load('qtbase_' + QLocale.system().name() + ".qm",
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    # Load Style
    """try:
        with open("./style/Combinear.qss", "r", encoding="utf-8") as style:
            qss = style.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        pass"""

    # Load fonts
    QFontDatabase.addApplicationFont("./font/Lato-Regular.ttf")
    QFontDatabase.addApplicationFont("./font/Radio Space.ttf")
    app.setFont(MAIN_FONT)

    # Splash Screen
    splash = QSplashScreen(QPixmap("./images/logocnfra2004-36k.JPG"))
    splash.show()

    window = MainWindow()
    window.setWindowOpacity(0.0)
    splash.finish(window)
    window.show()
    window.opacity_timer_open.start()
    sys.exit(app.exec_())
