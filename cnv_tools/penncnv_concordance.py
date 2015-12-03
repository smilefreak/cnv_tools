#!/usr/bin/env python
#
#
# @date 4 Dec 2015
# @author James Boocock

import argparse

class CNVList(object):
    """
        Represents a list of CNVs from PENNCNV
    """
    
    def __init__(self, penncnv_file):
        """
            Open PENNCNV file
            and load into object.
        """



class TechnicalRep(object):
    """
        Represenets an individual Technical Replicate
    """
    def __init__(self, sample_id):
        self.sample_id = sample_id 

    
    def get_cnvs(self, cnv_list):


def main():
    parser = argparse.ArgumentParser(description="Parses CNV output from PENNCNV and determines CNV concordance")
    parser.add_argument("-s","--sample-file", dest="sample_file", help="File containing technical replicates one set per line") 
    parser.add_argument("-p","--penn-cnv", dest="penn_cnv_input", help="PennCNV CNV file")
    args = parser.parse_args()
    concordant_list

if __name__ == "__main__":
    main()
