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

    def initEdge(self, u, v):
        if u not in self.g: self.g[u] = {}
        if v not in self.g: self.g[v] = {}
        if u not in self.g[v]: self.g[v][u] = MewsGraph.NUM_METHODS * [0]
        if v not in self.g[u]: self.g[u][v] = MewsGraph.NUM_METHODS * [0]

    def removeEdge(self, u, v):
        if u not in self.g: return
        if v not in self.g: return
        if u not in self.g[v]: return
        if v not in self.g[u]: return
        self.g[u].pop(v)
        self.g[v].pop(u)

    def nodes(self):
        return self.g.keys()

    def neighbors(self, u):
        return self.g[u].keys()

    def weights(self, u, v):
        return self.g[u][v]


    ##
    # @desc    removes edge if all thresholds aren't reached
    # --
    # @param   g
    # @param   ful    threshold for full_image_query
    # @param   rel    threshold for related_text
    # @param   sub    threshold for subimage
    # @param   ocr    threshold for ocr
    # @return  min_g  minimized graph
    ##
    def reduceBySoftWeights(self, ful, rel, sub, ocr):
        for source in list(self.nodes()):
            for target in list(self.neighbors(source)):
                # Remove Weights If Not In Threshold
                weights = self.weights(source, target)
                if weights[MewsGraph.FULL_IMG] < ful and weights[MewsGraph.REL_TXT] < rel and weights[MewsGraph.SUB_IMG] < sub and weights[MewsGraph.OCR] < ocr:
                    self.removeEdge(source, target)

    ##
    # @desc    removes edge if ANY thresholds aren't reached
    # --
    # @param   g
    # @param   ful    threshold for full_image_query
    # @param   rel    threshold for related_text
    # @param   sub    threshold for subimage
    # @param   ocr    threshold for ocr
    # @return  min_g  minimized graph
    ##
    def reduceByHardWeights(self, ful, rel, sub, ocr):
        for source in list(self.nodes()):
            for target in list(self.neighbors(source)):
                # Remove Weights If Not In Threshold
                weights = self.weights(source, target)
                if weights[MewsGraph.FULL_IMG] < ful or weights[MewsGraph.REL_TXT] < rel or weights[MewsGraph.SUB_IMG] < sub or weights[MewsGraph.OCR] < ocr:
                    self.removeEdge(source, target)

    def dump_txt(self, fpath):

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
        for v in self.nodes():
            for n in self.neighbors(v):
                for method_i in range(MewsGraph.NUM_METHODS):
                    f.write(f'{v};{n};{methods[method_i]};{self.weights(v,n)[method_i]};;;;\n')

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

