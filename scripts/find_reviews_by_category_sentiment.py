import csv
import sys
import getopt
import time

# This module takes two files as arguments:
# in_file is the result of empath_categories.py
# filter_file is the result of find_empath_categories.py 
#
# For each review all the found empath categories are cross checked with a cutoff point.
# Result is saved in a new file containing id, review, has_positive, has_negative
#
# Usage: python find_reviews_by_category_sentiment.py -i [in_file] -f [filter_file] -o [out_file] -c [cutoff]

def process_csv(in_file, filter_file, out_file, cutoff):
    start_time = time.time()
    
    f = open(filter_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    positive = ""
    negative = ""
    
    # First find the positive and negative categories from filter_file.
    for row in csv_reader:
        row_str = str(row)
        row_str = row_str.split(":")
        if row_str[0].find("positive") != -1:
            positive = row_str[1]            
        elif row_str[0].find("negative") != -1:
            negative = row_str[1]       

    f.close()
    
    f = open(in_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    fieldnames = ['id', 'rating', 'has_positive', 'has_negative']
    result = open(out_file, mode='w')
    csv_writer = csv.DictWriter(result, fieldnames=fieldnames)
    csv_writer.writeheader()

    cutoff_point = float(cutoff)
    line_count = 0
    
    # Then go through the categories in reviews and mark if positive and/or negative is found.
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:            
            has_positive = 0
            has_negative = 0
            categories = row[3]
            categories = eval(categories)

            for category, score in categories.items():                
                if score > cutoff_point:
                    #print(category, score)
                    if positive.find(category) > 0:
                        has_positive = 1
                    elif negative.find(category) > 0:
                        has_negative = 1
                            
            csv_writer.writerow({'id': row[0], 'rating': row[1], 'has_positive': str(has_positive), 'has_negative': str(has_negative)})  
            line_count += 1
            
    result.close()    
    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
    print_results(out_file)
    
def print_results(in_file):
    f = open(in_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    tester = filter(lambda x: (x[1] in ("5", "4") and x[2] in ("1")), list(csv_reader))
    positive_hits = sum(1 for line in tester)
    f.seek(0)    
    
    tester = filter(lambda x: (x[1] in ("1", "2") and x[3] in ("1")), list(csv_reader))
    negative_hits = sum(1 for line in tester)
    f.seek(0)
    
    total = sum(1 for line in f) - 1
    f.seek(0)
    ratings = [rec[1] for rec in csv_reader] 
    ones = ratings.count('1')
    twos = ratings.count('2')
    threes = ratings.count('3')
    fours = ratings.count('4')
    fives = ratings.count('5')
    
    f.close()
    print("Total # reviews:", total)
    print("1:", ones, "2:", twos, "3:", threes, "4:", fours, "5:", fives)
    print("Out of", fours + fives, "postive reviews", positive_hits, "had positive categories", "{:.2f}".format(100 * (positive_hits / (fours + fives))), "%")
    print("Out of", ones + twos, "negative reviews", negative_hits, "had negative categories", "{:.2f}".format(100 * (negative_hits / (ones + twos))), "%")
    

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:c:f:')

input_file = ""
filter_file = ""
output_file = ""
cutoff = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-f':
        filter_file = opt[1]       
    elif opt[0] == '-c':
        cutoff = opt[1]         

if input_file == "" or output_file == "" or filter_file == "":
    print("Usage: python find_reviews_by_category_sentiment.py -i [in_file] -f [filter_file] -o [out_file] -c [cutoff]")
else:
    process_csv(input_file, filter_file, output_file, cutoff)
