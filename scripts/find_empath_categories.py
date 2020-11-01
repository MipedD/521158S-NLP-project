import csv
import sys
import getopt
import time
import ast
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# This module parses a cvs file, which has Empath categories in a specified column.
# For each unique category Vader Sentiment analysis is run, and categories divided
# by pos, neu and neg sentiment. Results are saved in out file.
#
# Usage: python find_empath_categories.py.py -i [in_file] -o [out_file] -c [column]

def process_csv(in_file, out_file, column):
    start_time = time.time()
    
    f = open(in_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    positive = set()
    negative = set()
    neutral = set()
    category_col = int(column)
    sid = SentimentIntensityAnalyzer()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else: 
            content = list(row)
            categories = row[category_col]
            categories_dict = ast.literal_eval(categories)
            for category in categories_dict:
                ss = sid.polarity_scores(category)
                
                if 1 == ss.get("pos"):
                    positive.add(category)
                elif 1 == ss.get("neu"):
                    neutral.add(category)
                elif 1 == ss.get("neg"):
                    negative.add(category)

            line_count += 1
     
    collected = "positive:" + str(positive) + "\nneutral:"
    collected += str(neutral) + "\nnegative:" + str(negative)

    result_file = open(out_file, mode='w')
    result_file.write(collected)
    result_file.close()

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
    print("Usage: python find_empath_categories.py -i [in_file] -o [out_file] -c [column]")
else:
    process_csv(input_file, output_file, column)
