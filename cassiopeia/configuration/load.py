import sys
import os
import configparser


config = configparser.ConfigParser()
head, tail = os.path.split(__file__)
if len(sys.argv) > 1 and any(fn.endswith(".ini") for fn in sys.argv):
    for fn in sys.argv:
        if fn.endswith(".ini"):
            filename = fn
            break
else:
    filename = os.path.join(head, "default.ini")

if not os.path.exists(filename):
    filename = os.path.join(head, filename)
    if not os.path.exists(filename):
        filename = os.path.join(head, "default.ini")

config.read(filename)
