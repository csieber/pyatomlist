"""
    The guts that actually do the work. This is available here for the
    'pyatomlist' script and for your application's direct use.
"""

import shutil
import logging
import os
import struct
import collections

import io

from pyatomlist.exceptions import FastStartSetupError
from pyatomlist.exceptions import MalformedFileError
from pyatomlist.exceptions import UnsupportedFormatError

# This exception isn't directly used, included it for backward compatability
# in the event someone had used it from our namespace previously
from pyatomlist.exceptions import FastStartException

CHUNK_SIZE = 8192

log = logging.getLogger("pyatomlist")

# Older versions of Python require this to be defined
if not hasattr(os, 'SEEK_CUR'):
    os.SEEK_CUR = 1

Atom = collections.namedtuple('Atom', 'name position size')

def read_atom(datastream):
    """
        Read an atom and return a tuple of (size, type) where size is the size
        in bytes (including the 8 bytes already read) and type is a "fourcc"
        like "ftyp" or "moov".
    """
    size, type = struct.unpack(">L4s", datastream.read(8))
    type = type.decode('ascii')
    return size, type


def _read_atom_ex(datastream):
    """
    Read an Atom from datastream
    """
    pos = datastream.tell()
    atom_size, atom_type = read_atom(datastream)
    if atom_size == 1:
        atom_size, = struct.unpack(">Q", datastream.read(8))
    return Atom(atom_type, pos, atom_size)


def get_index(datastream):
    """
        Return an index of top level atoms, their absolute byte-position in the
        file and their size in a list:

        index = [
            ("ftyp", 0, 24),
            ("moov", 25, 2658),
            ("free", 2683, 8),
            ...
        ]

        The tuple elements will be in the order that they appear in the file.
    """
    log.debug("Getting index of top level atoms...")

    index = list(_read_atoms(datastream))
    _ensure_valid_index(index)

    return index


def _read_atoms(datastream):
    """
    Read atoms until an error occurs
    """
    while datastream:
        try:
            atom = _read_atom_ex(datastream)
            log.debug("%s: %09d - %09d (%s Bytes)" % (atom.name, atom.position, atom.position + atom.size, atom.size))
        except:
            break

        yield atom

        if atom.size == 0:
            if atom.name == "mdat":
                # Some files may end in mdat with no size set, which generally
                # means to seek to the end of the file. We can just stop indexing
                # as no more entries will be found!
                break
            else:
                # Weird, but just continue to try to find more atoms
                continue

        datastream.seek(atom.position + atom.size)


def _ensure_valid_index(index):
    """
    Ensure the minimum viable atoms are present in the index.

    Raise MalformedFileError if not.
    """
    top_level_atoms = set([item.name for item in index])
    for key in ["moov", "mdat"]:
        if key not in top_level_atoms:
            msg = "%s atom not found, is this a valid MOV/MP4 file?" % key
            log.warn(msg)
            raise MalformedFileError(msg)


def find_atoms(size, datastream):
    """
    Compatibilty interface for _find_atoms_ex
    """
    fake_parent = Atom('fake', datastream.tell()-8, size+8)
    for atom in _find_atoms_ex(fake_parent, datastream):
        yield atom.name


def _find_atoms_ex(parent_atom, datastream):
    """
        Yield either "stco" or "co64" Atoms from datastream.
        datastream will be 8 bytes into the stco or co64 atom when the value
        is yielded.

        It is assumed that datastream will be at the end of the atom after
        the value has been yielded and processed.

        parent_atom is the parent atom, a 'moov' or other ancestor of CO
        atoms in the datastream.
    """
    stop = parent_atom.position + parent_atom.size

    while datastream.tell() < stop:
        try:
            atom = _read_atom_ex(datastream)
        except:
            msg = "Error reading next atom!"
            log.exception(msg)
            raise MalformedFileError(msg)

        if atom.name in ["trak", "mdia", "minf", "stbl"]:
            # Known ancestor atom of stco or co64, search within it!
            for res in _find_atoms_ex(atom, datastream):
                yield res
        elif atom.name in ["stco", "co64"]:
            yield atom
        else:
            # Ignore this atom, seek to the end of it.
            datastream.seek(atom.position + atom.size)

def _moov_is_compressed(datastream, moov_atom):
    """
        scan the atoms under the moov atom and detect whether or not the
        atom data is compressed
    """
    # seek to the beginning of the moov atom contents
    datastream.seek(moov_atom.position+8)
    
    # step through the moov atom childeren to see if a cmov atom is among them
    stop = moov_atom.position + moov_atom.size
    while datastream.tell() < stop:
        child_atom = _read_atom_ex(datastream)
        datastream.seek(datastream.tell()+child_atom.size - 8)
        
        # cmov means compressed moov header!
        if child_atom.name == 'cmov':
            return True
    
    return False

def get_chunks(stream, chunk_size, limit):
    remaining = limit
    while remaining:
        chunk = stream.read(min(remaining, chunk_size))
        if not chunk:
            return
        remaining -= len(chunk)
        yield chunk
