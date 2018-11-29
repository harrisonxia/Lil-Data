#
#  Author: Lil Data
#  Email: cxa25@sfu.ca
#  CMPT 732 Lab Final Project
#  Date: 11/13/2018
#
import sys
assert sys.version_info >= (3, 5) 
import re
import os
import json

def clean_json(string):
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    return string

if __name__ == '__main__':
    inputs = sys.argv[1] # input raw data

    for file in os.listdir(inputs):
        print(file)
        json_data=open('data/'+file).read()
        cleaned = clean_json(json_data)
        with open('data/clean/'+file, 'w') as outfile:
            json.dump(json.loads(cleaned), outfile, indent=4, separators=(',', ': '))

