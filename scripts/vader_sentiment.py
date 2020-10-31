import sys
import time
import getopt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# This module runs Vader sentiment analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file which contains
# the input data appended with sentiment columns.
#
# Usage: python vader_sentiment.py.py -i [in_file] -o [out_file] -c [column]

def process_csv(in_file, out_file, column):
    print('Processing..')
    start_time = time.time()
    sid = SentimentIntensityAnalyzer()
    data = pd.read_csv(in_file, sep=',', encoding='utf-8')
    out_data = data
    sentiment_colums = ['pos', 'neu', 'neg', 'compound']
    sentiments = {"pos" : list(), 'neg' : list(), 'neu' : list(), 'compound' : list()}
    line_count = 0
    for review in data[column]:
        line_count = line_count + 1
        try: ss = sid.polarity_scores(review)
        except: ss = {'pos' : 'NaN', 'neu' : 'NaN', 'neg' : "NaN", 'compound' : 'NaN'}
        for sentiment in sentiment_colums:
            res = ss.get(sentiment)
            sentiments[sentiment].append(res)
    out_data["sentiment.positive.vader"] = sentiments['pos']
    out_data["sentiment.negative.vader"] = sentiments['neg']
    out_data["sentiment.neutral.vader"] = sentiments['neu']
    out_data["sentiment.overall.vader"] = sentiments['compound']
    out_data.to_csv(out_file, index=False, encoding='utf_8', sep=',')
    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')

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
    print("Usage: python vader_sentiment.py.py -i [in_file] -o [out_file] -c [column]")
else:
    process_csv(input_file, output_file, column)
