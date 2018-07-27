#!/usr/bin/env python
import binascii
import sys
import os

__author__ = "Oz"
__copyright__ = "SAMSUNG Pit Parser"

header = "769834121f000000434f4d5f54415232"  # v 4.....COM_TAR2

def get_pit():
    """
    find the pit file and return the file name .
    :return: pit file name
    """
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd, topdown=True):
        del dirs[:]  # remove the sub directories.
        for file in files:
            if file.endswith(".pit"):
                return os.path.join(file)


if __name__ == '__main__':

    pit = get_pit()
    if not pit:
        print "There is no .pit file in the directory"
    else:
        f = open(pit, "rb")
        file_contents = f.read()
        f.close()
        hex_file = bytearray(binascii.hexlify(file_contents))
        if header in hex_file:
            print "Pit Header"



