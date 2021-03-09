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
    g = MewsGraph()
    g.load_txt(inpath)

    # Minimize Based On Weights
    g.reduceBySoftWeights(min_full_img, min_rel_txt, min_sub_img, min_ocr)

    # Print Graph
    g.dump_txt(outpath)
