# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 14:15:54 2020

This script is mostly for task 10 (and the following) -
we're looking to establish "ambiguous" class based on the discrepancy
between the sentiment polarity and actual review.

This script calculates the difference between overall sentiment as seen by
analyzer and compares it to the review and classifies each review
as ambiguous (true, false) if the difference is greater than the input

TODO:   this script DOES NOT address one part of the assignment:
        "setting up a threshold to distinguish positive and negative
        rating based sentiment" as I have no clue what that means and what
        purpose it would serve here.
        Could the idea be that it further filters the ambiguous class
        as in any discrepancy is acceptable as long as the rough conclusion
        (negative vs positive) is correct for the analyzer?

@author: Miika
"""

import pandas as pd
import sys
import getopt
from sklearn.preprocessing import MinMaxScaler

#This is the border between negative and positive. Everything <= is negative,
#and everything greater is positive
neg_pos_treshold = 0.5

def read_reviews_dataset(a_file, a_delimiter):
    data = pd.read_csv(a_file, sep=a_delimiter, encoding='utf-8')
    return data

def normalize_column(a_data, a_column):
    scaler = MinMaxScaler()
    target_col = a_data[[a_column]]
    target_col_scaled = scaler.fit_transform(target_col)
    a_data[a_column] = target_col_scaled

def calculate_discrepancy(a_data, a_rating, a_sentiment):
    a_data["discrepancy"] = abs(a_data[a_rating] - a_data[a_sentiment])# and a_data["correct"]
    a_data["overall_accurate"] = (a_data[a_rating] > neg_pos_treshold) & (a_data[a_sentiment] > neg_pos_treshold)
    return a_data

def classify_ambiguous(a_data, a_treshold):
    a_data["ambiguous"] = (a_data["discrepancy"] > a_treshold) & (a_data["overall_accurate"])
    return a_data

def save_data_to_csv(a_data, a_file_name):
    a_data.to_csv(a_file_name, index=False, encoding='utf-8')

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:t:')

input_file = ""
output_file = ""
treshold = 0.25

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-t':
        treshold = float(opt[1])

if input_file == "" or output_file == "":
    print("Usage: -i [in_file] -o [out_file] -c [col]")
else:
    #Read vader output
    print("Reading input..")
    original = read_reviews_dataset(input_file, ',')
    copy = original.copy()
    print("Normalizing sentiment..")
    normalize_column(copy, "sentiment.overall.vader")
    print("Normalizing ratings..")
    normalize_column(copy, "reviews.rating")
    print("Calculating discrepancy")
    copy = calculate_discrepancy(copy, "reviews.rating", "sentiment.overall.vader")
    print("Marking reviews ambiguous based on discrepancy exceeding", treshold)
    copy = classify_ambiguous(copy, treshold)
    print("Writing results into", output_file)
    original["ambiguous"] = copy["ambiguous"]
    save_data_to_csv(original, output_file)
    print("Done.")
