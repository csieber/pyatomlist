
from __future__ import print_function

import logging
import os
import shutil
import sys
import tempfile

from optparse import OptionParser
from pyatomlist import VERSION
from pyatomlist import processor
from pyatomlist.exceptions import FastStartException

log = logging.getLogger("pyatomlist")

def run():
    logging.basicConfig(level = logging.INFO, stream = sys.stdout,
                        format = "%(message)s")

    parser = OptionParser(usage="%prog [options] infile",
                          version="%prog " + VERSION)

    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true",
                      help="Enable debug output")

    options, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit(1)

    if options.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    index = processor.get_index(open(args[0], "rb"))

    for atom, pos, size in index:
        if atom == "\x00\x00\x00\x00":
            # Strange zero atom... display with dashes rather than
            # an empty string
            atom = "----"

        print("%d,%s,%d" % (pos, atom, size))

    raise SystemExit

