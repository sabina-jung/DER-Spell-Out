import argparse
import base64
import logging
import re
import sys

import der

# parse args
parser = argparse.ArgumentParser(description='List data fields of a PEM/DER encoded file.')
parser.add_argument('file', metavar='FILENAME', type=argparse.FileType('r'), 
                   help='specify file to be used')
parser.add_argument('--verbose', '-v', action='count')
args = parser.parse_args()

# configure logging
logging_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
logging_sane_level = logging_levels.index(logging.ERROR)
if args.verbose:
    logging_sane_level = min(max(args.verbose, 0), len(logging_levels)-1)
logging.basicConfig(level=logging_levels[logging_sane_level])
logging.info("Logging level: %s" % (
    logging.getLevelName(logging.getLogger().getEffectiveLevel())));

# get file from pared args
dat = args.file
logging.info("Using file \"%s\"." % (dat.name))


base64re = re.compile('[A-Za-z0-9\/\=\+]+')  # valid base64 data
base64data = ""

# Collect all Base64 lines
while True:
    lineFromFile = dat.readline()     
    if lineFromFile == "": break  # EOF?
    lineFromFile = lineFromFile.rstrip()
    # wait for the fist base64 line 
    # and stop when base64 data ceases
    if not base64re.match(lineFromFile): 
        if base64data == "":
            continue
        else:
            break
    base64data += lineFromFile
    
logging.debug("Stopped at line \"%s\"." % (lineFromFile))
logging.debug("Got Base64: %s" % (base64data))

dat.close()

raw = base64.b64decode(bytearray(base64data, "ascii"))
logging.debug("Raw DER: %s" % (repr(raw)))
logging.info("Read %d bytes." % len(raw))
# Python 2 bytearrays consist of strings
if len(raw) > 0 and type(raw[0]) == str:
    raw = [ord(x) for x in raw]
der.readDer(raw)

