#!/usr/bin/env python
from __future__ import print_function

import binascii
import os
import sys
import tarfile
import time

__author__ = "Oz"
__copyright__ = "SAMSUNG Pit Parser snd tar extract"

header = "76983412"  # v 4.


def get_file(file_type):
    """
    find the file with the given extension and return the file name
    :return: file name
    """
    cwd = os.getcwd()
    for _root, dirs, files in os.walk(cwd, topdown=True):
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
    for _ in range(len(deadbeef)):
        temp.append(deadbeef[-2:])
        deadbeef.pop(-1)
        deadbeef.pop(-1)
        if not deadbeef:
            break
    temp = "".join(temp)  # join the list
    return temp


if __name__ == '__main__':

    # d = disk
    # reader  = d.detect_disk()
    # if reader[0] == True:
    cwdir = os.getcwd()
    tar_file = get_file(".md5")
    if not tar_file:
        print("There is no .tar.md5 file in the directory")
        sys.exit(0)
    pit = get_file(".pit")
    i = 128
    if not pit:
        print("There is no '.pit' file in the directory")
        sys.exit(0)
    else:
        f = open(pit, "rb")
        file_contents = f.read()
        f.close()
        hex_file = bytearray(binascii.hexlify(file_contents))
        if header in hex_file:
            print("Platform".ljust(12) + " : " +
                  hex_file[32:64].decode("hex").strip("00"))
            x = len(hex_file)
            while i < x:
                partition = hex_file[i:i+32].strip("00")
                #  print partition  # debug purpose
                partition = partition.replace("00", "")  # get rid of this .
                partition = fix_hex(partition).decode("hex")
                partition_file = hex_file[i+64:i+96].strip("00").decode("hex")
                addr = hex_file[i-32:i-24]
                hex_addr = little_endian(str(addr))
                addr = hex(int(hex_addr, 16) * 512)
                size = hex_file[i-24:i-16]
                hex_size = little_endian(str(size))
                size = hex(int(hex_size, 16) * 512)
                if partition.isalnum():
                    if partition_file != "":
                        try:
                            # TODO : i need to find .
                            tar = tarfile.open(tar_file)
                            tar.extract(partition_file, cwdir)
                            tar.close()
                            time.sleep(0.05)
                            print(
                                partition.ljust(12) + " : " +
                                partition_file.ljust(20) + " " +
                                addr.strip("L").ljust(12) + " " +
                                size.strip("L").ljust(12) + " " +
                                "Extracted")
                        except KeyError:
                            time.sleep(0.05)
                            print(
                                partition.ljust(12) + " : " +
                                partition_file.ljust(20) + " " +
                                addr.strip("L").ljust(12) + " " +
                                size.strip("L").ljust(12) + " " +
                                "Not Found")
                    else:
                        print(
                            partition.ljust(12) + " : " +
                            partition_file.ljust(20) + " " +
                            addr.strip("L").ljust(12) + " " +
                            size.strip("L").ljust(12))
                else:
                    print("END")
                    break
                i = i + 264  # 84 bytes each block of pit
        else:
            "This .pit file seems wrong\n" \
                "Please send us to analyze"
