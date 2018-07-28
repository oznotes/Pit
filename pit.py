#!/usr/bin/env python
import binascii
import os

__author__ = "Oz"
__copyright__ = "SAMSUNG Pit Parser"

header = "769834121f000000434f4d5f54415232"  # v 4.....COM_TAR2


def get_pit():
    """
    find the pit file
    :return: pit file name
    """
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd, topdown=True):
        del dirs[:]  # remove the sub directories.
        for pf in files:
            if pf.endswith(".pit"):
                return os.path.join(pf)


def fix_hex(mihex):
    sx = len(mihex)
    if sx % 2 == 0:
        return mihex
    else:
        mihex = mihex + "0"
        return mihex


if __name__ == '__main__':

    pit = get_pit()
    i = 128
    if not pit:
        print "There is no '.pit' file in the directory"
    else:
        f = open(pit, "rb")
        file_contents = f.read()
        f.close()
        hex_file = bytearray(binascii.hexlify(file_contents))
        if header in hex_file:
            print "CHIP SET".ljust(12) + " : " + hex_file[32:64].decode("hex").strip("00")
            x = len(hex_file)
            while i < x:
                partition = hex_file[i:i+32].strip("00")
                partition = fix_hex(partition).decode("hex")
                partition_file = hex_file[i+64:i+96].strip("00").decode("hex")
                if partition.isalnum():
                    print partition.ljust(12) + " : " + partition_file
                else:
                    print "END"
                    break
                i = i + 264
