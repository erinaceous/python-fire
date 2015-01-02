#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 textwidth=79 cc=72,79:
"""
    All functionality needed to read in NSL-KDD-compatible ARFF
    datasets.

    Original Author: Owain Jones [github.com/erinaceous] [odj@aber.ac.uk]
"""

from __future__ import print_function
from scipy.io.arff import loadarff


class Reader:
    """Wrapper class. Uses scipy.io.arff to parse ARFF files. Might
       extend to handle the KDD-Cup CSV files also.

       To load and get data:
       reader.load(file.arff); data = reader.data
    """

    @staticmethod
    def _get_file_object(arffile=None):
        """Convert a file path into a file object"""
        if type(arffile) == str:
            return open(arffile, 'r')
        elif arffile is not None:
            return arffile
        return None

    def __init__(self, arffile=None):
        self.inputstream = Reader._get_file_object(arffile)
        self.attributes = None
        self.data = None

    def load(self, arffile=None):
        """Loads the file specified by arffile (or the file given in
           Reader(file) constructor).
           Returns True if it was read successfully.
           After reading, data can be accessed through
           instance.data.
           instance.attributes also contains the information about the
           ARFF attributes.
        """
        inputstream = Reader._get_file_object(arffile)
        if inputstream is None:
            inputstream = self.inputstream
        if inputstream is None:
            return False

        arff_data = loadarff(inputstream)
        self.data = arff_data[0]
        self.attributes = arff_data[1]
        return True
