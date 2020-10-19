import csv
import sys
from empath import Empath
import time

file_name = sys.argv[1]
review_col = sys.argv[2]

# This module runs Empath category analysis on a text in a single column in .csv file.
# The first row of the input file is expected to be header.
# Results are written in a new file empath_result.txt which contains
# the input data appended with non-zero categories.
#
# Usage: python empath_categories.py [file] [column]

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    review_col = int(review_col)

    result = open('empath_result.txt', mode='w')
    csv_writer = csv.writer(result)
    
    empath_column = 'categories'
    
    lexicon = Empath()
    
    line_count = 0
    start_time = time.time()
    
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
            for category, score in categories.items():
                if score != 0:
                    trimmed_categories[category] = score
            
            row.append(trimmed_categories)
 
            #print(row)
            csv_writer.writerow(row)
            line_count += 1

    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
