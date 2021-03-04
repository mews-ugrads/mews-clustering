#!/usr/bin/python3

##
# @file  grab-most-related.py
# @desc  output graph to txt file that has weights of certain threshold
# @note  NA
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
	print('''Usage: {} [-f FULL_THRESH -r REL_THRESH -s SUB_THRESH -c OCR_THRESH] IN_FILE OUT_FILE
    -f  FULL_THRESH  Full Image Query Threshold
    -s  REL_THRESH   Related Text Threshold
    -s  SUB_THRESH   Subimage Threshold
    -c  OCR_THRESH   OCR Threshold'''.format(os.path.basename(sys.argv[0])))
	sys.exit(exit_code)


##
# @desc    insert vertices if nonexistent
# --
# @param   g        graph
# @param   source   node #1
# @param   target   node #2
# @return  NA
##
def init_vertices(g, source, target):
    if source not in g: g[source] = {}
    if target not in g: g[target] = {}
    if source not in g[target]: g[target][source] = MewsGraph.NUM_METHODS * [0]
    if target not in g[source]: g[source][target] = MewsGraph.NUM_METHODS * [0]
    

##
# @desc    returns new graph with edges that exceed certain threshold
# --
# @param   g
# @param   ful    threshold for full_image_query
# @param   rel    threshold for related_text
# @param   sub    threshold for subimage
# @param   ocr    threshold for ocr
# @return  min_g  minimized graph
##
def reduce_by_weight(g, ful, rel, sub, ocr):
    min_g = {}

    for source in g:
        for target in g[source]:

            # Add Weights If In Threshold
            weights = g[source][target]
            if weights[MewsGraph.FULL_IMG] >= ful:
                init_vertices(min_g, source, target)
                min_g[source][target][MewsGraph.FULL_IMG] = weights[MewsGraph.FULL_IMG]
                min_g[target][source][MewsGraph.FULL_IMG] = weights[MewsGraph.FULL_IMG]
            if weights[MewsGraph.REL_TXT] >= rel:
                init_vertices(min_g, source, target)
                min_g[source][target][MewsGraph.REL_TXT] = weights[MewsGraph.REL_TXT]
                min_g[target][source][MewsGraph.REL_TXT] = weights[MewsGraph.REL_TXT]
            if weights[MewsGraph.SUB_IMG] >= sub:
                init_vertices(min_g, source, target)
                min_g[source][target][MewsGraph.SUB_IMG] = weights[MewsGraph.SUB_IMG]
                min_g[target][source][MewsGraph.SUB_IMG] = weights[MewsGraph.SUB_IMG]
            if weights[MewsGraph.OCR] >= ocr:
                init_vertices(min_g, source, target)
                min_g[source][target][MewsGraph.OCR] = weights[MewsGraph.OCR]
                min_g[target][source][MewsGraph.OCR] = weights[MewsGraph.OCR]

    return min_g


### Main Execution ###

if __name__ == '__main__':

    # Set Defaults
    min_full_img = 4000
    min_rel_txt = 0.3
    min_sub_img = 1000
    min_ocr = 0.8

    # Grab Flags
    args = sys.argv[1:]
    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if (arg == '-f'):
            min_full_img = float(args.pop(0))
        elif (arg == '-r'):
            min_rel_txt = float(args.pop(0))
        elif (arg == '-s'):
            min_sub_img = float(args.pop(0))
        elif (arg == '-c'):
            min_ocr = float(args.pop(0))
        else:
            usage(1)
    
    # Grab Input File
    if len(args) != 2:
        usage(2)
    inpath = args.pop(0)
    outpath = args.pop(0)

    # Convert to graph
    g = MewsGraph.load_txt(inpath)

    # Minimize Based On Weights
    min_g = reduce_by_weight(g, min_full_img, min_rel_txt, min_sub_img, min_ocr)

    # Print Graph
    MewsGraph.dump_txt(min_g, outpath)
