#!/usr/bin/python3

##
# @file  MewsGraph.py
# @desc  creates static class to help with loading and declaring vars
# @note  graph is dict with key of img name. val is another ...
#        ... dict with key as neighbor img name. val is list (length 4) ...
#        ... of weights corresponding to methods.
##
import sys

class MewsGraph:

    # Static Variables
    NUM_METHODS = 4
    FULL_IMG    = 0
    REL_TXT     = 1
    SUB_IMG     = 2
    OCR         = 3

    ##
    # @desc    converts txt file to graph
    # --
    # @param   fpath  file path for txt file; path has format "u;v;method;weight;x;x;x;"
    # @return  g      graph in format of {v1: { e1: [w1, w2, w3, w4], e2: [...] }, v2: ...}
    ##
    @staticmethod
    def load_txt(fpath):
        # Initialize Graph
        g = {}

        # Open File
        try:
            f = open(fpath, 'r')
        except:
            print(f'Cannot open "{fpath}"')
            sys.exit(1)

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

        f.close()
        return g


    ##
    # @desc    prints graph
    # --
    # @param   g  graph
    # @return  NA
    ##
    @staticmethod
    def print(g):

        # Every Vertex
        for v in g:
            print(f'{v}:')

            # Every Neighbor
            for n in g[v]:

                # Every Edge Between Them
                print(f'    {n}: [{g[v][n][0]}, {g[v][n][1]}, {g[v][n][2]}, {g[v][n][3]}]')

