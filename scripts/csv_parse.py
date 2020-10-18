import csv
import sys

file_name = sys.argv[1]
included_cols = sys.argv[2].split(',')

# This module parses wanted columns of a .csv file to a new result.txt file.
#
# Usage: python csv_parse.py [file] [col,col,...]

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    included_cols = map(int, included_cols)

    result = open('result.txt', mode='w')
    csv_writer = csv.writer(result)
    line_count = 0
 
    for row in csv_reader:
        content = list(row[i] for i in included_cols)
        csv_writer.writerow(content)
        #print(content)
        line_count += 1

    print 'Processed', line_count, 'rows.'
