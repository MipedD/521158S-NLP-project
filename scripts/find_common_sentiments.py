import csv
import sys
import getopt
import time

# This module takes two files as arguments:
# sentistrenght_file is the result of Sentitrenght analysis
# vader_file is the result of Vader analysis
#
# For each analysis we find positive and negative analysis
# and compile the intersection.
#
# Usage: python find_common_sentiments.py -s [sentistrenght_file] -v [vader_file]

def process_csv(sentistrenght_file, vader_file):
    start_time = time.time()
    
    f = open(sentistrenght_file, "r") 
    csv_reader = csv.reader(f, delimiter='\t', quotechar='"')

    line_count = 0
    senti_positive = set()
    senti_negative = set()
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            if content:
                positive_sentiment = int(content[3])
                negative_sentiment = int(content[4])
                if positive_sentiment + negative_sentiment > 0:
                    senti_positive.add(content[0])
                elif positive_sentiment + negative_sentiment < 0:
                    senti_negative.add(content[0])
                line_count += 1
      
    f.close()
 
    f = open(vader_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    vader_positive = set()
    vader_negative = set()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            compound = float(content[6])
            if compound > 0:
                vader_positive.add(content[0])
            elif compound < 0:
                vader_negative.add(content[0])
            line_count += 1

    f.close()
    
    print("# SentiStrenght positive:", len(senti_positive))
    print("# SentiStrenght negative:", len(senti_negative))
    
    print("# Vader positive:", len(vader_positive))
    print("# Vader negative:", len(vader_negative))
    
    senti_positive &= vader_positive
    senti_negative &= vader_negative
    
    print("# Positive intersection:", len(senti_positive))
    print("# Negative intersection:", len(senti_negative))
    print('Finished in', "{:.2f}".format(time.time() - start_time), 'seconds.')
    
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 's:v:')

sentistrenght_file = ""
vader_file = ""

for opt in opts:
    if opt[0] == '-s':
        sentistrenght_file = opt[1]
    elif opt[0] == '-v':
        vader_file = opt[1]             

if sentistrenght_file == "" or vader_file == "":
    print("Usage: python find_common_sentiments.py -s [sentistrenght_file] -v [vader_file]")
else:
    process_csv(sentistrenght_file, vader_file)
