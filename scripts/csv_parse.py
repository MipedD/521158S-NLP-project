import csv
import sys
import time
import getopt

# This module parses wanted columns of a .csv file to a new
# file and adds column "id" as the first column.
#
# Usage: python csv_parse.py -i [in_file] -o [out_file] -c [col, col,...]

def process_csv(in_file, out_file, columns):
    start_time = time.time()
    
    f = open(in_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')

    columns = columns.split(',')
    for i in range(0, len(columns)): 
        columns[i] = int(columns[i])

    result = open(out_file, mode='w', encoding='utf-8')
    csv_writer = csv.writer(result)
    line_count = 0
 
    for row in csv_reader:
        content = list(row[i] for i in columns)
        content.insert(0, ("id" if line_count == 0 else line_count))
        csv_writer.writerow(content)
        line_count += 1

    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
    print('<result> Output can be found at', out_file, '</result>')
    
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:c:')

input_file = ""
output_file = ""
columns = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-c':
        columns = opt[1]

if input_file == "" or output_file == "" or columns == "":
    print("Usage: python csv_parse.py -i [in_file] -o [out_file] -c [col, col,...]")
else:
    process_csv(input_file, output_file, columns)
