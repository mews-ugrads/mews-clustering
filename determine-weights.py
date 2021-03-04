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

### Globals ###
NUM_METHODS = 4
FULL_IMG    = 0
REL_TXT     = 1
SUB_IMG     = 2
OCR         = 3


### Functions ###

##
# @desc    prints usage message
# --
# @param   exit_code  0 or 1
# @return  g          NA
##
def usage(exit_code=0):
	print('''Usage: {} IN_FILE
		- IN_FILE   input file (.pov)'''.format(os.path.basename(sys.argv[0])))
	sys.exit(exit_code)


##
# @desc    converts txt file to graph
# --
# @param   fpath  file path for txt file
# @return  g      graph in format of {v1: { e1: [w1, w2, w3, w4], e2: [...] }, v2: ...}
##
def convert_txt(fpath):
    graph = {}
    
    f = open(fpath, 'r')

    # Ignore First Line
    next(f)

    # Loop Through Lines
    for line in f:
        # Grab Items
        items = line.rstrip().split(';')
        
        # Grab Attributes
        source = items[0]
        target = items[1]
        method = items[2]
        weight = float(items[3])

        # Insert Vertices
        if source not in graph: graph[source] = {}
        if target not in graph: graph[target] = {}
        if source not in graph[target]: graph[target][source] = NUM_METHODS * [0]
        if target not in graph[source]: graph[source][target] = NUM_METHODS * [0]

        # Add Weights
        if method == "full_image_query":
            graph[source][target][FULL_IMG] += weight
            graph[target][source][FULL_IMG] += weight
        if method == "related_text":
            graph[source][target][REL_TXT] += weight
            graph[target][source][REL_TXT] += weight
        if method == "subimage":
            graph[source][target][SUB_IMG] += weight
            graph[target][source][SUB_IMG] += weight
        if method == "ocr":
            graph[source][target][OCR] += weight
            graph[target][source][OCR] += weight

    f.close()

    return graph

##
# @desc    prints graph
# --
# @param   g  graph
# @return  NA
##
def print_graph(g):

    # Every Vertex
    for v in g:
        print(f'{v}:')

        # Every Neighbor
        for n in g[v]:

            # Every Edge Between Them
            print(f'    {n}: [{g[v][n][0]}, {g[v][n][1]}, {g[v][n][2]}, {g[v][n][3]}]')


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
            full_img[0] = min(g[v][n][FULL_IMG], full_img[0])
            rel_txt[0]  = min(g[v][n][REL_TXT], rel_txt[0])
            sub_img[0]  = min(g[v][n][SUB_IMG], sub_img[0])
            ocr[0]      = min(g[v][n][OCR], ocr[0])
            full_img[1] = max(g[v][n][FULL_IMG], full_img[1])
            rel_txt[1]  = max(g[v][n][REL_TXT], rel_txt[1])
            sub_img[1]  = max(g[v][n][SUB_IMG], sub_img[1])
            ocr[1]      = max(g[v][n][OCR], ocr[1])

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
    g = convert_txt(fpath)

    # Print Graph
    #print_graph(g)

    # Print Lows and Highs of Methods
    print_range(g)

