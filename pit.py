#!/usr/bin/env python
import binascii
import os

__author__ = "Oz"
__copyright__ = "SAMSUNG Pit Parser"

header = "76983412"  # v 4.


def get_file(file_type):
    """
    find the file with the given extension and return the file name
    :return: file name
    """
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd, topdown=True):
        del dirs[:]  # remove the sub directories.
        for pf in files:
            if pf.endswith(file_type):
                return os.path.join(pf)


def fix_hex(mihex):
    sx = len(mihex)
    if sx % 2 == 0:
        return mihex
    else:
        mihex = mihex + "0"
        return mihex


def little_endian(deadbeef):  # ef be ad de
    temp = []
    deadbeef = list(deadbeef)
    for i in range(len(deadbeef)):
        temp.append(deadbeef[-2:])
        deadbeef.pop(-1)
        deadbeef.pop(-1)
        if not deadbeef:
            break
    temp = str(temp).replace("'", "").replace(",", "").replace("[", "").replace("]", "").replace(" ", "")
    return temp


if __name__ == '__main__':

    pit = get_file(".pit")
    i = 128
    if not pit:
        print "There is no '.pit' file in the directory"
    else:
        f = open(pit, "rb")
        file_contents = f.read()
        f.close()
        hex_file = bytearray(binascii.hexlify(file_contents))
        if header in hex_file:
            print "Platform".ljust(12) + " : " + hex_file[32:64].decode("hex").strip("00")
            x = len(hex_file)
            while i < x:
                partition = hex_file[i:i+32].strip("00")
                #print partition  # debug purpose
                partition = partition.replace("00","") # get rid of this .
                partition = fix_hex(partition).decode("hex")
                partition_file = hex_file[i+64:i+96].strip("00").decode("hex")
                addr = hex_file[i-32:i-24]
                hex_addr = little_endian(str(addr))
                addr = hex(int(hex_addr, 16) * 512)
                size = hex_file[i-24:i-16]
                hex_size = little_endian(str(size))
                size = hex(int(hex_size, 16) * 512)
                if partition.isalnum():
                    print partition.ljust(12) + " : "  + partition_file.ljust(20) + "  " + addr.ljust(12) + " " + size
                else:
                    print "END"
                    break
                i = i + 264
