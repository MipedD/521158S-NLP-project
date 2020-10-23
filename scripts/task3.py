# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:47:02 2020

@author: Miika
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def read_ratings(a_file, a_id_col, a_reviews_col, a_delimiter, normalize):
    data = pd.read_csv(a_file, sep=a_delimiter)
    if normalize:
        scaler = MinMaxScaler()
        reviews_column = data[[a_reviews_col]]
        reviews_column_scaled = scaler.fit_transform(reviews_column)
        data[a_reviews_col] = reviews_column_scaled
    reviews_data = pd.DataFrame()
    reviews_data["id"] = data[a_id_col]
    reviews_data["rating"] = data[a_reviews_col]
    return reviews_data

def read_sentiment_analyzer_output(a_file, a_id_col, a_positive_col, a_negative_col, a_overall_col, a_delimiter, normalize):
    data = pd.read_csv(a_file, sep=a_delimiter)
    scaler = MinMaxScaler()
    if normalize[0]:
        #normalize values - positive
        positive_column = data[[a_positive_col]]
        positive_column_scaled = scaler.fit_transform(positive_column)
        data[a_positive_col] = positive_column_scaled
    if normalize[1]:
        #normalize values - negative
        negative_column = data[[a_negative_col]]
        negative_column_scaled = scaler.fit_transform(negative_column)
        data[a_negative_col] = 1 - negative_column_scaled
    if normalize[2]:
        #normalize values - overall
        overall_column = data[[a_overall_col]]
        overall_column_scaled = scaler.fit_transform(overall_column)
        data[a_overall_col] = overall_column_scaled
        #Mark negative values with a sign

    sentiment_data = pd.DataFrame()
    sentiment_data["id"] = data[a_id_col]
    sentiment_data["positive"] = data[a_positive_col]
    sentiment_data["negative"] = data[a_negative_col]
    sentiment_data["overall"] = data[a_overall_col]

    return sentiment_data

#Just one possible way to plot sentistrength output vs actual reviews.
def sample_plot_sentistrength(a_ratings, a_analyzer1, a_analyzer2, a_range):
    x = np.arange(a_range[0] + 1, a_range[1] + 1, 1.0)
    #Get the list of actual ratings from the users
    y_ratings = a_ratings["rating"][a_range[0]:a_range[1]]
    #Get the overall of #1
    y_overall1 = a_analyzer1["overall"][a_range[0]:a_range[1]]
    #Same for the analyzer2
    y_overall2 = a_analyzer2["overall"][a_range[0]:a_range[1]]
    s = 8
    plt.scatter(x, y_overall1, s, c="g", alpha=1, marker="o",
                label="Overall 1")
    plt.scatter(x, y_overall2, s, c="b", alpha=1, marker="o",
                label="Overall 2")
    plt.scatter(x, y_ratings, s, c="red", alpha=1, marker="o")
    plt.xlabel("Review @ row")
    plt.ylabel("Sentiment value")
    plt.legend(loc='upper left')
    plt.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)
    plt.xticks(np.arange(a_range[0], a_range[1], step=1), rotation=-90)
    plt.rcParams.update({'font.size': 7})
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()

def plot_barchart(a_ratings, a_analyzer1, a_analyzer2, a_range):
    x = np.arange(a_range[0]+1, a_range[1]+1, 1.0)
    #Get the list of actual ratings from the users
    y_ratings = a_ratings["rating"][a_range[0]:a_range[1]]
    #Get the overall of #1
    y_overall1 = a_analyzer1["overall"][a_range[0]:a_range[1]]
    #Same for the analyzer2
    y_overall2 = a_analyzer2["overall"][a_range[0]:a_range[1]]
    width=0.8
    plt.scatter(x, y_ratings, 14, c="black", alpha=1, marker="x", zorder=5)
    plt.bar(x, y_overall1 - y_ratings, width=width, bottom = y_ratings, align="center", zorder=2, color="grey", alpha=0.5)
    plt.bar(x, y_overall2 - y_ratings, width=width, bottom = y_ratings, align="center", color="g", alpha=0.5, zorder=1)

    plt.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)
    plt.xticks(np.arange(a_range[0]+1, a_range[1]+1, step=1), rotation=-90)
    plt.yticks(np.arange(-0.1, 1.1, step=0.25))
    plt.show()

def pearson_correlation_coefficient(a_set1, a_set2):
    #According to docs this function is pearson correlation coefficient
    #Basically returns a 2 x 2 matrix
    return np.corrcoef(a_set1, a_set2)

#data_ratings = read_ratings("C:/Users/Miika/Documents/git/521158S-NLP-project/data/Datafiniti_Jun19_parsed.csv", "id", "reviews.rating", ',', True)
data_senti = read_sentiment_analyzer_output("C:/Users/Miika/Documents/git/521158S-NLP-project/data/sentistrength_sentiments.csv", "id","positive","negative", "overall", '\t', [True, True, True])
data_vader = read_sentiment_analyzer_output("C:/Users/Miika/Documents/git/521158S-NLP-project/data/vader_sentiments.csv", "id","pos","neg", "compound", ';', [False, False, True])
#print(data_ratings)
print("Senti values")
print(data_senti)
print("Vader values")
print(data_vader)
#plot_barchart(data_ratings, data_senti, data_vader, [0, 50])
