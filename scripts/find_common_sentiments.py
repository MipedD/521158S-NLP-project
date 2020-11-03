import csv
import sys
import getopt
import time

# This module takes the following arguments:
# sentistrenght_file is the result of Sentitrenght analysis
# positive_column is the index of postive value column in sentistrenght_file
# negative_column is the index of negative value column in sentistrenght_file
# vader_file is the result of Vader analysis
# compound_column is the index of compound_column value column in vader_file
# empath_file is the file containing empath categories
#
# For each analysis we find positive and negative analysis
# and compile the intersection.
#
# Usage: python find_common_sentiments.py -s [sentistrenght_file] -p [positive_column] -n [negative_column] -v [vader_file] -c [compound_column] -e [empath_file]

def process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, posneg):
    ss_positive = int(ss_positive)
    ss_negative = int(ss_negative)
    pos_wanted = 1 if posneg == "positive" else 0
    
    f = open(sentistrenght_file, "r") 
    csv_reader = csv.reader(f, delimiter='\t', quotechar='"')

    line_count = 0
    senti_set = set()
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            if content:
                positive_sentiment = int(content[ss_positive])
                negative_sentiment = int(content[ss_negative])
                if positive_sentiment + negative_sentiment > 0 and pos_wanted == 1:
                    senti_set.add(content[0])
                elif positive_sentiment + negative_sentiment < 0 and pos_wanted == 0:
                    senti_set.add(content[0])
      
    f.close()
    print("<result>SentiStrength found", len(senti_set), posneg, "reviews.</result>")
    return senti_set

def process_vader(vader_file, vader_compound, posneg):
    vader_compound = int(vader_compound)
    pos_wanted = 1 if posneg == "positive" else 0
     
    f = open(vader_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    vader_set = set()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            compound = float(content[vader_compound])
            if compound > 0 and pos_wanted == 1:
                vader_set.add(content[0])
            elif compound < 0 and pos_wanted == 0:
                vader_set.add(content[0])
            line_count += 1

    f.close()
    print("<result>Vader found", len(vader_set), posneg, "reviews.</result>")
    return vader_set
    
def filter_empath(empath_file, ids):
    f = open(empath_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    filtered = filter(lambda x: (x[0] in ids), list(csv_reader))
    f.close()
    return list(filtered)

def check_results(empath_file, positive_set, negative_set):
    positive_list = filter_empath(empath_file, positive_set)
    negative_list = filter_empath(empath_file, negative_set)
    
    f = open(empath_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    all_sum = 0
    neutral_sum = 0
    line_count = 0
    neutral_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[0] not in positive_set and row[0] not in positive_set:
                neutral_sum += int(row[1])
                neutral_count += 1
            all_sum += int(row[1])
            line_count += 1
    f.close()
    
    positive_count = len(positive_list)
    negative_count = len(negative_list)
    positive_sum = 0
    negative_sum = 0

    for row in positive_list:
        positive_sum += int(row[1])
        
    for row in negative_list:
        negative_sum += int(row[1])
        
    all_avg = all_sum / (line_count - 1)
    positive_avg = positive_sum / positive_count
    negative_avg = negative_sum / negative_count
    neutral_avg = neutral_sum / neutral_count
    
    print("<result>")
    print("Total # of reviews:", line_count - 1)
    print("# Intersection of positive sentiment:", positive_count)
    print("# Intersection of negative sentiment:", negative_count)
    print("Average of all reviews:", "{:.2f}".format(all_avg))
    print("Average of reviews with positive sentiment:", "{:.2f}".format(positive_avg))
    print("Average of reviews with neutral sentiment:", "{:.2f}".format(neutral_avg))
    print("Average of reviews with negative sentiment:", "{:.2f}".format(negative_avg))
    print("</result>")
    
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 's:p:n:v:c:e:')

sentistrenght_file = ""
ss_positive = ""
ss_negative = ""
vader_file = ""
vader_compound = ""
empath_file = ""

for opt in opts:
    if opt[0] == '-s':
        sentistrenght_file = opt[1]
    elif opt[0] == '-p':
        ss_positive = opt[1]
    elif opt[0] == '-n':
        ss_negative = opt[1]   
    elif opt[0] == '-v':
        vader_file = opt[1]    
    elif opt[0] == '-c':
        vader_compound = opt[1]  
    elif opt[0] == '-e':
        empath_file = opt[1]
    

if sentistrenght_file == "" or ss_positive == "" or ss_negative == ""  or vader_file == "" or vader_compound == "":
    print("Usage: python find_common_sentiments.py -s [sentistrenght_file] -p [positive_column] -n [negative_column] -v [vader_file] -c [compound_column] -e [empath_file]")
else:
    start_time = time.time()
    
    senti_positive = process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, "positive")
    senti_negative = process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, "negative")
    vader_positive = process_vader(vader_file, vader_compound, "positive")
    vader_negative = process_vader(vader_file, vader_compound, "negative")
    
    senti_positive &= vader_positive
    senti_negative &= vader_negative
    
    if empath_file != "":
        check_results(empath_file, senti_positive, senti_negative)

    print('Finished in', "{:.2f}".format(time.time() - start_time), 'seconds.')

