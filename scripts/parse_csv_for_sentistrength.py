# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:38:56 2020

@author: Miika

Notes:  sentistrength wants text in a format such that each line contains
        the text to be analyzed. This means that the reviews.text needs to
        be extracted from the dataset into a separate file which can be passed
        to sentistrength.
"""

import sys
import getopt
import pandas as pd

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:o:')

input_file = ""
output_file = ""

for opt in opts:
    if opt[0] == '-i':
        input_file = opt[1]
    elif opt[0] == '-o':
        output_file = opt[1]

if input_file == "" or output_file == "":
    print("Please specify input and output file")
else:
    print("Reading dataset:", input_file)
    data = pd.read_csv(input_file, sep=',', encoding='utf_8')
    print("Preparing dataset for SentiStrength, writing modified copy to", output_file)
    data.to_csv(output_file, index=False, encoding='utf_8', sep='\t')
    print("<result>Dataset ready for SentiStrength</result>")
