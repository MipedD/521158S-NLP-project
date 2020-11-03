# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:47:02 2020

@author: Miika
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import getopt
import sys
from sklearn.preprocessing import MinMaxScaler

#Just one possible way to plot sentistrength output vs actual reviews.
def scatter_plot(a_ratings, a_analyzer1, a_analyzer2, a_range, a_output_file):
    x = np.arange(a_range[0] + 1, a_range[1] + 1, 1.0)
    #Get the list of actual ratings from the users
    y_ratings = a_ratings[a_range[0]:a_range[1]]
    #Get the overall of #1
    y_overall1 = a_analyzer1[a_range[0]:a_range[1]]
    #Same for the analyzer2
    y_overall2 = a_analyzer2[a_range[0]:a_range[1]]
    s = 1
    fig = plt.figure(figsize=(15,5))
    plt.scatter(x, y_overall1, s, c="black", alpha=0.2, marker="o",
                label="Sentistrength")
    plt.scatter(x, y_overall2, s, c="green", alpha=0.2, marker="o",
                label="Vader")
    plt.scatter(x, y_ratings, s, c="red", alpha=0.2, marker="o",
                label="Rating")
    plt.xlabel("Review")
    plt.ylabel("Sentiment value")
    plt.legend(loc='upper left')
    plt.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)
    plt.xticks(np.arange(a_range[0], a_range[1], step=1), rotation=-90)
    plt.rcParams.update({'font.size': 7})
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.gca().axes.xaxis.set_ticks([])
    #plt.show()
    fig.savefig(a_output_file)
    print("<result>Plot saved to", a_output_file, "</result>")

def plot_barchart(a_ratings, a_analyzer1, a_analyzer2, a_range):
    x = np.arange(a_range[0]+1, a_range[1]+1, 1.0)
    #Get the list of actual ratings from the users
    y_ratings = a_ratings[a_range[0]:a_range[1]]
    #Get the overall of #1
    y_overall1 = a_analyzer1[a_range[0]:a_range[1]]
    #Same for the analyzer2
    y_overall2 = a_analyzer2[a_range[0]:a_range[1]]
    width=0.8
    plt.scatter(x, y_ratings, 14, c="black", alpha=1, marker="x", zorder=5)
    plt.bar(x, y_overall1 - y_ratings, width=width, bottom = y_ratings, align="center", zorder=2, color="grey", alpha=0.5)
    plt.bar(x, y_overall2 - y_ratings, width=width, bottom = y_ratings, align="center", color="g", alpha=0.5, zorder=1)

    plt.grid(color='black', alpha=0.2, linestyle='-', linewidth=1)
    #plt.xticks(np.arange(a_range[0]+1, a_range[1]+1, step=1), rotation=-90)
    plt.yticks(np.arange(-0.1, 1.1, step=0.25))
    #plt.save()

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:')

input_file = ""
output_file = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]

if input_file == "":
    print("invalid args")
else:
    #read dataset
    data = pd.read_csv(input_file, sep=',', encoding='utf-8')
    vader_overall = data["sentiment.overall.vader"]
    ss_overall = data["sentiment.overall.sentistrength"]
    actual_ratings = data["reviews.rating"]
    print("Calculating pearson correlation coefficient for both analyzers..")
    #Calculate the correlation coefficient for vader
    vader_pcc_df = pd.DataFrame()
    vader_pcc_df["actual_rating"] = data["reviews.rating"]
    vader_pcc_df["vader_analysis"] = data["sentiment.overall.vader"]
    vader_pcc = vader_pcc_df.corr(method='pearson')
    #Calculate the correlation coefficient for sentistrength
    ss_pcc_df = pd.DataFrame()
    ss_pcc_df["actual_rating"] = data["reviews.rating"]
    ss_pcc_df["ss_analysis"] = data["sentiment.overall.sentistrength"]
    ss_pcc = ss_pcc_df.corr(method='pearson')
    #Log the correlations for GUI
    print("<result>Sentistrength (SS) Pearson Correlation Coefficient:</result>")
    print(ss_pcc)
    print("<result>Vader Pearson Correlation Coefficient:</result>")
    print(vader_pcc)
    print("Normalizing sentiment analyzer output and reviews for plotting..")
    #Normalize values for plotting
    scaler = MinMaxScaler()
    plot_data = data.head(10000)
    print(plot_data)
    plot_data = plot_data.sort_values(by='reviews.rating')
    print(plot_data)
    vader_norm = scaler.fit_transform(plot_data[["sentiment.overall.vader"]])
    ss_norm =  scaler.fit_transform(plot_data[["sentiment.overall.sentistrength"]])
    rating_norm =  scaler.fit_transform(plot_data[["reviews.rating"]])
    #Plot values
    print("Plotting..")
    scatter_plot(rating_norm, ss_norm, vader_norm, [0,10000], output_file)
