# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:31:19 2020

@author: Miika
"""

import pandas as pd
import sys
import getopt
import os

def merge(a_ss_input, a_target):
    data = pd.read_csv(a_target, sep=',', encoding='utf-8')
    data["sentiment.positive.sentistrength"] = a_ss_input["1"]
    data["sentiment.negative.sentistrength"] = a_ss_input["-1"]
    data["sentiment.overall.sentistrength"] = a_ss_input["1"] + a_ss_input["-1"]
    return data

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
    print("Usage: -i [in_file] -o [out_file]")
else:
    print("Reading sentistrength output..")
    data = pd.read_csv(input_file, sep='\t', encoding='ISO-8859-1')
    print("Mergin data..")
    data = merge(data, output_file)
    print("Saving file..")
    data.to_csv(output_file, index=False, encoding='utf-8')
    print("Removing temporary file..")
    os.remove(input_file)
