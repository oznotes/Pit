#!/usr/bin/env python
import binascii
import sys
import os
import re

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
    i = 128
    if not pit:
        print "There is no .pit file in the directory"
    else:
        f = open(pit, "rb")
        file_contents = f.read()
        f.close()
        hex_file = bytearray(binascii.hexlify(file_contents))
        if header in hex_file:
            print "CHIPSET : " + hex_file[32:64].decode("hex").strip("00")
            x = len(hex_file)
            while i < x:
                partition = hex_file[i:i+32].strip("00").decode("hex")
                partition_file = hex_file[i+64:i+96].strip("00").decode("hex")
                #if partition.isalpha()is True:
                print partition + " : " + partition_file

           # if bool(re.match('^[a-zA-Z0-9]+$', partition)):
           #         print partition + " : " + partition_file

                i = i + 264
