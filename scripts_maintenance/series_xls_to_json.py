#!/usr/bin/python3
""" Series converter: xls to json """
import json
import pandas as pd


series_dict = dict()

xls = pd.read_excel("./Séries.xls", engine="xlrd")
for row in xls.values:
    serie = str(row[0]).strip()
    q1 = str(row[1]).strip()
    q2 = str(row[2]).strip()
    q3 = str(row[3]).strip()
    q4 = str(row[4]).strip()
    q5 = str(row[5]).strip()
    q6 = str(row[6]).strip()
    q7 = str(row[7]).strip()
    q8 = str(row[8]).strip()
    q9 = str(row[9]).strip()
    q10 = str(row[10]).strip()
    q11 = str(row[11]).strip()
    q12 = str(row[12]).strip()
    q13 = str(row[13]).strip()
    q14 = str(row[14]).strip()
    q15 = str(row[15]).strip()
    q16 = str(row[16]).strip()
    q17 = str(row[17]).strip()
    q18 = str(row[18]).strip()
    q19 = str(row[19]).strip()
    q20 = str(row[20]).strip()


    series_dict[serie] = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10,
        "q11": q11,
        "q12": q12,
        "q13": q13,
        "q14": q14,
        "q15": q15,
        "q16": q16,
        "q17": q17,
        "q18": q18,
        "q19": q19,
        "q20": q20,
        }

with open("../files/series.json", "w", encoding="utf-8") as series_file:
    json.dump(series_dict, series_file, indent=4,
              sort_keys=False, ensure_ascii=False)