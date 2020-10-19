import csv
import sys
import getopt
import time
from textblob import TextBlob

# This module runs TextBlob sentiment analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file which contains
# the input data appended with polarity and subjectivity columns.
#
# Usage: Usage: python textblob_sentiment.py -i [in_file] -o [out_file] -c [col]

def process_csv(in_file, out_file, column):
    start_time = time.time()
    
    f = open(in_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    result = open(out_file, mode='w')
    csv_writer = csv.writer(result)
    
    review_col = int(column)
    line_count = 0
 
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
    print("Usage: python textblob_sentiment.py -i [in_file] -o [out_file] -c [col]")
else:
    process_csv(input_file, output_file, column)
