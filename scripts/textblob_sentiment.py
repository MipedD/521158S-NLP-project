import csv
import sys
from textblob import TextBlob
import time

file_name = sys.argv[1]
review_col = sys.argv[2]

# This module runs TextBlob sentiment analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file textblob_result.txt which contains
# the input data appended with polarity and subjectivity columns.
#
# Usage: python textblob_sentiment.py [file] [column]

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    review_col = int(review_col)

    result = open('textblob_result.txt', mode='w')
    csv_writer = csv.writer(result)
    line_count = 0
    start_time = time.time()
 
    for row in csv_reader:
        if line_count == 0:
            row.append('polarity')
            row.append('subjectivity')
            csv_writer.writerow(row)
            line_count += 1
        else:
            content = list(row)
            review = row[review_col]
            review_blob = TextBlob(review)
            row.append(review_blob.polarity)
            row.append(review_blob.subjectivity)
            #print(row)
            csv_writer.writerow(row)
            line_count += 1

    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
