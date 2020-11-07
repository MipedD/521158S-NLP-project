# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 13:13:28 2020

This script explores the textstat for task 12 a bit.

For more info: https://pypi.org/project/textstat/

To install simply run "pip install textstat"

Assignment explicitly asks to consider AUTOMATED READABILITY INDEX.
For that reason other alternatives are not explored here

About automated readability index (ARI):
    -   the score is up from 1 where lower score would mean easier readability.
    -   Wikipedia has a nice table explaining value ranges
        https://en.wikipedia.org/wiki/Automated_readability_index

@author: Miika
"""

import textstat
import pandas as pd
import sys
import getopt

#This example is based on the pypi textstat docs
def simple_example_ari():
    test_data = (
        "Playing games has always been thought to be important to "
        "the development of well-balanced and creative children; "
        "however, what part, if any, they should play in the lives "
        "of adults has never been researched that deeply. I believe "
        "that playing games is every bit as important for adults "
        "as for children. Not only is taking time out to play games "
        "with our children and other adults valuable to building "
        "interpersonal relationships but is also a wonderful way "
        "to release built up tension."
    )
    print("Calculating automated readability index (ARI)")
    readability_index = textstat.automated_readability_index(test_data)
    print("ARI:", readability_index)

def read_reviews_dataset(a_file, a_delimiter):
    data = pd.read_csv(a_file, sep=a_delimiter)
    return data

def ari_for_col(a_data, a_col):
    ari_col = []
    for review in a_data[a_col]:
        ari = -1
        try: ari = textstat.automated_readability_index(review)
        except: pass
            #print("unable to find ARI for", review)
        ari_col.append(ari)
    a_data["ari"] = ari_col
    return a_data

def save_data_to_csv(a_data, a_file_name):
    a_data.to_csv(a_file_name, index=False)

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:c:')

input_file = ""
output_file = ""
column = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-c':
        column = opt[1]

if input_file == "" or output_file == "" or column == "":
    print("Usage: -i [in_file] -o [out_file] -c [col]")
else:
    print("Reading dataset..")
    dataset = read_reviews_dataset(input_file, ',')
    print("Finding ARI")
    dataset_ari = ari_for_col(dataset, column)
    averages = dataset_ari.groupby(["ambiguous"], as_index=False).mean()
    print("<result>Average ARI for ambiguous:</result>")
    print(averages.loc[averages["ambiguous"] == True]["ari"])
    print("<result>Average ARI for unambiguous:</result>")
    print(averages.loc[averages["ambiguous"] == False]["ari"])
    print("Saving output to", output_file)
    save_data_to_csv(dataset_ari, output_file)
