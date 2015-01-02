python-fire
===========

(Not to be confused with `pyfire` which is
[completely different](https://github.com/mariano/pyfire) and is actual useful
software)

Fuzzy Intrusion Detection Engine written in Python. For a Masters assignment;
ingests datasets similar to NSL-KDD dataset.

This is a reimplementation of the
["Fuzzy Intrusion Recognition Engine"(FIRE)](http://home.engineering.iastate.edu/~julied/research/FIRE/)
originally designed by Dickerson et. al.

Due to time constraints this is an offline system which must be trained first
and then tested with static data files. It supports the
[NSL-KDD](http://nsl.cs.unb.ca/NSL-KDD/) dataset and/or any datasets that are in
the same format. NSL-KDD is a modified version of the original
[KDD-Cup '99](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html) data that
is popular within Network Intrusion Detection research. NSL-KDD claims to
improve the false-positive rate across all machine learning algorithms tested,
compared to the original KDD-Cup data. This code accepts the NSL-KDD data in
its' [ARFF](http://weka.wikispaces.com/ARFF) version, which is more expressive
than Comma-Separated Values (CSV).


