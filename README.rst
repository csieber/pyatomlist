pyatomlist
----------

List the position and types of atoms in a MP4 file.

This program is based on qtfaststart of danielgtaylor, which in turn is
based on qt-faststart.c from the ffmpeg project, which is released into 
the public domain, as well as ISO 14496-12:2005 (the official spec for
MP4), which can be obtained from the ISO or found online.

Features
--------

    * Works everywhere Python (2.6+) can be installed
    * Handles both 32-bit (stco) and 64-bit (co64) atoms

Installing from source
----------------------

Download a copy of the source, ``cd`` into the top-level
``pyatomlist`` directory, and run::

    python setup.py install

If you are installing to your system Python (instead of a virtualenv), you
may need root access (via ``sudo`` or ``su``).

Usage
-----
See ``pyatomlist --help`` for more info! If outfile is not present then
the infile is overwritten::

    $ pyatomlist infile

To run without installing you can use::

    $ bin/pyatomlist infile

If on Windows, the pyatomlist script will not execute, so use::

    > python -m pyatomlist ...

History
-------
    * 2016-01-20: Fork of qtfaststart to pyatomlist.
    
For the history predating pyatomlist, please check qtfaststart.

License
-------

Copyright (C) 2016 Christian Sieber <c.sieber@tum.de>

Copyright (C) 2008 - 2013  Daniel G. Taylor <dan@programmer-art.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
