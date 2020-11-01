import csv
import sys
import getopt
import time

# This module takes three arguments:
# in_file is any csv file that has id in first column
# filter_file is the result of find_named_entity_categories.py
# Thid argument is a list of wanted categories separated by comma.
#
# This module goes through the filter file to find ids of rows that
# match all wanted categories. If no categories are wanted ids where
# there are none are listed.
#
# Usage: get_review_id_by_category.py -i [in_file] -f [filter_file] -c [category, category,...]

def process_csv(in_file, filter_file, categories):
    start_time = time.time()
    
    f = open(filter_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    category_list = list()
    if categories:
        category_list = categories.split(',')
        
    category_columns = list()
    match_ids = list()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            # First find the index of the wanted categories
            if category_list:
                for category in category_list:
                    try:
                        index = row.index(category)
                        category_columns.append(index)
                    except:
                        print("Error: Category not found:", category)
            line_count += 1
        else:
            # Then compare that all or none wanted categories appear
            if category_columns:
                match = 1
                for category in category_columns:
                    match &= int(row[category])
                if match == 1:                    
                    match_ids.append(row[0])
            else:
                row_id = row[0]
                row.pop(0)
                match = 0
                for category in row:
                    match += int(category)
                if match == 0:
                    match_ids.append(row_id)
            line_count += 1

    f.close()
    f = open(in_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    filtered = filter(lambda x: (x[0] in match_ids), list(csv_reader))
    f.close()
    
    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
    print(len(match_ids), "matches found")

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:c:f:')

input_file = ""
filter_file = ""
categories = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-f':
        filter_file = opt[1]       
    elif opt[0] == '-c':
        categories = opt[1]         

if input_file == "" or filter_file == "":
    print("Usage: get_review_id_by_category.py -i [in_file] -f [filter_file] -c [category, category,...]")
else:
    process_csv(input_file, filter_file, categories)
