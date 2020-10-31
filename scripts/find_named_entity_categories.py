import csv
import sys
import getopt
import time

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk import ne_chunk

# This module runs nltk tokenizer on a text in a single column in .csv file.
# It searches for named entities and their types.
# The first row of the input file is expected to be header.
# Results are written in a new file which contains
# the id of row and boolean status of appearance of certain category.
#
# Usage: find_named_entity_categories.py -i [in_file] -o [out_file] -c [column]

def process_csv(in_file, out_file, column):
    start_time = time.time()
    
    f = open(in_file, "r") 
    csv_reader = csv.reader(f, delimiter=',', quotechar='"')
    
    result = open(out_file, mode='w')
    csv_writer = csv.writer(result)

    review_col = int(column)
    entities_columns = ['id', 'location', 'person', 'organization', 'facility']
    line_count = 0

    pattern = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(pattern)
    
    for row in csv_reader:
        if line_count == 0:
            header = list()
            for sentiment in entities_columns:
                header.append(sentiment)

            csv_writer.writerow(header)
            line_count += 1
        else:
            has_location = 0
            has_person = 0
            has_organization = 0
            has_facility = 0

            review = row[review_col] 
            sentences = sent_tokenize(review)
            token_sentences = [word_tokenize(sent) for sent in sentences]
            pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]

            for sent in pos_sentences:
                chunked_sentences = ne_chunk(sent)
                cs = cp.parse(chunked_sentences)

                for tag in cs:
                    if isinstance(tag, nltk.tree.Tree):
                        label = tag.label()
                        if label == "LOCATION":
                            has_location = 1
                        elif label == "PERSON":
                            has_person = 1
                        elif label == "ORGANIZATION":
                            has_organization = 1
                        elif label == "FACILITY":
                            has_facility = 1

            result_row = [row[0], has_location, has_person, has_organization, has_facility]
            csv_writer.writerow(result_row)

    print('Processed', line_count, 'rows in', "{:.2f}".format(time.time() - start_time), 'seconds.')
    
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:c:')

input_file = ""
output_file = ""
column = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]
    elif opt[0] == '-c':
        column = opt[1]

if input_file == "" or output_file == "" or column == "":
    print("Usage: find_named_entity_categories.py -i [in_file] -o [out_file] -c [column]")
else:
    process_csv(input_file, output_file, column)
