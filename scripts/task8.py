import csv
import sys
import getopt
import time

# This module takes the following arguments:
# '-i': nltk_file = Named entity file (result of find_named_entity_categories.py)
# '-r': review_file = File containing user rating
# '-d': id_column = Id column number in review_file
# '-f': review_column = Rating column number in review_file 
#
# For each named-entity category type we first collect the ids.
# Then using the filtered ids we calculate averages from reviews.
#
# Usage: python taks8.py -i [nltk_file] -r [review_file] -d [id_column] -f [review_column]


def parse_nltk_file(nltk_file):
    f = open(nltk_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')

    nltk_list = list()
    
    for row in csv_reader:
        nltk_list.append(row)
      
    f.close()

    return nltk_list

def parse_entity(nltk_list, entity):
    line_count = 0
    category_column = -1
    id_column = -1
    
    ids = list()
    ids.append(entity)
    
    for row in nltk_list:
        if len(row) == 0:
            continue
        if line_count == 0:
            try:
                category_column = row.index(entity)
                id_column = row.index("id")
            except:
                print("Error: Category not found:", entity)
                break
            line_count += 1
        elif int(row[category_column]) == 1:
            ids.append(row[id_column])

    return ids

def analyse_category(review_file, category, id_column, review_column):
    id_column = int(id_column)
    review_column = int(review_column)
    
    category_name = category.pop(0)
    num_ratings = 0
    sum_ratings = 0
    
    sum_filtered_ratings = 0
    num_filtered_ratings = 0
    
    f = open(review_file, "r", encoding='utf-8')
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    filtered = filter(lambda x: (x[id_column] in category), list(csv_reader))
    f.seek(0)
    next(csv_reader)
    for row in csv_reader:
        num_ratings += 1
        sum_ratings += float(row[review_column])

    f.close()
    
    for row in filtered:
        sum_filtered_ratings += float(row[review_column])
        num_filtered_ratings += 1

    print("<result>", "For named-entity type:", category_name, "</result>")
    print("<result>", "    From the total of", num_ratings, "reviews", num_filtered_ratings, "contain the type", "</result>")
    print("<result>", "    Average of all reviews:", "{:.2f}".format(sum_ratings / num_ratings), "</result>")
    print("<result>", "    Average of reviews with named-entity:", "{:.2f}".format(sum_filtered_ratings / num_filtered_ratings), "</result>")
    print()

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:r:d:f:')

nltk_file = ""
review_file = ""
id_column = ""
review_column = ""

for opt in opts:
    if opt[0] == '-i':
        nltk_file = opt[1]
    elif opt[0] == '-r':
        review_file = opt[1]
    elif opt[0] == '-d':
        id_column = opt[1]   
    elif opt[0] == '-f':
        review_column = opt[1]    


if nltk_file == "" or review_file == "" or id_column == "" or review_column == "":
    print("Usage: python taks8.py -i [nltk_file] -r [review_file] -d [id_column] -f [review_column]")
else:
    start_time = time.time()
    
    nltk_list = parse_nltk_file(nltk_file)
    entity_types = nltk_list[0]
 
    list_of_category_entries = []
    for entity in entity_types:
        if entity != "id":
            list_of_category_entries.append(parse_entity(nltk_list, entity))
    
    for category in list_of_category_entries:
        analyse_category(review_file, category, id_column, review_column)

    print('Finished in', "{:.2f}".format(time.time() - start_time), 'seconds.')
