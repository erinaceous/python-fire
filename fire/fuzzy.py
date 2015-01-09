# vim: set tabstop=4 shiftwidth=4 textwidth=79 cc=72,79:
"""
    fuzzy: Fuzzy Set and Fuzzy Logic functions.
    Original Author: Owain Jones [github.com/erinaceous] [contact@odj.me]
"""

from __future__ import print_function
import fuzzython.utils
import fuzzython.norms.norms
import fuzzython.fsets.fuzzy_set
import fuzzython.fsets.gaussian
import fuzzython.fsets.polygon
import operator
import numpy
import copy
import math


# Uniformly distributed sets across a line
# 'SET NAME': (centroid, extent)
SETS = {
    'low': (0.1, 0.1),
    'medium-low': (0.3, 0.1),
    'medium': (0.5, 0.1),
    'medium-high': (0.7, 0.1),
    'high': (0.9, 0.1)
}


def scale(value, minimum, maximum):
    return (1.0 / (maximum - minimum) * (value))


class Attribute:
    def memberships(self, value):
        value = self.normalize(value)
        memberships = dict()
        for set_name, function in self.sets.items():
            memberships[set_name] = function(value)
        return memberships

    def classify(self, value):
        memberships = self.memberships(value)
        return max(memberships.items(), key=operator.itemgetter(1))[0]

    def __repr__(self):
        return str(self.sets)


class NumericAttribute(Attribute):
    def __init__(self, data):
        try:
            self.minimum = data.min()
            self.maximum = data.max()
        except AttributeError:
            self.minimum = min(data)
            self.maximum = max(data)
        self.sets = {
            key: fuzzython.fsets.gaussian.Gaussian(value[0], value[1])
            for key, value in SETS.items()
        }

    def normalize(self, value):
        value = scale(value, self.minimum, self.maximum)
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        return value


class NominalAttribute(Attribute):
    def __init__(self, data, attribute):
        set_step = 1.0 / len(attribute[1])
        set_min = set_step / 2.0
        steps = numpy.arange(set_min, 1.0, set_step)
        self.centroids = {
            set_name: steps[i]
            for i, set_name in enumerate(attribute[1])
        }
        self.sets = {
            set_name: fuzzython.fsets.polygon.Polygon(
                (steps[i] - (set_min + 0.000001), 0.0),
                (steps[i] - set_min, 1.0),
                (steps[i], 1.0),
                (steps[i] + set_min, 1.0),
                (steps[i] + (set_min + 0.000001), 0.0)
            )
            for i, set_name in enumerate(attribute[1])
        }

    def normalize(self, value):
        return self.centroids[value.decode()]


class BinaryAttribute(NominalAttribute):
    def __init__(self, data, attribute):
        NominalAttribute.__init__(self, data, attribute)
        centroids = self.centroids
        sets = self.sets
        self.centroids = {}
        self.sets = {}
        for key in centroids.keys():
            if key in [0, '0', 'false', 'False', 'FALSE', False]:
                self.centroids['false'] = centroids[key]
                self.sets['false'] = sets[key]
            elif key in [1, '1', 'true', 'True', 'TRUE', True]:
                self.centroids['true'] = centroids[key]
                self.sets['true'] = sets[key]

    def normalize(self, value):
        try:
            value = value.decode()
        except AttributeError:
            pass
        if value in [0, '0', 'false', 'False', 'FALSE', False]:
            return self.centroids['false']
        elif value in [1, '1', 'true', 'True', 'TRUE', True]:
            return self.centroids['true']


def build_attributes(data, attributes, ignore=['class']):
    tree = {}
    for name in data.dtype.names:
        if name in ignore:
            continue
        if attributes[name][0] == 'nominal':
            if attributes[name][1] in [(0, 1), ('0', '1'), ('true', 'false'),
                                    ('True', 'False'), ('TRUE', 'FALSE'),
                                    (True, False)]:
                tree[name] = BinaryAttribute(data[name], attributes[name])
            else:
                tree[name] = NominalAttribute(data[name], attributes[name])
        elif attributes[name][0] == 'numeric':
            tree[name] = NumericAttribute(data[name])
    return tree


def classify_example(example, attributes, attribute_tree, ignore=['class']):
    output = {}
    for name in attributes:
        if name in ignore:
            continue
        output[name] = attribute_tree[name].classify(example[name])
    return output


def cmeans(data, attributes, tree, maxiter=10, ignore=['class']):
    for attribute in attributes:
        if attribute in ignore:
            continue
        if attributes[attribute][0] != 'numeric':
            continue
        tree[attribute] = cmeans_attrib(data[attribute],
                                        tree[attribute], maxiter)
        print(tree[attribute].sets)
    return tree


def centers(data, attribute, fuzziness=2.0):
    memberships = attribute.sets
    cluster_centers = {}
    t = {}

    # Get current membership values for each set
    for key, value in memberships.items():
        t[key] = []
        for point in data:
            t[key].append(math.pow(value(attribute.normalize(point)),
                                   fuzziness))

    # Now do the magic that finds the cluster center....
    for key, value in t.items():
        numerator = 0.0
        denominator = 0.0
        for i in range(0, len(data)):
            numerator += t[key][i] * attribute.normalize(data[i])
            denominator += t[key][i]
        cluster_centers[key] =\
            fuzzython.fsets.gaussian.Gaussian(numerator / denominator, 0.1)
    attribute.sets = cluster_centers
    return attribute


def cmeans_attrib(data, attribute, maxiter):
    attribute = centers(data, attribute)
    for x in range(0, maxiter):
        attribute = centers(data, attribute)
    return attribute
