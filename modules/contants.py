import json

from PyQt5.QtWidgets import QMessageBox

THEMES_DICT = {
    305: "Questions entrainement",
    206: "Electricité de base",
    202: "Groupements de résistances",
    207: "Courants alternatifs",
    208: "Condensateurs et bobines (séparés)",
    209: "Transformateurs, ampli op, filtres RC LC RLC",
    205: "Rôle des différents étages RF, haut-parleur, micro",
    203: "Diodes et transistors, classes d'amplification",
    210: "Antennes, couplage, propagation, ligne de transmission",
    204: "Synoptiques d'émetteurs et de récepteurs",
    201: "Code des couleurs des résistances",
    304: "Table d'épellation internationale",
    309: "Adaptation, ROS, affaiblissement linéique, calcul ",
    307: "Teneur des messages, matériel obligatoire, exposition",
    302: "Indicatifs d'appel français et préfixes européens",
    306: "Sanctions,  examen, perturbation, bande passante",
    308: "Caractéristiques des antennes, longueur d'onde-fréquence",
    301: "Définition et autorisation des classes d'émission",
    310: "Gammes d'onde, décibels, CEM, protection",
    303: "Abréviations en code Q"
        }

THEMES_LIST = [
    305, 206, 202, 207, 208, 209, 205, 203, 210, 204,
    201, 304, 309, 307, 302, 306, 308,301, 310, 303
]

SEPARATED_THEME_DICT = {
    "Reglementation": {
        303: "Abréviations en code Q",
        309: "Adaptation, ROS, affaiblissement linéique, calcul ",
        308: "Caractéristiques des antennes, longueur d'onde-fréquence",
        301: "Définition et autorisation des classes d'émission",
        310: "Gammes d'onde, décibels, CEM, protection",
        302: "Indicatifs d'appel français et préfixes européens",
        305: "Questions entrainement",
        306: "Sanctions,  examen, perturbation, bande passante",
        304: "Table d'épellation internationale",
        307: "Teneur des messages, matériel obligatoire, exposition",
    },
    "Technique": {
        210: "Antennes, couplage, propagation, ligne de transmission",
        201: "Code des couleurs des résistances",
        208: "Condensateurs et bobines (séparés)",
        207: "Courants alternatifs",
        203: "Diodes et transistors, classes d'amplification",
        206: "Electricité de base",
        202: "Groupements de résistances",
        205: "Rôle des différents étages RF, haut-parleur, micro",
        204: "Synoptiques d'émetteurs et de récepteurs",
        209: "Transformateurs, ampli op, filtres RC LC RLC",
    }
}

def get_series():
    """ Get series from series.json """
    with open("./files/series.json", "r", encoding="utf-8") as series_file:
        return json.load(series_file)

def get_users():
    """ Get the users from users.json """
    with open("./files/users.json", "r", encoding="utf-8") as users_file:
        return json.load(users_file)

def get_questions():
    """ Get all the questions """
    with open("./questions/questions.json") as questions_files:
        return json.load(questions_files)

def display_error(master, error):
    """ Display the given error """
    error_win = QMessageBox(master)
    error_win.setText(error)
    error_win.setWindowTitle("Erreur")
    error_win.setIcon(QMessageBox.Critical)
    error_win.setModal(True)
    error_win.exec_()