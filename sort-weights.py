#!/usr/bin/python3

##
# @file  sort-weights.py
# @desc  NA
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
	print('''Usage: {} [-f FULL_AMT -r REL_AMT -s SUB_AMT -c OCR_AMT] IN_FILE
    -f  FULL_THRESH  Full Image Amount
    -s  REL_THRESH   Related Text Amount
    -s  SUB_THRESH   Subimage Amount
    -c  OCR_THRESH   OCR Amount'''.format(os.path.basename(sys.argv[0])))
	sys.exit(exit_code)

def printSortedWeights(g, f, r, s, o):
    full_img = []
    rel_txt = []
    sub_img = []
    ocr = []
    for v in g.nodes():
        for n in g.neighbors(v):
            weights = g.weights(v,n)
            full_img.append(weights[MewsGraph.FULL_IMG])
            rel_txt.append(weights[MewsGraph.REL_TXT])
            sub_img.append(weights[MewsGraph.SUB_IMG])
            ocr.append(weights[MewsGraph.OCR])

    if f > 0 and f <= len(full_img):
        full_img = sorted(full_img, reverse=True)[0:f-1]
        print(f'Full Image Sorted Weights: {full_img}')
        
    if r > 0 and r <= len(rel_txt):
        rel_txt = sorted(rel_txt, reverse=True)[0:r-1]
        print(f'Related Text Sorted Weights: {rel_txt}')

    if s > 0 and s <= len(sub_img):
        sub_img = sorted(sub_img, reverse=True)[0:s-1]
        print(f'Sub Image Sorted Weights: {sub_img}')

    if o > 0 and o <= len(ocr):
        ocr = sorted(ocr, reverse=True)[0:o-1]
        print(f'OCR Sorted Weights: {ocr}')


### Main Execution ###

if __name__ == '__main__':

    # Set Defaults
    full_img_amt = 10
    rel_txt_amt  = 10
    sub_img_amt  = 10
    ocr_amt      = 10

    # Grab Flags
    args = sys.argv[1:]
    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if (arg == '-f'):
            full_img_amt = int(args.pop(0))
        elif (arg == '-r'):
            rel_txt_amt = int(args.pop(0))
        elif (arg == '-s'):
            sub_img_amt = int(args.pop(0))
        elif (arg == '-c'):
            ocr_amt = int(args.pop(0))
        else:
            usage(1)
    
    # Grab Input File
    if len(args) != 1:
        usage(2)
    inpath = args.pop(0)

    # Convert to graph
    g = MewsGraph()
    g.load_txt(inpath)

    # Print Highest
    printSortedWeights(g, full_img_amt, rel_txt_amt, sub_img_amt, ocr_amt)

