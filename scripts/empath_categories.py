import csv
import sys
import getopt
import time
import pandas as pd
import os
from empath import Empath

# This module runs Empath category analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file which contains
# the input data appended with non-zero categories.
#
# Usage: python empath_categories.py.py -i [in_file] -o [out_file] -c [column]

def process_csv(in_file, out_file, column):
    start_time = time.time()
    
    f = open(in_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    result = open(out_file, mode='w', encoding='utf-8')
    csv_writer = csv.writer(result)
    
    review_col = int(column)
    empath_column = 'categories'
    lexicon = Empath()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            row.append(empath_column)
            csv_writer.writerow(row)
            line_count += 1
        else: 
            content = list(row)
            review = row[review_col]
            categories = lexicon.analyze(review, normalize=True)
            trimmed_categories = dict()
            if categories:
                for category, score in categories.items():
                    if score != 0:
                        trimmed_categories[category] = score
            
            row.append(trimmed_categories)
 
            #print(row)
            csv_writer.writerow(row)
            line_count += 1

    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')

input_file = ""
output_file = ""
column = ""
append_to_input = False

argv = sys.argv[1:]
if argv.index('-a') != -1:
    append_to_input = True
    argv.pop(argv.index('-a'))
opts, args = getopt.getopt(argv, 'i:o:c:')

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-c':
        column = opt[1]

if input_file == "" or output_file == "" or column == "":
    print("Usage: python empath_categories.py.py -i [in_file] -o [out_file] -c [column]")
else:
    process_csv(input_file, output_file, column)
    if append_to_input:
        print("Appending results to input file.")
        data = pd.read_csv(output_file, sep=',', encoding='utf-8')
        data.to_csv(input_file, sep=',', encoding='utf-8', index=False)
        os.remove(output_file)
