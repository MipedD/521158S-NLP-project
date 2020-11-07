# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:16:24 2020

This script addresses mostly task 10 as we're now checking how many words
in each review we can spot that aren't recognized by WordNet

TODO:   should we preprocess the reviews here? The number of recognized words
        is surprisingly low overall.

@author: Miika
"""

import pandas as pd
import sys
import getopt
from nltk.corpus import wordnet
from nltk.tokenize import WordPunctTokenizer

def read_reviews_dataset(a_file, a_delimiter):
    data = pd.read_csv(a_file, sep=a_delimiter)
    return data

def num_unrecognized_words(a_review):
    wpt = WordPunctTokenizer()
    total = 0
    unrecognized = 0
    recognized = 0
    #tokenize
    tokens = []
    try: tokens = wpt.tokenize(a_review)
    except: print("unable to handle tokenization for", a_review)
    total = len(tokens)
    for token in tokens:
        if not wordnet.synsets(token):
            unrecognized = unrecognized + 1
        else:
            recognized = recognized + 1
    result = {}
    result["total"] = total
    result["unrecognized"] = unrecognized
    result["recognized"] = recognized
    return result

def process_reviews(a_data, a_col):
    unrecognized = []
    recognized = []
    total = []
    for index, row in a_data.iterrows():
        result = num_unrecognized_words(row[a_col])
        unrecognized.append(result["unrecognized"])
        recognized.append(result["recognized"])
        total.append(result["total"])
    a_data["unrecognized"] = unrecognized
    a_data["recognized"] = recognized
    a_data["total"] = total
    a_data["recognized.percent"] = a_data["recognized"] / a_data["total"]
    #let's check what are the percentages for ambiguous and non-ambiguous
    result = a_data.groupby(["ambiguous"], as_index=False).mean()
    ambiguous = a_data[a_data['ambiguous'] == True]
    non_ambiguous = a_data[a_data['ambiguous'] == False]
    ambiguous_mean = ambiguous['recognized.percent'].mean()
    non_ambigious_mean = non_ambiguous['recognized.percent'].mean()
    #Check the average number of words per for ambiguous & non-ambiguous
    ambiguous_average_words = ambiguous["total"].mean()
    non_ambiguous_average_words = non_ambiguous["total"].mean()
    print(result)
    print("<result>Average known words percentage for ambiguous:",ambiguous_mean, "</result>")
    print("<result>Average known words percentage for unambiguous:",non_ambigious_mean, "</result>")
    print("<result>Average total words for ambiguous:", ambiguous_average_words, "</result>")
    print("<result>Average total words for unambiguous:", non_ambiguous_average_words, "</result>")


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

if input_file == "" or output_file == "":# or column == "":
    print("Usage: -i [in_file] -o [out_file] -c [col]")
else:
    print("Reading dataset")
    dataset = read_reviews_dataset(input_file, ',')
    result = num_unrecognized_words("asd")
    process_reviews(dataset, "reviews.text")
    save_data_to_csv(dataset, output_file)
