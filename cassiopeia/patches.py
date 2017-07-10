import datetime

from typing import Optional as _Optional


class Patch(object):
    def __init__(self, name: str, patch: str, start: datetime.date, end: _Optional[datetime.date]):
        self._name = name
        self._patch = patch
        self._start = start
        self._end = end

    @classmethod
    def from_str(cls, string):
        for patch in cls.__patches:
            if string in patch.patch:
                return patch
        else:
            raise ValueError("Unknown patch name {}".format(string))

    @property
    def name(self):
        return self._name

    @property
    def patch(self):
        return self._patch

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def major(self):
        return self.patch.split(".")[0]

    @property
    def minor(self):
        return self.patch.split(".")[1]

    @property
    def majorminor(self):
        return ".".join(self.patch.split(".")[:2])

    @property
    def revision(self):
        return ".".join(self.patch.split(".")[2:])


patches = [
    Patch(name="Closed Beta", patch="0.9.22.4", start=datetime.date(2009, 7, 30), end=datetime.date(2009, 8, 7)),
    Patch(name="Closed Beta", patch="0.9.22.7", start=datetime.date(2009, 8, 7), end=datetime.date(2009, 8, 12)),
    Patch(name="Closed Beta", patch="0.9.22.9", start=datetime.date(2009, 8, 12), end=datetime.date(2009, 8, 19)),
    Patch(name="Closed Beta", patch="0.9.22.15", start=datetime.date(2009, 8, 19), end=datetime.date(2009, 9, 2)),
    Patch(name="Closed Beta", patch="0.9.22.16", start=datetime.date(2009, 9, 2), end=datetime.date(2009, 9, 10)),
    Patch(name="Closed Beta", patch="0.9.22.18", start=datetime.date(2009, 9, 10), end=datetime.date(2009, 9, 19)),
    Patch(name="Closed Beta", patch="0.9.25.21", start=datetime.date(2009, 9, 19), end=datetime.date(2009, 10, 1)),
    Patch(name="Closed Beta", patch="0.9.25.24", start=datetime.date(2009, 10, 1), end=datetime.date(2009, 10, 10)),
    Patch(name="Closed Beta", patch="0.9.25.34", start=datetime.date(2009, 10, 10), end=datetime.date(2009, 10, 21)),
    Patch(name="Season 1", patch="1.0.0.32", start=datetime.date(2009, 10, 21), end=datetime.date(2009, 11, 11)),
    Patch(name="Season 1", patch="1.0.0.52", start=datetime.date(2009, 11, 11), end=datetime.date(2009, 11, 20)),
    Patch(name="Season 1", patch="1.0.0.58", start=datetime.date(2009, 11, 20), end=datetime.date(2009, 12, 2)),
    Patch(name="Season 1", patch="1.0.0.61", start=datetime.date(2009, 12, 2), end=datetime.date(2009, 12, 17)),
    Patch(name="Season 1", patch="1.0.0.63", start=datetime.date(2009, 12, 17), end=datetime.date(2010, 1, 13)),
    Patch(name="Season 1", patch="1.0.0.70", start=datetime.date(2010, 1, 13), end=datetime.date(2010, 2, 2)),
    Patch(name="Season 1", patch="1.0.0.72", start=datetime.date(2010, 2, 2), end=datetime.date(2010, 2, 9)),
    Patch(name="Season 1", patch="1.0.0.74", start=datetime.date(2010, 2, 9), end=datetime.date(2010, 2, 24)),
    Patch(name="Season 1", patch="1.0.0.75", start=datetime.date(2010, 2, 24), end=datetime.date(2010, 3, 16)),
    Patch(name="Season 1", patch="1.0.0.79", start=datetime.date(2010, 3, 16), end=datetime.date(2010, 3, 24)),
    Patch(name="Season 1", patch="1.0.0.81", start=datetime.date(2010, 3, 24), end=datetime.date(2010, 4, 8)),
    Patch(name="Season 1", patch="1.0.0.82", start=datetime.date(2010, 4, 8), end=datetime.date(2010, 4, 27)),
    Patch(name="Season 1", patch="1.0.0.83", start=datetime.date(2010, 4, 27), end=datetime.date(2010, 5, 11)),
    Patch(name="Season 1", patch="1.0.0.85", start=datetime.date(2010, 5, 11), end=datetime.date(2010, 6, 1)),
    Patch(name="Season 1", patch="1.0.0.86", start=datetime.date(2010, 6, 1), end=datetime.date(2010, 6, 8)),
    Patch(name="Season 1", patch="1.0.0.87", start=datetime.date(2010, 6, 8), end=datetime.date(2010, 6, 24)),
    Patch(name="Season 1", patch="1.0.0.94", start=datetime.date(2010, 6, 24), end=datetime.date(2010, 6, 29)),
    Patch(name="Season 1", patch="1.0.0.94(b)", start=datetime.date(2010, 6, 29), end=datetime.date(2010, 7, 13)),
    Patch(name="Season 1", patch="1.0.0.96", start=datetime.date(2010, 7, 13), end=datetime.date(2010, 7, 27)),
    Patch(name="Season 1", patch="1.0.0.97", start=datetime.date(2010, 7, 27), end=datetime.date(2010, 8, 10)),
    Patch(name="Season 1", patch="1.0.0.98", start=datetime.date(2010, 8, 10), end=datetime.date(2010, 8, 24)),
    Patch(name="Season 1", patch="1.0.0.99", start=datetime.date(2010, 8, 24), end=datetime.date(2010, 9, 8)),
    Patch(name="Season 1", patch="1.0.0.100", start=datetime.date(2010, 9, 8), end=datetime.date(2010, 9, 21)),
    Patch(name="Season 1", patch="1.0.0.101", start=datetime.date(2010, 9, 21), end=datetime.date(2010, 10, 5)),
    Patch(name="Season 1", patch="1.0.0.102", start=datetime.date(2010, 10, 5), end=datetime.date(2010, 10, 19)),
    Patch(name="Season 1", patch="1.0.0.103", start=datetime.date(2010, 10, 19), end=datetime.date(2010, 11, 2)),
    Patch(name="Season 1", patch="1.0.0.104", start=datetime.date(2010, 11, 2), end=datetime.date(2010, 11, 16)),
    Patch(name="Season 1", patch="1.0.0.105", start=datetime.date(2010, 11, 16), end=datetime.date(2010, 12, 1)),
    Patch(name="Season 1", patch="1.0.0.106", start=datetime.date(2010, 12, 1), end=datetime.date(2010, 12, 14)),
    Patch(name="Season 1", patch="1.0.0.107", start=datetime.date(2010, 12, 14), end=datetime.date(2011, 1, 4)),
    Patch(name="Season 1", patch="1.0.0.108", start=datetime.date(2011, 1, 4), end=datetime.date(2011, 1, 18)),
    Patch(name="Season 1", patch="1.0.0.109", start=datetime.date(2011, 1, 18), end=datetime.date(2011, 2, 1)),
    Patch(name="Season 1", patch="1.0.0.110", start=datetime.date(2011, 2, 1), end=datetime.date(2011, 2, 16)),
    Patch(name="Season 1", patch="1.0.0.111", start=datetime.date(2011, 2, 16), end=datetime.date(2011, 3, 1)),
    Patch(name="Season 1", patch="1.0.0.112", start=datetime.date(2011, 3, 1), end=datetime.date(2011, 3, 15)),
    Patch(name="Season 1", patch="1.0.0.113", start=datetime.date(2011, 3, 15), end=datetime.date(2011, 3, 29)),
    Patch(name="Season 1", patch="1.0.0.114", start=datetime.date(2011, 3, 29), end=datetime.date(2011, 4, 12)),
    Patch(name="Season 1", patch="1.0.0.115", start=datetime.date(2011, 4, 12), end=datetime.date(2011, 4, 26)),
    Patch(name="Season 1", patch="1.0.0.116", start=datetime.date(2011, 4, 26), end=datetime.date(2011, 5, 10)),
    Patch(name="Season 1", patch="1.0.0.118", start=datetime.date(2011, 5, 10), end=datetime.date(2011, 5, 24)),
    Patch(name="Season 1", patch="1.0.0.118b", start=datetime.date(2011, 5, 24), end=datetime.date(2011, 6, 1)),
    Patch(name="Season 1", patch="1.0.0.119", start=datetime.date(2011, 6, 1), end=datetime.date(2011, 6, 22)),
    Patch(name="Season 1", patch="1.0.0.120", start=datetime.date(2011, 6, 22), end=datetime.date(2011, 7, 8)),
    Patch(name="Season 1", patch="1.0.0.121", start=datetime.date(2011, 7, 8), end=datetime.date(2011, 7, 26)),
    Patch(name="Season 1", patch="1.0.0.122", start=datetime.date(2011, 7, 26), end=datetime.date(2011, 8, 9)),
    Patch(name="Season 1", patch="1.0.0.123", start=datetime.date(2011, 8, 9), end=datetime.date(2011, 8, 24)),
    Patch(name="Season 1", patch="1.0.0.124", start=datetime.date(2011, 8, 24), end=datetime.date(2011, 9, 14)),
    Patch(name="Season 1", patch="1.0.0.125", start=datetime.date(2011, 9, 14), end=datetime.date(2011, 10, 5)),
    Patch(name="Season 2", patch="1.0.0.126", start=datetime.date(2011, 10, 5), end=datetime.date(2011, 10, 19)),
    Patch(name="Season 2", patch="1.0.0.127", start=datetime.date(2011, 10, 19), end=datetime.date(2011, 11, 1)),
    Patch(name="Season 2", patch="1.0.0.128", start=datetime.date(2011, 11, 1), end=datetime.date(2011, 11, 15)),
    Patch(name="Season 2", patch="1.0.0.129", start=datetime.date(2011, 11, 15), end=datetime.date(2011, 11, 29)),
    Patch(name="Season 2", patch="1.0.0.130", start=datetime.date(2011, 11, 29), end=datetime.date(2011, 12, 13)),
    Patch(name="Season 2", patch="1.0.0.131", start=datetime.date(2011, 12, 13), end=datetime.date(2012, 1, 17)),
    Patch(name="Season 2", patch="1.0.0.132", start=datetime.date(2012, 1, 17), end=datetime.date(2012, 2, 1)),
    Patch(name="Season 2", patch="1.0.0.133", start=datetime.date(2012, 2, 1), end=datetime.date(2012, 2, 14)),
    Patch(name="Season 2", patch="1.0.0.134", start=datetime.date(2012, 2, 14), end=datetime.date(2012, 2, 29)),
    Patch(name="Season 2", patch="1.0.0.135", start=datetime.date(2012, 2, 29), end=datetime.date(2012, 3, 20)),
    Patch(name="Season 2", patch="1.0.0.136", start=datetime.date(2012, 3, 20), end=datetime.date(2012, 4, 18)),
    Patch(name="Season 2", patch="1.0.0.138", start=datetime.date(2012, 4, 18), end=datetime.date(2012, 5, 1)),
    Patch(name="Season 2", patch="1.0.0.139", start=datetime.date(2012, 5, 1), end=datetime.date(2012, 5, 23)),
    Patch(name="Season 2", patch="1.0.0.140", start=datetime.date(2012, 5, 23), end=datetime.date(2012, 6, 5)),
    Patch(name="Season 2", patch="1.0.0.140b", start=datetime.date(2012, 6, 5), end=datetime.date(2012, 6, 17)),
    Patch(name="Season 2", patch="1.0.0.141", start=datetime.date(2012, 6, 17), end=datetime.date(2012, 7, 7)),
    Patch(name="Season 2", patch="1.0.0.142", start=datetime.date(2012, 7, 7), end=datetime.date(2012, 7, 19)),
    Patch(name="Season 2", patch="1.0.0.143", start=datetime.date(2012, 7, 19), end=datetime.date(2012, 8, 1)),
    Patch(name="Season 2", patch="1.0.0.144", start=datetime.date(2012, 8, 1), end=datetime.date(2012, 8, 14)),
    Patch(name="Season 2", patch="1.0.0.145", start=datetime.date(2012, 8, 14), end=datetime.date(2012, 8, 30)),
    Patch(name="Season 2", patch="1.0.0.146", start=datetime.date(2012, 8, 30), end=datetime.date(2012, 9, 12)),
    Patch(name="Season 2", patch="1.0.0.147", start=datetime.date(2012, 9, 12), end=datetime.date(2012, 9, 27)),
    Patch(name="Season 2", patch="1.0.0.148", start=datetime.date(2012, 9, 27), end=datetime.date(2012, 10, 17)),
    Patch(name="Season 2", patch="1.0.0.149", start=datetime.date(2012, 10, 17), end=datetime.date(2012, 10, 25)),
    Patch(name="Season 2", patch="1.0.0.150", start=datetime.date(2012, 10, 25), end=datetime.date(2012, 11, 13)),
    Patch(name="Season 2", patch="1.0.0.151", start=datetime.date(2012, 11, 13), end=datetime.date(2013, 2, 1)),
    Patch(name="Season 3", patch="3.01", start=datetime.date(2013, 2, 1), end=datetime.date(2013, 2, 13)),
    Patch(name="Season 3", patch="3.02", start=datetime.date(2013, 2, 13), end=datetime.date(2013, 3, 1)),
    Patch(name="Season 3", patch="3.03", start=datetime.date(2013, 3, 1), end=datetime.date(2013, 3, 19)),
    Patch(name="Season 3", patch="3.04", start=datetime.date(2013, 3, 19), end=datetime.date(2013, 3, 28)),
    Patch(name="Season 3", patch="3.5", start=datetime.date(2013, 3, 28), end=datetime.date(2013, 4, 30)),
    Patch(name="Season 3", patch="3.6", start=datetime.date(2013, 4, 30), end=datetime.date(2013, 5, 15)),
    Patch(name="Season 3", patch="3.7", start=datetime.date(2013, 5, 15), end=datetime.date(2013, 6, 13)),
    Patch(name="Season 3", patch="3.8", start=datetime.date(2013, 6, 13), end=datetime.date(2013, 7, 9)),
    Patch(name="Season 3", patch="3.9", start=datetime.date(2013, 7, 9), end=datetime.date(2013, 7, 30)),
    Patch(name="Season 3", patch="3.10", start=datetime.date(2013, 7, 30), end=datetime.date(2013, 8, 22)),
    Patch(name="Season 3", patch="3.10a", start=datetime.date(2013, 8, 22), end=datetime.date(2013, 9, 4)),
    Patch(name="Season 3", patch="3.11", start=datetime.date(2013, 9, 4), end=datetime.date(2013, 10, 1)),
    Patch(name="Season 3", patch="3.12", start=datetime.date(2013, 10, 1), end=datetime.date(2013, 10, 29)),
    Patch(name="Season 3", patch="3.13", start=datetime.date(2013, 10, 29), end=datetime.date(2014, 1, 15)),
    Patch(name="Season 4", patch="4.1", start=datetime.date(2014, 1, 15), end=datetime.date(2014, 2, 10)),
    Patch(name="Season 4", patch="4.2", start=datetime.date(2014, 2, 10), end=datetime.date(2014, 2, 27)),
    Patch(name="Season 4", patch="4.3", start=datetime.date(2014, 2, 27), end=datetime.date(2014, 3, 18)),
    Patch(name="Season 4", patch="4.4", start=datetime.date(2014, 3, 18), end=datetime.date(2014, 4, 3)),
    Patch(name="Season 4", patch="4.5", start=datetime.date(2014, 4, 3), end=datetime.date(2014, 4, 21)),
    Patch(name="Season 4", patch="4.6", start=datetime.date(2014, 4, 21), end=datetime.date(2014, 5, 8)),
    Patch(name="Season 4", patch="4.7", start=datetime.date(2014, 5, 8), end=datetime.date(2014, 5, 22)),
    Patch(name="Season 4", patch="4.8", start=datetime.date(2014, 5, 22), end=datetime.date(2014, 6, 4)),
    Patch(name="Season 4", patch="4.9", start=datetime.date(2014, 6, 4), end=datetime.date(2014, 6, 18)),
    Patch(name="Season 4", patch="4.10", start=datetime.date(2014, 6, 18), end=datetime.date(2014, 7, 2)),
    Patch(name="Season 4", patch="4.11", start=datetime.date(2014, 7, 2), end=datetime.date(2014, 7, 16)),
    Patch(name="Season 4", patch="4.12", start=datetime.date(2014, 7, 16), end=datetime.date(2014, 7, 30)),
    Patch(name="Season 4", patch="4.13", start=datetime.date(2014, 7, 30), end=datetime.date(2014, 8, 13)),
    Patch(name="Season 4", patch="4.14", start=datetime.date(2014, 8, 13), end=datetime.date(2014, 8, 27)),
    Patch(name="Season 4", patch="4.15", start=datetime.date(2014, 8, 27), end=datetime.date(2014, 9, 10)),
    Patch(name="Season 4", patch="4.16", start=datetime.date(2014, 9, 10), end=datetime.date(2014, 9, 25)),
    Patch(name="Season 4", patch="4.17", start=datetime.date(2014, 9, 25), end=datetime.date(2014, 10, 9)),
    Patch(name="Season 4", patch="4.18", start=datetime.date(2014, 10, 9), end=datetime.date(2014, 11, 5)),
    Patch(name="Season 4", patch="4.19", start=datetime.date(2014, 11, 5), end=datetime.date(2015, 1, 15)),
    Patch(name="Season 5", patch="5.1", start=datetime.date(2015, 1, 15), end=datetime.date(2015, 1, 28)),
    Patch(name="Season 5", patch="5.2", start=datetime.date(2015, 1, 28), end=datetime.date(2015, 2, 11)),
    Patch(name="Season 5", patch="5.3", start=datetime.date(2015, 2, 11), end=datetime.date(2015, 2, 25)),
    Patch(name="Season 5", patch="5.4", start=datetime.date(2015, 2, 25), end=datetime.date(2015, 3, 12)),
    Patch(name="Season 5", patch="5.5", start=datetime.date(2015, 3, 12), end=datetime.date(2015, 3, 25)),
    Patch(name="Season 5", patch="5.6", start=datetime.date(2015, 3, 25), end=datetime.date(2015, 4, 8)),
    Patch(name="Season 5", patch="5.7", start=datetime.date(2015, 4, 8), end=datetime.date(2015, 4, 28)),
    Patch(name="Season 5", patch="5.8", start=datetime.date(2015, 4, 28), end=datetime.date(2015, 5, 14)),
    Patch(name="Season 5", patch="5.9", start=datetime.date(2015, 5, 14), end=datetime.date(2015, 5, 28)),
    Patch(name="Season 5", patch="5.10", start=datetime.date(2015, 5, 28), end=datetime.date(2015, 6, 10)),
    Patch(name="Season 5", patch="5.11", start=datetime.date(2015, 6, 10), end=datetime.date(2015, 6, 24)),
    Patch(name="Season 5", patch="5.12", start=datetime.date(2015, 6, 24), end=datetime.date(2015, 7, 8)),
    Patch(name="Season 5", patch="5.13", start=datetime.date(2015, 7, 8), end=datetime.date(2015, 7, 22)),
    Patch(name="Season 5", patch="5.14", start=datetime.date(2015, 7, 22), end=datetime.date(2015, 8, 5)),
    Patch(name="Season 5", patch="5.15", start=datetime.date(2015, 8, 5), end=datetime.date(2015, 8, 20)),
    Patch(name="Season 5", patch="5.16", start=datetime.date(2015, 8, 20), end=datetime.date(2015, 9, 2)),
    Patch(name="Season 5", patch="5.17", start=datetime.date(2015, 9, 2), end=datetime.date(2015, 9, 16)),
    Patch(name="Season 5", patch="5.18", start=datetime.date(2015, 9, 16), end=datetime.date(2015, 9, 30)),
    Patch(name="Season 5", patch="5.19", start=datetime.date(2015, 9, 30), end=datetime.date(2015, 10, 14)),
    Patch(name="Season 5", patch="5.20", start=datetime.date(2015, 10, 14), end=datetime.date(2015, 10, 29)),
    Patch(name="Season 5", patch="5.21", start=datetime.date(2015, 10, 29), end=datetime.date(2016, 1, 14)),
    Patch(name="Season 6", patch="6.1", start=datetime.date(2016, 1, 14), end=datetime.date(2016, 1, 28)),
    Patch(name="Season 6", patch="6.2", start=datetime.date(2016, 1, 28), end=datetime.date(2016, 2, 10)),
    Patch(name="Season 6", patch="6.3", start=datetime.date(2016, 2, 10), end=datetime.date(2016, 2, 24)),
    Patch(name="Season 6", patch="6.4", start=datetime.date(2016, 2, 24), end=datetime.date(2016, 3, 9)),
    Patch(name="Season 6", patch="6.5", start=datetime.date(2016, 3, 9), end=datetime.date(2016, 3, 23)),
    Patch(name="Season 6", patch="6.6", start=datetime.date(2016, 3, 23), end=datetime.date(2016, 4, 6)),
    Patch(name="Season 6", patch="6.7", start=datetime.date(2016, 4, 6), end=datetime.date(2016, 4, 20)),
    Patch(name="Season 6", patch="6.8", start=datetime.date(2016, 4, 20), end=datetime.date(2016, 5, 4)),
    Patch(name="Season 6", patch="6.9", start=datetime.date(2016, 5, 4), end=datetime.date(2016, 5, 18)),
    Patch(name="Season 6", patch="6.10", start=datetime.date(2016, 5, 18), end=datetime.date(2016, 6, 1)),
    Patch(name="Season 6", patch="6.11", start=datetime.date(2016, 6, 1), end=datetime.date(2016, 6, 15)),
    Patch(name="Season 6", patch="6.12", start=datetime.date(2016, 6, 15), end=datetime.date(2016, 6, 29)),
    Patch(name="Season 6", patch="6.13", start=datetime.date(2016, 6, 29), end=datetime.date(2016, 7, 13)),
    Patch(name="Season 6", patch="6.14", start=datetime.date(2016, 7, 13), end=datetime.date(2016, 7, 26)),
    Patch(name="Season 6", patch="6.15", start=datetime.date(2016, 7, 26), end=datetime.date(2016, 8, 10)),
    Patch(name="Season 6", patch="6.16", start=datetime.date(2016, 8, 10), end=datetime.date(2016, 8, 24)),
    Patch(name="Season 6", patch="6.17", start=datetime.date(2016, 8, 24), end=datetime.date(2016, 9, 8)),
    Patch(name="Season 6", patch="6.18", start=datetime.date(2016, 9, 8), end=datetime.date(2016, 9, 21)),
    Patch(name="Season 6", patch="6.19", start=datetime.date(2016, 9, 21), end=datetime.date(2016, 10, 5)),
    Patch(name="Season 6", patch="6.20", start=datetime.date(2016, 10, 5), end=datetime.date(2016, 10, 19)),
    Patch(name="Season 6", patch="6.21", start=datetime.date(2016, 10, 19), end=datetime.date(2016, 11, 10)),
    Patch(name="Season 6", patch="6.22", start=datetime.date(2016, 11, 10), end=datetime.date(2016, 11, 22)),
    Patch(name="Season 6", patch="6.23", start=datetime.date(2016, 11, 22), end=datetime.date(2016, 12, 7)),
    Patch(name="Season 6", patch="6.24", start=datetime.date(2016, 12, 7), end=datetime.date(2017, 1, 11)),
    Patch(name="Season 7", patch="7.1", start=datetime.date(2017, 1, 11), end=datetime.date(2017, 1, 25)),
    Patch(name="Season 7", patch="7.2", start=datetime.date(2017, 1, 25), end=datetime.date(2017, 2, 8)),
    Patch(name="Season 7", patch="7.3", start=datetime.date(2017, 2, 8), end=datetime.date(2017, 2, 23)),
    Patch(name="Season 7", patch="7.4", start=datetime.date(2017, 2, 23), end=datetime.date(2017, 3, 8)),
    Patch(name="Season 7", patch="7.5", start=datetime.date(2017, 3, 8), end=datetime.date(2017, 3, 22)),
    Patch(name="Season 7", patch="7.6", start=datetime.date(2017, 3, 22), end=datetime.date(2017, 4, 5)),
    Patch(name="Season 7", patch="7.7", start=datetime.date(2017, 4, 5), end=datetime.date(2017, 4, 19)),
    Patch(name="Season 7", patch="7.8", start=datetime.date(2017, 4, 19), end=datetime.date(2017, 5, 3)),
    Patch(name="Season 7", patch="7.9", start=datetime.date(2017, 5, 3), end=datetime.date(2017, 5, 17)),
    Patch(name="Season 7", patch="7.10", start=datetime.date(2017, 5, 17), end=datetime.date(2017, 6, 1)),
    Patch(name="Season 7", patch="7.11", start=datetime.date(2017, 6, 1), end=datetime.date(2017, 6, 14)),
    Patch(name="Season 7", patch="7.12", start=datetime.date(2017, 6, 14), end=datetime.date(2017, 6, 28)),
    Patch(name="Season 7", patch="7.13", start=datetime.date(2017, 6, 28), end=datetime.date(2017, 7, 12)),
    Patch(name="Season 7", patch="7.14", start=datetime.date(2017, 7, 12), end=None)
]

Patch._Patch__patches = patches
