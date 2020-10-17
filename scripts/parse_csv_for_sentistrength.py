# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:38:56 2020

@author: Miika

Notes:  sentistrength wants text in a format such that each line contains
        the text to be analyzed. This means that the reviews.text needs to
        be extracted from the dataset into a separate file which can be passed
        to sentistrength.

        Pass -i <file> to specify the input file and -o <file> to specify the
        output file. -c <column_name> selects the column to extract
"""

import csv
import sys
import getopt

dataset_delimiter = ','
dataset_newline = '\n'

#Function to read the dataset into 2d array. Returns dictionary {header, data}
def read_data_from_csv(a_file, a_delimiter, a_newline):
    print("Reading dataset...")
    data_rows = []
    #Open file and read rows into data
    with open(a_file, newline=a_newline, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=a_delimiter)
        for row in spamreader:
            data_rows.append(row)
    ret_dict = {"header" : data_rows.pop(0), "body" : data_rows}
    dbgmsg = "=> Success. Dataset contains " + str(len(data_rows)) + " rows and " + str(len(ret_dict["header"])) + " columns"
    print(dbgmsg)
    return ret_dict

#Write dataset column a_column into a file in a format sentistrength approves
def dataset_column_to_txt(a_data, a_column, a_output_file_name):
    #Write reviews.text from each row to a .txt file. Text separated with "\n"
    dbgmsg = "Writing column \"" + a_data["header"][a_column] + "\" to file \"" + a_output_file_name + "\"..."
    print(dbgmsg)
    f = open(a_output_file_name, "a")
    #Sentistrenght expects a header
    f.write("Source text\n")
    for row in a_data["body"]:
        f.write(row[a_column] + "\n")
    f.close()
    dbgmsg = "=> Probably a success."
    print(dbgmsg)

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

if input_file == "" or output_file == "":
    print("Please specify input and output file")
else:
    data = read_data_from_csv(input_file, dataset_delimiter, dataset_newline)
    index = data["header"].index(column)
    if index != -1:
        dataset_column_to_txt(data, index, output_file)
    else:
        print("Invalid column.")
