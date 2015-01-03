# vim: set tabstop=4 shiftwidth=4 textwidth=79 cc=72,79:
"""
    All functionality needed to read in NSL-KDD-compatible ARFF
    datasets.

    Original Author: Owain Jones [github.com/erinaceous] [odj@aber.ac.uk]
"""

from __future__ import print_function
from scipy.io.arff import loadarff
import json


def _get_file_object(inputfile=None):
    """Convert a file path into a file object"""
    if type(inputfile) == str:
        return open(inputfile, 'r')
    return inputfile


class ARFFReader:
    """Wrapper class. Uses scipy.io.arff to parse ARFF files. Might
       extend to handle the KDD-Cup CSV files also.

       To load and get data:
       reader.load(file.arff); data = reader.data
    """

    def __init__(self, arffile=None):
        self.inputstream = _get_file_object(arffile)
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
        inputstream = _get_file_object(arffile)
        if inputstream is None:
            inputstream = self.inputstream
        if inputstream is None:
            return False

        arff_data = loadarff(inputstream)
        self.data = arff_data[0]
        self.attributes = arff_data[1]
        return True


class JSONReader:
    """Wrapper class for JSON config files."""

    def __init__(self, jsonfile=None):
        self.inputstream = _get_file_object(jsonfile)
        self.data = None

    def load(self, jsonfile=None):
        """Load config from a .json file. Returns True if loading was
           successful."""
        inputstream = _get_file_object(jsonfile)
        if inputstream is None:
            inputstream = self.inputstream
        if inputstream is None:
            return False

        json_data = json.load(inputstream)
        self.data = json_data
        return True

    def save(self):
        """Saves config to the .json file this JSONReader instance was
           initialized with. Returns True if saving was successful.
           Overwrites old file.
        """
        if self.data is None or self.inputstream is None:
            return False
        json.dump(self.data, self.inputstream)
        return True

