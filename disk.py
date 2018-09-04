from __future__ import print_function

import sys
import time

import wmi

__author__ = "Oz"
__copyright__ = "Disk Reader WMI"


def read_in_chunks(fileobj, chunksize=65536):
    """
    Lazy function to read a file piece by piece.
    Default chunk size: 64kB.
    """
    while True:
        data = fileobj.read(chunksize)
        if not data:
            break
        yield data


def detect_disk():
    count = 0
    disks = []
    while disks == []:
        disks = wmi.WMI().Win32_DiskDrive(MediaType="Removable Media")
        if disks == []:
            time.sleep(2)
            print ("Please connect ")
            if count == 10:
                return False, "a", "b", "c"
            count += 1
        else:
            for disk in disks:
                disk_size = int(disk.size)
                gig = 1024 * 1024
                uid = disk.serialnumber
                sector_size = disk.BytesPerSector
            return True, disk.name, disk_size, sector_size


def reading():
    pass


def writing(d, image, addr):
    f = open(image, "rb")
    booster = open(d, "r+b")
    addr2 = addr.strip("L")
    addr2 = int(addr2, 16)
    print("  Flashing...", end="")
    booster.seek(addr2)
    for piece in read_in_chunks(f):
        booster.write(piece)
    print ("Completed")
    return True
