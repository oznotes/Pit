#!/usr/bin/env python
# from __future__ import print_function

import binascii
import os
import sys
import tarfile
import time

__author__ = "Oz"
__copyright__ = "SAMSUNG Pit Parser and tar extract"

header = "76983412"  # v 4.
# convert
b = bytearray()
b.extend(map(ord, header))


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
    temp = ''.join(map(str, temp))
    temp = temp.replace("'", "").replace(
        '[', '').replace(']', '').replace(',', '').replace(' ', '')
    return temp


def extractor(hex_in, start, end):
    """
    given the byterray
    out:string

    """
    try:
        hex_out = str((binascii.unhexlify((hex_in[start:end].decode(
            "utf-8")).strip("00")))).replace("b'", "").replace("'", "")
    except binascii.Error:
        hex_out = str((binascii.unhexlify(
            (hex_in[start:end].decode("utf-8"))))).replace("b'", "").replace("'", "")
        hex_out = hex_out.replace("\\x00", "")
    # hex_out = fix_hex(hex_file)
    return hex_out


def bytearraytostr(by):
    """
    """
    by = by.replace("bytearray", "")
    by = by.replace("b'", "")
    by = by.replace("'", "")
    by = by.replace("(", "")
    by = by.replace(")", "")
    return by


if __name__ == '__main__':
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
        if b in hex_file:
            platform = extractor(hex_file, 32, 64)
            print("Platform".ljust(12) + " :", platform)
            x = len(hex_file)
            while i < x:
                """
                Pit File here :
                """
                partition = extractor(hex_file, i, i+32)
                partition_file = extractor(hex_file, i+64, i+96)
                addr = str(hex_file[i-32:i-24])  # location
                addr = bytearraytostr(addr)
                hex_addr = little_endian(str(addr))
                addr = hex(int(hex_addr, 16) * 512)
                size = str(hex_file[i-24:i-16])
                size = bytearraytostr(size)
                hex_size = little_endian(str(size))
                size = hex(int(hex_size, 16) * 512)
                if partition.isalnum():
                    if partition_file != "":
                        try:
                            """
                            Tar File is here:
                            """
                            # TODO : i need to find .
                            tar = tarfile.open(tar_file)
                            # check if folder is empty or not ?
                            tar.extract(partition_file, cwdir +
                                        "\\" + tar_file[0:6] + "\\extract")
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
