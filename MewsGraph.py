#!/usr/bin/python3

##
# @file  MewsGraph.py
# @desc  creates static class to help with loading and declaring vars
# @note  graph is dict with key of img name. val is another ...
#        ... dict with key as neighbor img name. val is list (length 4) ...
#        ... of weights corresponding to methods.
##

### Imports

import sys


### MewsGraph

class MewsGraph:

    # Static Variables
    NUM_METHODS = 4
    FULL_IMG    = 0
    REL_TXT     = 1
    SUB_IMG     = 2
    OCR         = 3

    def __init__(self):
        self.g = {}

    ##
    # @desc    converts txt file to graph
    # --
    # @param   fpath  file path for txt file; path has format "u;v;method;weight;x;x;x;"
    # @return  g      graph in format of {v1: { e1: [w1, w2, w3, w4], e2: [...] }, v2: ...}
    ##
    def load_txt(self, fpath):
        # Initialize Graph
        self.g = {}

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
            if source not in self.g: self.g[source] = {}
            if target not in self.g: self.g[target] = {}
            if source not in self.g[target]: self.g[target][source] = MewsGraph.NUM_METHODS * [0]
            if target not in self.g[source]: self.g[source][target] = MewsGraph.NUM_METHODS * [0]

            # Add Weights
            if method == "full_image_query":
                self.g[source][target][MewsGraph.FULL_IMG] += weight
                self.g[target][source][MewsGraph.FULL_IMG] += weight
            if method == "related_text":
                self.g[source][target][MewsGraph.REL_TXT] += weight
                self.g[target][source][MewsGraph.REL_TXT] += weight
            if method == "subimage":
                self.g[source][target][MewsGraph.SUB_IMG] += weight
                self.g[target][source][MewsGraph.SUB_IMG] += weight
            if method == "ocr":
                self.g[source][target][MewsGraph.OCR] += weight
                self.g[target][source][MewsGraph.OCR] += weight

        f.close()

    def nodes(self):
        return self.g.keys()

    def neighbors(self, u):
        return self.g[u].keys()

    def weights(self, u, v):
        return self.g[u][v]

    def dump_txt(g, fpath):

        # Open File
        try:
            f = open(fpath, 'w')
        except:
            print(f'Cannot write to "{fpath}"')
            sys.exit(1)
        
        # Write First Line
        f.write('node1; node2; key; weight; label; text1; text2\n')

        # Write All Other Lines
        methods = ['full_image_query', 'related_text', 'subimage', 'ocr']
        for v in g:
            for n in g[v]:
                for method_i in range(MewsGraph.NUM_METHODS):
                    f.write(f'{v};{n};{methods[method_i]};{g[v][n][method_i]};;;;\n')

        f.close()
        return

    ##
    # @desc    prints graph
    # --
    # @param   g  graph
    # @return  NA
    ##
    def print(self):

        # Every Vertex
        for v in self.nodes():
            print(f'{v}:')

            # Every Neighbor
            for n in self.neighbors(v):

                # Every Edge Between Them
                print(f'    {n}: [{self.weights(v,n)[MewsGraph.FULL_IMG]}, {self.weights(v,n)[MewsGraph.REL_TXT]}, {self.weights(v,n)[MewsGraph.SUB_IMG]}, {self.weights(v,n)[MewsGraph.OCR]}]')

