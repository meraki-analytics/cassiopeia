from collections import namedtuple
import datetime


class Patch(object):
    def __init__(self, name: str, patch: str, start: datetime.date, end: datetime.date):
        self._name = name
        self._patch = patch
        self._start = start
        self._end = end

    @classmethod
    def from_str(cls, string):
        for patch in cls.__patches:
            if string in patch.name:
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
    Patch(name="Closed Beta", patch="0.9.22.4", start=datetime.datetime.strptime("2009-07-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-08-07", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.22.7", start=datetime.datetime.strptime("2009-08-07", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-08-12", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.22.9", start=datetime.datetime.strptime("2009-08-12", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-08-19", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.22.15", start=datetime.datetime.strptime("2009-08-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-09-02", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.22.16", start=datetime.datetime.strptime("2009-09-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-09-10", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.22.18", start=datetime.datetime.strptime("2009-09-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-09-19", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.25.21", start=datetime.datetime.strptime("2009-09-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-10-01", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.25.24", start=datetime.datetime.strptime("2009-10-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-10-10", "%Y-%m-%d")),
    Patch(name="Closed Beta", patch="0.9.25.34", start=datetime.datetime.strptime("2009-10-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-10-21", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.32", start=datetime.datetime.strptime("2009-10-21", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-11-11", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.52", start=datetime.datetime.strptime("2009-11-11", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-11-20", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.58", start=datetime.datetime.strptime("2009-11-20", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-12-02", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.61", start=datetime.datetime.strptime("2009-12-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2009-12-17", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.63", start=datetime.datetime.strptime("2009-12-17", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-01-13", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.70", start=datetime.datetime.strptime("2010-01-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-02-02", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.72", start=datetime.datetime.strptime("2010-02-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-02-09", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.74", start=datetime.datetime.strptime("2010-02-09", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-02-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.75", start=datetime.datetime.strptime("2010-02-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-03-16", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.79", start=datetime.datetime.strptime("2010-03-16", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-03-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.81", start=datetime.datetime.strptime("2010-03-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-04-08", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.82", start=datetime.datetime.strptime("2010-04-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-04-27", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.83", start=datetime.datetime.strptime("2010-04-27", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-05-11", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.85", start=datetime.datetime.strptime("2010-05-11", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-06-01", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.86", start=datetime.datetime.strptime("2010-06-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-06-08", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.87", start=datetime.datetime.strptime("2010-06-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-06-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.94", start=datetime.datetime.strptime("2010-06-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-06-29", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.94(b)", start=datetime.datetime.strptime("2010-06-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-07-13", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.96", start=datetime.datetime.strptime("2010-07-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-07-27", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.97", start=datetime.datetime.strptime("2010-07-27", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-08-10", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.98", start=datetime.datetime.strptime("2010-08-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-08-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.99", start=datetime.datetime.strptime("2010-08-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-09-08", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.100", start=datetime.datetime.strptime("2010-09-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-09-21", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.101", start=datetime.datetime.strptime("2010-09-21", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-10-05", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.102", start=datetime.datetime.strptime("2010-10-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-10-19", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.103", start=datetime.datetime.strptime("2010-10-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-11-02", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.104", start=datetime.datetime.strptime("2010-11-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-11-16", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.105", start=datetime.datetime.strptime("2010-11-16", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-12-01", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.106", start=datetime.datetime.strptime("2010-12-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2010-12-14", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.107", start=datetime.datetime.strptime("2010-12-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-01-04", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.108", start=datetime.datetime.strptime("2011-01-04", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-01-18", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.109", start=datetime.datetime.strptime("2011-01-18", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-02-01", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.110", start=datetime.datetime.strptime("2011-02-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-02-16", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.111", start=datetime.datetime.strptime("2011-02-16", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-03-01", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.112", start=datetime.datetime.strptime("2011-03-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-03-15", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.113", start=datetime.datetime.strptime("2011-03-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-03-29", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.114", start=datetime.datetime.strptime("2011-03-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-04-12", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.115", start=datetime.datetime.strptime("2011-04-12", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-04-26", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.116", start=datetime.datetime.strptime("2011-04-26", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-05-10", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.118", start=datetime.datetime.strptime("2011-05-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-05-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.118b", start=datetime.datetime.strptime("2011-05-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-06-01", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.119", start=datetime.datetime.strptime("2011-06-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-06-22", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.120", start=datetime.datetime.strptime("2011-06-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-07-08", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.121", start=datetime.datetime.strptime("2011-07-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-07-26", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.122", start=datetime.datetime.strptime("2011-07-26", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-08-09", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.123", start=datetime.datetime.strptime("2011-08-09", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-08-24", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.124", start=datetime.datetime.strptime("2011-08-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-09-14", "%Y-%m-%d")),
    Patch(name="Season 1", patch="1.0.0.125", start=datetime.datetime.strptime("2011-09-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-10-05", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.126", start=datetime.datetime.strptime("2011-10-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-10-19", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.127", start=datetime.datetime.strptime("2011-10-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-11-01", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.128", start=datetime.datetime.strptime("2011-11-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-11-15", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.129", start=datetime.datetime.strptime("2011-11-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-11-29", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.130", start=datetime.datetime.strptime("2011-11-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2011-12-13", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.131", start=datetime.datetime.strptime("2011-12-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-01-17", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.132", start=datetime.datetime.strptime("2012-01-17", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-02-01", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.133", start=datetime.datetime.strptime("2012-02-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-02-14", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.134", start=datetime.datetime.strptime("2012-02-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-02-29", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.135", start=datetime.datetime.strptime("2012-02-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-03-20", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.136", start=datetime.datetime.strptime("2012-03-20", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-04-18", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.138", start=datetime.datetime.strptime("2012-04-18", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-05-01", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.139", start=datetime.datetime.strptime("2012-05-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-05-23", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.140", start=datetime.datetime.strptime("2012-05-23", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-06-05", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.140b", start=datetime.datetime.strptime("2012-06-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-06-17", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.141", start=datetime.datetime.strptime("2012-06-17", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-07-07", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.142", start=datetime.datetime.strptime("2012-07-07", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-07-19", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.143", start=datetime.datetime.strptime("2012-07-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-08-01", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.144", start=datetime.datetime.strptime("2012-08-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-08-14", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.145", start=datetime.datetime.strptime("2012-08-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-08-30", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.146", start=datetime.datetime.strptime("2012-08-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-09-12", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.147", start=datetime.datetime.strptime("2012-09-12", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-09-27", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.148", start=datetime.datetime.strptime("2012-09-27", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-10-17", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.149", start=datetime.datetime.strptime("2012-10-17", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-10-25", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.150", start=datetime.datetime.strptime("2012-10-25", "%Y-%m-%d"), end=datetime.datetime.strptime("2012-11-13", "%Y-%m-%d")),
    Patch(name="Season 2", patch="1.0.0.151", start=datetime.datetime.strptime("2012-11-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-02-01", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.01", start=datetime.datetime.strptime("2013-02-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-02-13", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.02", start=datetime.datetime.strptime("2013-02-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-03-01", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.03", start=datetime.datetime.strptime("2013-03-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-03-19", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.04", start=datetime.datetime.strptime("2013-03-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-03-28", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.5", start=datetime.datetime.strptime("2013-03-28", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-04-30", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.6", start=datetime.datetime.strptime("2013-04-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-05-15", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.7", start=datetime.datetime.strptime("2013-05-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-06-13", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.8", start=datetime.datetime.strptime("2013-06-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-07-09", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.9", start=datetime.datetime.strptime("2013-07-09", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-07-30", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.10", start=datetime.datetime.strptime("2013-07-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-08-22", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.10a", start=datetime.datetime.strptime("2013-08-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-09-04", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.11", start=datetime.datetime.strptime("2013-09-04", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-10-01", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.12", start=datetime.datetime.strptime("2013-10-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2013-10-29", "%Y-%m-%d")),
    Patch(name="Season 3", patch="3.13", start=datetime.datetime.strptime("2013-10-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-01-15", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.1", start=datetime.datetime.strptime("2014-01-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-02-10", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.2", start=datetime.datetime.strptime("2014-02-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-02-27", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.3", start=datetime.datetime.strptime("2014-02-27", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-03-18", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.4", start=datetime.datetime.strptime("2014-03-18", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-04-03", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.5", start=datetime.datetime.strptime("2014-04-03", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-04-21", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.6", start=datetime.datetime.strptime("2014-04-21", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-05-08", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.7", start=datetime.datetime.strptime("2014-05-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-05-22", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.8", start=datetime.datetime.strptime("2014-05-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-06-04", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.9", start=datetime.datetime.strptime("2014-06-04", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-06-18", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.10", start=datetime.datetime.strptime("2014-06-18", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-07-02", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.11", start=datetime.datetime.strptime("2014-07-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-07-16", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.12", start=datetime.datetime.strptime("2014-07-16", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-07-30", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.13", start=datetime.datetime.strptime("2014-07-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-08-13", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.14", start=datetime.datetime.strptime("2014-08-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-08-27", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.15", start=datetime.datetime.strptime("2014-08-27", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-09-10", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.16", start=datetime.datetime.strptime("2014-09-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-09-25", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.17", start=datetime.datetime.strptime("2014-09-25", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-10-09", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.18", start=datetime.datetime.strptime("2014-10-09", "%Y-%m-%d"), end=datetime.datetime.strptime("2014-11-05", "%Y-%m-%d")),
    Patch(name="Season 4", patch="4.19", start=datetime.datetime.strptime("2014-11-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-01-15", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.1", start=datetime.datetime.strptime("2015-01-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-01-28", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.2", start=datetime.datetime.strptime("2015-01-28", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-02-11", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.3", start=datetime.datetime.strptime("2015-02-11", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-02-25", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.4", start=datetime.datetime.strptime("2015-02-25", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-03-12", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.5", start=datetime.datetime.strptime("2015-03-12", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-03-25", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.6", start=datetime.datetime.strptime("2015-03-25", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-04-08", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.7", start=datetime.datetime.strptime("2015-04-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-04-28", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.8", start=datetime.datetime.strptime("2015-04-28", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-05-14", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.9", start=datetime.datetime.strptime("2015-05-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-05-28", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.10", start=datetime.datetime.strptime("2015-05-28", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-06-10", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.11", start=datetime.datetime.strptime("2015-06-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-06-24", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.12", start=datetime.datetime.strptime("2015-06-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-07-08", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.13", start=datetime.datetime.strptime("2015-07-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-07-22", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.14", start=datetime.datetime.strptime("2015-07-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-08-05", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.15", start=datetime.datetime.strptime("2015-08-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-08-20", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.16", start=datetime.datetime.strptime("2015-08-20", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-09-02", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.17", start=datetime.datetime.strptime("2015-09-02", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-09-16", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.18", start=datetime.datetime.strptime("2015-09-16", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-09-30", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.19", start=datetime.datetime.strptime("2015-09-30", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-10-14", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.20", start=datetime.datetime.strptime("2015-10-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2015-10-29", "%Y-%m-%d")),
    Patch(name="Season 5", patch="5.21", start=datetime.datetime.strptime("2015-10-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-01-14", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.1", start=datetime.datetime.strptime("2016-01-14", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-01-28", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.2", start=datetime.datetime.strptime("2016-01-28", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-02-10", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.3", start=datetime.datetime.strptime("2016-02-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-02-24", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.4", start=datetime.datetime.strptime("2016-02-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-03-09", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.5", start=datetime.datetime.strptime("2016-03-09", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-03-23", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.6", start=datetime.datetime.strptime("2016-03-23", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-04-06", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.7", start=datetime.datetime.strptime("2016-04-06", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-04-20", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.8", start=datetime.datetime.strptime("2016-04-20", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-05-04", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.9", start=datetime.datetime.strptime("2016-05-04", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-05-18", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.10", start=datetime.datetime.strptime("2016-05-18", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-06-01", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.11", start=datetime.datetime.strptime("2016-06-01", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-06-15", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.12", start=datetime.datetime.strptime("2016-06-15", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-06-29", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.13", start=datetime.datetime.strptime("2016-06-29", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-07-13", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.14", start=datetime.datetime.strptime("2016-07-13", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-07-26", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.15", start=datetime.datetime.strptime("2016-07-26", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-08-10", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.16", start=datetime.datetime.strptime("2016-08-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-08-24", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.17", start=datetime.datetime.strptime("2016-08-24", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-09-08", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.18", start=datetime.datetime.strptime("2016-09-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-09-21", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.19", start=datetime.datetime.strptime("2016-09-21", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-10-05", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.20", start=datetime.datetime.strptime("2016-10-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-10-19", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.21", start=datetime.datetime.strptime("2016-10-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-11-10", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.22", start=datetime.datetime.strptime("2016-11-10", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-11-22", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.23", start=datetime.datetime.strptime("2016-11-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2016-12-07", "%Y-%m-%d")),
    Patch(name="Season 6", patch="6.24", start=datetime.datetime.strptime("2016-12-07", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-01-11", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.1", start=datetime.datetime.strptime("2017-01-11", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-01-25", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.2", start=datetime.datetime.strptime("2017-01-25", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-02-08", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.3", start=datetime.datetime.strptime("2017-02-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-02-23", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.4", start=datetime.datetime.strptime("2017-02-23", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-03-08", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.5", start=datetime.datetime.strptime("2017-03-08", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-03-22", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.6", start=datetime.datetime.strptime("2017-03-22", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-04-05", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.7", start=datetime.datetime.strptime("2017-04-05", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-04-19", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.8", start=datetime.datetime.strptime("2017-04-19", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-05-03", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.9", start=datetime.datetime.strptime("2017-05-03", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-05-17", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.10", start=datetime.datetime.strptime("2017-05-17", "%Y-%m-%d"), end=datetime.datetime.strptime("2017-06-01", "%Y-%m-%d")),
    Patch(name="Season 7", patch="7.11", start=datetime.datetime.strptime("2017-06-01", "%Y-%m-%d"), end=None)
]

Patch._Patch__patches = patches
