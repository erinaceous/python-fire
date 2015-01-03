# vim: set tabstop=4 shiftwidth=4 textwidth=79 cc=72,79:
"""
    fuzzy: Fuzzy Set and Fuzzy Logic functions.
    Original Author: Owain Jones [github.com/erinaceous] [contact@odj.me]
"""

from __future__ import print_function
import fuzzython.fsets.gaussian
import random
import numpy


# Uniformly distributed sets across a line
# 'SET NAME': (centroid, extent)
SETS = {
    'LOW': (0.1, 0.2),
    'MEDIUM-LOW': (0.3, 0.2),
    'MEDIUM': (0.5, 0.2),
    'MEDIUM-HIGH': (0.7, 0.2),
    'HIGH': (0.9, 0.2)
}


# Membership functions!
# Just use Gaussian for now.
MF = {
    'gaussian': lambda x: fuzzython.fsets.gaussian.Gaussian(*x)
}


def cmeans(data, attributes, sets=SETS, exponent=1.0, tolerance=0.2,
           maxiter=1000, ignore=['class'], mf=MF['gaussian']):
    """Uses the fuzzy C-means algorithm to calculate membership function
       centroids and exponents for all of the attributes/variables given.

       Arguments:
       data:        Entire dataset to train on
       sets:        Fuzzy sets to generate membership functions for
       exponent:    Exponent of FCM algorithm
       tolerance:   Termination criteria for FCM.
       maxiter:     Maximum number of iterations.
       ignore:      List of attributes to ignore.

       Returns the following data structure:
        {
            "attribute1": [
                instance1 -> {
                    "LOW": (centroid, extents),
                    ...
                    "HIGH": (centroid, extents)
                },
                ...
                instance999 -> {
                    "LOW": (centroid, extents),
                    ...
                }
                average -> {
                    "LOW": (centroid, extents),
                    ...
                }
            ],
            ...
            "attribute50": ...
        }
       Where the "average" key for each attribute is the mean
       centroid/extent value for all of that attribute's instances.
    """
    results = {}
    for name in data.dtype.names:
        if name in ignore:
            continue
        if attributes[name][0] == 'nominal':
            continue
            # if attributes[name][1] in [('0', '1'), (0, 1), ('true', 'false'),
            #                             ('TRUE', 'FALSE'), ('True', 'False'),
            #                             (True, False)]:
            #     result[name] = binary_attrib(data[name])
            # else:
            #     result[name] = nominal_attrib(data[name], attributes)
        else:
            results[name] = cmeans_attrib(data[name], sets, exponent,
                                          tolerance, maxiter)
    return results


def binary_attrib(attribute):
    pass


def nominal_attrib(attribute, attributes):
    pass


def cmeans_attrib(attribute, sets, exponent, tolerance, maxiter):
    """Calculate the centroid/extent for each attribute."""

    # 1. Initialize U=[u_ik] matrix, U^(0)
    k = 0
    U = [attribute]

    while k < maxiter:

        # At k-step: calculate the centers vectors C^(k)=[c_j] with U^(k)
        U[k] = 1.0 / (U[k])

        if (U[k - 1] - U[k]) < tolerance:
            return
        k += 1
