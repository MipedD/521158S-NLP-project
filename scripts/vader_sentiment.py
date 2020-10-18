import csv
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

file_name = sys.argv[1]
review_col = sys.argv[2]

# This module runs Vader sentiment analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file vader_result.txt which contains
# the input data appended with sentiment columns.
#
# Usage: python vader_sentiment.py [file] [column]

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    review_col = int(review_col)

    result = open('vader_result.txt', mode='w')
    csv_writer = csv.writer(result)
    
    sentiment_colums = ['pos', 'neu', 'neg', 'compound']
    
    sid = SentimentIntensityAnalyzer()
    
    line_count = 0
 
    for row in csv_reader:
        if line_count == 0:
            for sentiment in sentiment_colums:
                row.append(sentiment)

            csv_writer.writerow(row)
            line_count += 1
        else: 
            content = list(row)
            review = row[review_col]
            ss = sid.polarity_scores(review)
            for sentiment in sentiment_colums:
                row.append(ss.get(sentiment))
                
            #print(row)
            csv_writer.writerow(row)
            line_count += 1

    print('Processed', line_count, 'rows.')
