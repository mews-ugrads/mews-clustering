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
	print('''Usage: {} IN_FILE OUT_FILE
		- IN_FILE   input file (.txt)
                - OUT_FILE  output file (.txt)'''.format(os.path.basename(sys.argv[0])))
	sys.exit(exit_code)

def reduce_by_weight(g, ful, rel, sub, ocr):
    min_g = {}

    for source in g:
        for target in g[v]:
            # Insert Vertices
            if source not in g: g[source] = {}
            if target not in g: g[target] = {}
            if source not in g[target]: g[target][source] = MewsGraph.NUM_METHODS * [0]
            if target not in g[source]: g[source][target] = MewsGraph.NUM_METHODS * [0]

            # Add Weights
            if method == "full_image_query":
                g[source][target][MewsGraph.FULL_IMG] += weight
                g[target][source][MewsGraph.FULL_IMG] += weight
            if method == "related_text":
                g[source][target][MewsGraph.REL_TXT] += weight
                g[target][source][MewsGraph.REL_TXT] += weight
            if method == "subimage":
                g[source][target][MewsGraph.SUB_IMG] += weight
                g[target][source][MewsGraph.SUB_IMG] += weight
            if method == "ocr":
                g[source][target][MewsGraph.OCR] += weight
                g[target][source][MewsGraph.OCR] += weight


### Main Execution ###

if __name__ == '__main__':

    # Parse Command Line
    if len(sys.argv) != 3: usage(1)

    # Set Defaults
    min_full_img = 4000
    min_rel_txt = 0.3
    min_sub_img = 1000
    min_ocr = 0.8

    # Grab Input File
    inpath = sys.argv[1]

    # Convert to graph
    g = MewsGraph.load_txt(inpath)

    # Minimize Based On Weights
    min_g = reduce_by_weight(g, min_full_img, min_rel_txt, min_sub_img, min_ocr)

    # Print Graph
    MewsGraph.print(min_g)
