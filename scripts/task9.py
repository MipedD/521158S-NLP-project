# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 18:13:20 2020

The script is directed at task 9. The script simply looks for instances of expressions
specifified with -e <file> which is expected to be a single column csv.

Specify -i for inputting review data.

@author: Miika
"""

import pandas as pd
import sys
import getopt

#Number of a_expressions found in a_target
def count_expressions(a_target, a_expressions):
    target_str = ""
    try:
        target_str = str(a_target)
    except:
        pass
    total_instances = 0
    for expression in a_expressions:
        instances = target_str.lower().count(expression.lower())
        total_instances = total_instances + instances
    return total_instances

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:e:')

input_file = "C:/Users/Miika/Documents/git/521158S-NLP-project/data/dataset_processed.csv"
expl_expr = "C:/Users/Miika/Documents/git/521158S-NLP-project/data/explanatory_wording.csv"

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    if opt[0] == '-e':
        expl_expr = opt[1]

if input_file == "":
    print("Usage: -i [in_file_dataset] -e [in_file_wordlist]")
else:
    #Load dataset
    print("Reading dataset:", input_file)
    dataset = pd.read_csv(input_file, sep=',', encoding='utf-8')
    #Load list of expressions
    print("Reading list of explanatory wording:", expl_expr)
    explanatory_wording = pd.read_csv(expl_expr, sep=',', encoding='utf-8')
    print("Finding explanatory wording in each review..")
    new_series = []
    for review in dataset["reviews.text"]:
        new_series.append(count_expressions(review, explanatory_wording["expressions"]))
    #Let's see if the number of explanatory expressions matter
    temp = pd.DataFrame()
    temp["user.rating"] = dataset["reviews.rating"]
    temp["explanatory_expressions"] = new_series
    positive = temp.loc[temp['user.rating'] >= 4]
    negative = temp.loc[temp['user.rating'] <= 2]
    positive_mean = positive.mean()["explanatory_expressions"]
    negative_mean = negative.mean()["explanatory_expressions"]
    print("<result> Average explanatory expressions per positive review", positive_mean, "</result>")
    print("<result> Average explanatory expressions per negative review", negative_mean, "</result>")
