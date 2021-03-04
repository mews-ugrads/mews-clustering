#!/usr/bin/python3

##
# @file  determine-weights.py
# @desc  determine the lowest and highest weights...
#        ... per key in the graph
# @note  graph is dict with key of img name. val is another ...
#        ... dict with key as neighbor img name. val is list (length 4) ...
#        ... of weights corresponding to methods.
##


### Imports ###

import os
import sys
import math
from MewsGraph import MewsGraph


### Functions ###

##
# @desc    prints usage message
# --
# @param   exit_code  0 or 1
# @return  g          NA
##
def usage(exit_code=0):
	print('''Usage: {} IN_FILE
		- IN_FILE   input file (.txt)'''.format(os.path.basename(sys.argv[0])))
	sys.exit(exit_code)


##
# @desc    determines low and high values of weights
# --
# @param   g  graph
# @param   m  method (enum)
# @return  NA
##
def print_range(g):

    # Define Ranges
    full_img = [math.inf, 0]
    rel_txt  = [math.inf, 0]
    sub_img  = [math.inf, 0]
    ocr      = [math.inf, 0]

    # Computer 
    for v in g:
        for n in g[v]:
            full_img[0] = min(g[v][n][MewsGraph.FULL_IMG], full_img[0])
            full_img[1] = max(g[v][n][MewsGraph.FULL_IMG], full_img[1])
            rel_txt[0]  = min(g[v][n][MewsGraph.REL_TXT], rel_txt[0])
            rel_txt[1]  = max(g[v][n][MewsGraph.REL_TXT], rel_txt[1])
            sub_img[0]  = min(g[v][n][MewsGraph.SUB_IMG], sub_img[0])
            sub_img[1]  = max(g[v][n][MewsGraph.SUB_IMG], sub_img[1])
            ocr[0]      = min(g[v][n][MewsGraph.OCR], ocr[0])
            ocr[1]      = max(g[v][n][MewsGraph.OCR], ocr[1])

    # Print
    print('Ranges by Method')
    print(f'  Full Image Query: {full_img}')
    print(f'  Related Text: {rel_txt}')
    print(f'  Subimage: {sub_img}')
    print(f'  OCR: {ocr}')

    return


### Main Execution ###

if __name__ == '__main__':

    # Parse Command Line
    if len(sys.argv) != 2: usage(1)

    # Grab Input File
    fpath = sys.argv[1]

    # Convert to graph
    g = MewsGraph.load_txt(fpath)

    # Print Lows and Highs of Methods
    print_range(g)

