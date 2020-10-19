# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:47:02 2020

@author: Miika
"""

import numpy as np
import matplotlib.pyplot as plt
import csv

def read_sentistrength_output(a_file, a_positive_col, a_negative_col):
    return_val = {}
    return_val["negative_sentiments"] = []
    return_val["positive_sentiments"] = []
    with open(a_file, newline='\n', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            try: int(row[0])
            except: continue
            try: int(row[1])
            except: continue
            return_val["negative_sentiments"].append(int(row[a_negative_col]))
            return_val["positive_sentiments"].append(int(row[a_positive_col]))
    return return_val

#Just one possible way to plot sentistrength output vs actual reviews.
def sample_plot_sentistrength(a_actual_reviews, a_negative_sentiments, a_positive_sentiments, a_range):
    x = np.arange(a_range[0], a_range[1], 1.0)
    y_actual = a_actual_reviews[a_range[0]:a_range[1]]
    y_pos = a_positive_sentiments[a_range[0]:a_range[1]]
    y_neg = a_negative_sentiments[a_range[0]:a_range[1]]
    s = 5
    plt.scatter(x, y_neg, s, c="r", alpha=1, marker="v",
                label="Sentistrength negative")
    plt.scatter(x, y_pos, s, c="b", alpha=1, marker="^",
                label="Sentistrength positive")
    plt.scatter(x, y_actual, s, c="g", alpha=1, marker="o",
                label="actual review")
    plt.xlabel("Review @ row")
    plt.ylabel("Sentiment value")
    plt.legend(loc='upper left')
    plt.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)
    plt.xticks(np.arange(0, 50, step=1), rotation=-90)
    plt.rcParams.update({'font.size': 7})
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()

def pearson_correlation_coefficient(a_set1, a_set2):
    #According to docs this function is pearson correlation coefficient
    #Basically returns a 2 x 2 matrix
    return np.corrcoef(a_set1, a_set2)
