import csv
import sys
import getopt
import time
import collections

# This module takes the following arguments:
# '-s': sentistrenght_file = File with SentiStrenght analysis
# '-a': ss_id = Id column number in sentistrenght_file
# '-p': ss_positive = Positive column number in sentistrenght_file
# '-n': ss_negative = Negative column number in sentistrenght_file 
# '-v': vader_file = File with Vader analysis
# '-b': vader_id = Id column number in vader_file
# '-c': vader_compound = Compound column number in vader_file
# '-e': empath_file = File with Empath categories
# '-i': empath_id_column = Id column number in empath_file   
# '-r': empath_rating_column = Rating column number in empath_file 
# '-g': empath_category_column = Categories column in empath_file
# '-l': category_sentiments_file = File with categories categorized in positive and negative
#
# For each analysis we find positive and negative analysis
# and compile the intersection.


def process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, posneg, ss_id):
    ss_positive = int(ss_positive)
    ss_negative = int(ss_negative)
    ss_id = int(ss_id)
    pos_wanted = 1 if posneg == "positive" else 0
    
    f = open(sentistrenght_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')

    line_count = 0
    senti_set = set()
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            if content:
                try:
                    positive_sentiment = float(content[ss_positive])
                    negative_sentiment = float(content[ss_negative])
                    if positive_sentiment + negative_sentiment > 0 and pos_wanted == 1:
                        senti_set.add(content[ss_id])
                    elif positive_sentiment + negative_sentiment < 0 and pos_wanted == 0:
                        senti_set.add(content[ss_id])
                except:
                    continue

    f.close()

    print("<result>SentiStrength found", len(senti_set), posneg, "reviews.</result>")
    return senti_set

def process_vader(vader_file, vader_compound, posneg, vader_id):
    vader_compound = int(vader_compound)
    vader_id = int(vader_id)
    pos_wanted = 1 if posneg == "positive" else 0
     
    f = open(vader_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    vader_set = set()
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            content = list(row)
            try:
                compound = float(content[vader_compound])
                if compound > 0 and pos_wanted == 1:
                    vader_set.add(content[vader_id])
                elif compound < 0 and pos_wanted == 0:
                    vader_set.add(content[vader_id])
                line_count += 1
            except:
                continue

    f.close()
    print("<result>Vader found", len(vader_set), posneg, "reviews.</result>")
    return vader_set
    
def filter_empath(empath_file, empath_id_column, ids):
    f = open(empath_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    filtered = filter(lambda x: (x[empath_id_column] in ids), list(csv_reader))
    f.close()
    return list(filtered)

def filter_categoty_sentiments(category_sentiments_file, category):
    print(category_sentiments_file)
    f = open(category_sentiments_file, "r", encoding='utf-8')
    categories_str = f.read()
    f.close()
    
    start = categories_str.find(category)
    if start == -1:
        return list()
    
    start += len(category) + 1 
    end = categories_str.find("}", start)
    categories_str = categories_str[int(start):int(end)]
    
    return categories_str.split(",")    

def category_freq(category_list, category_column):
    category_count =  dict()
    
    for line in category_list:
        categories = line[category_column]
        categories = eval(categories)
        for category in categories:
            if category in category_count:
                category_count[category] = category_count[category] + 1
            else:
                category_count[category] = 1
              
    return category_count

def check_results(empath_file, empath_id_column, empath_rating_column, empath_category_column, category_sentiments_file, positive_set, negative_set):
    empath_id_column = int(empath_id_column)
    empath_rating_column = int(empath_rating_column)
    empath_category_column = int(empath_category_column)
    positive_list = filter_empath(empath_file, empath_id_column, positive_set)
    negative_list = filter_empath(empath_file, empath_id_column, negative_set)
    positive_categories = filter_categoty_sentiments(category_sentiments_file, "positive:")
    negative_categories = filter_categoty_sentiments(category_sentiments_file, "negative:")
    
    f = open(empath_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    all_sum = 0
    neutral_sum = 0
    line_count = 0
    neutral_count = 0
    positive_reviews_positive_category = set()
    negative_reviews_negative_category = set()
  
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[empath_id_column] in negative_set:
                for category in negative_categories:
                    if row[empath_category_column].find(category) != -1:
                        negative_reviews_negative_category.add(row[empath_id_column])
                        
            elif row[empath_id_column] not in positive_set and row[empath_id_column] not in positive_set:
                neutral_sum += float(row[empath_rating_column])
                neutral_count += 1

            elif row[empath_id_column] in positive_set:   
                for category in positive_categories:
                    if row[empath_category_column].find(category) != -1:
                        positive_reviews_positive_category.add(row[empath_id_column])
                        
            all_sum += float(row[empath_rating_column])
            line_count += 1
    f.close()
    
    all_postive_list = filter_empath(empath_file, empath_id_column, positive_reviews_positive_category)
    all_negative_list = filter_empath(empath_file, empath_id_column, negative_reviews_negative_category)
    positive_review_and_category_count = len(positive_reviews_positive_category)
    negative_review_and_category_count = len(negative_reviews_negative_category)
    positive_count = len(positive_list)
    negative_count = len(negative_list)
    positive_sum = 0
    negative_sum = 0
    all_positive_sum = 0
    all_negative_sum = 0
    
    positive_categories_count = category_freq(all_postive_list, empath_category_column)
    negative_categories_count = category_freq(all_negative_list, empath_category_column)

    for row in positive_list:
        positive_sum += float(row[empath_rating_column])
        
    for row in negative_list:
        negative_sum += float(row[empath_rating_column])
        
    for row in all_postive_list:
        all_positive_sum += float(row[empath_rating_column])
        
    for row in all_negative_list:
        all_negative_sum += float(row[empath_rating_column])
        
    all_avg = all_sum / (line_count - 1)
    positive_avg = positive_sum / positive_count
    negative_avg = negative_sum / negative_count
    neutral_avg = neutral_sum / neutral_count
    all_positive_avg = all_positive_sum / positive_review_and_category_count
    all_negative_avg = all_negative_sum / negative_review_and_category_count
    
    #print("<result>")
    print("# Total of reviews:", line_count - 1)
    print("# Intersection of positive sentiment:", positive_count)
    print("# Intersection of negative sentiment:", negative_count)
    print("# Positive sentiment and category:", positive_review_and_category_count)
    print("# Negative sentiment and category:", negative_review_and_category_count)
    print("Average of all reviews:", "{:.2f}".format(all_avg))
    print("Average of reviews with positive sentiment:", "{:.2f}".format(positive_avg))
    print("Average of reviews with neutral sentiment:", "{:.2f}".format(neutral_avg))
    print("Average of reviews with negative sentiment:", "{:.2f}".format(negative_avg))
    print("Average of reviews with positive sentiment and category:", "{:.2f}".format(all_positive_avg))
    print("Average of reviews with negative sentiment and category:", "{:.2f}".format(all_negative_avg), "\n")
    
    print("Category frequency of reviews with positive sentiments:")
    for w in sorted(positive_categories_count, key=positive_categories_count.get, reverse=True):
        print(w, positive_categories_count[w])
    print("\nCategory frequency of reviews with negative sentiments:")
    for w in sorted(negative_categories_count, key=negative_categories_count.get, reverse=True):
        print(w, negative_categories_count[w])
    #print("</result>")
    
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 's:p:n:v:c:e:i:r:l:g:a:b:')

sentistrenght_file = ""
ss_positive = ""
ss_negative = ""
ss_id = ""
vader_file = ""
vader_compound = ""
vader_id = ""
empath_file = ""
empath_id_column = ""
empath_rating_column = ""
empath_category_column = ""
category_sentiments_file = ""

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
    elif opt[0] == '-i':
        empath_id_column = opt[1]     
    elif opt[0] == '-r':
        empath_rating_column = opt[1]
    elif opt[0] == '-l':
        category_sentiments_file = opt[1]  
    elif opt[0] == '-g':
        empath_category_column = opt[1]      
    elif opt[0] == '-a':
        ss_id = opt[1]        
    elif opt[0] == '-b':
        vader_id = opt[1]     

if sentistrenght_file == "" or ss_positive == "" or ss_negative == ""  or vader_file == "" or vader_compound == "":
    print("Usage: python find_common_sentiments.py -s [sentistrenght_file] -p [positive_column] -n [negative_column] -v [vader_file] -c [compound_column] -e [empath_file]")
else:
    start_time = time.time()
    
    senti_positive = process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, "positive", ss_id)
    senti_negative = process_sentistrenght(sentistrenght_file, ss_positive, ss_negative, "negative", ss_id)
    vader_positive = process_vader(vader_file, vader_compound, "positive", vader_id)
    vader_negative = process_vader(vader_file, vader_compound, "negative", vader_id)
    
    senti_positive &= vader_positive
    senti_negative &= vader_negative
    
    if empath_file != "":
        check_results(empath_file, empath_id_column, empath_rating_column, empath_category_column, category_sentiments_file, senti_positive, senti_negative)

    print('Finished in', "{:.2f}".format(time.time() - start_time), 'seconds.')

