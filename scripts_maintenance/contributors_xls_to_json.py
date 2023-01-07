#!/usr/bin/python3
""" Contributor converter: xls to json """
import json
import pandas as pd


contributor_dict = dict()

xls = pd.read_excel("./Contributeurs.xls", engine="xlrd")
for row in xls.values:
    nom = str(row[1]).strip()
    indicatif = str(row[2]).strip()
    adresse = str(row[3]).strip()
    if indicatif == "nan" or indicatif == "":
        indicatif = ""
    if adresse == "nan" or adresse == "":
        adresse = ""

    contributor_dict[nom] = {"indicatif": indicatif,
                                "adresse": adresse
                                }

with open("./contributors.json", "w", encoding="utf-8") as contributor_file:
    json.dump(contributor_dict, contributor_file, indent=4,
              sort_keys=True, ensure_ascii=False)