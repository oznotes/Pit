import wmi
import time

__author__ = "Oz"
__copyright__ = "Disk Reader WMI"

"""
Useful parameters :

Availability	        ;	Manufacturer	            ;	SectorsPerTrack
BytesPerSector	        ;	MaxBlockSize	            ;	SerialNumber
Capabilities	        ;	MaxMediaSize	            ;	Signature
CapabilityDescriptions	;	MediaLoaded	                ;	Size
Caption	                ;	MediaType	                ;	Status
CompressionMethod	    ;	MinBlockSize	            ;	StatusInfo
ConfigManagerErrorCode	;	Model	                    ;	SystemCreationClassName
ConfigManagerUserConfig	;	Name	                    ;	SystemName
CreationClassName	    ;	NeedsCleaning	            ;	TotalCylinders
DefaultBlockSize	    ;	NumberOfMediaSupported	    ;	TotalHeads
Description	            ;	Partitions	                ;	TotalSectors
DeviceID	            ;	PNPDeviceID	                ;	TotalTracks
ErrorCleared	        ;	PowerManagementCapabilities	;	TracksPerCylinder
ErrorDescription	    ;	PowerManagementSupported		
ErrorMethodology	    ;	SCSIBus		
FirmwareRevision	    ;	SCSILogicalUnit		
Index	                ;	SCSIPort		
datetime InstallDate	;	SCSITargetId		
InterfaceType	        ;			
LastErrorCode	        ;	

Notes : 
her 512 byte da , 4 byte checksum
TODO : reading size 		
"""


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
            print "Please connect "
            if count == 10:
                return False, "a", "b", "c"
            count += 1
        else:
            for disk in disks:
                disk_size = int(disk.size)
                gig = 1024 * 1024
                uid = disk.serialnumber
                sector_size = disk.BytesPerSector
                """

                print(disk.Model)
                print\
                    (
                            disk.name + " \n"
                            "Size : " + str(disk_size/gig) + " MB  \n"
                            "Sector : " + str(int(sector_size)) + " bytes"
                    )
                """
            return True, disk.name, disk_size, sector_size


def reading():
    pass


def writing(d, image, addr):
    # windows generic access for writing disks
    flash = open(image, "rb")
    addr2 = int(addr, 16)
    whole = flash.read()
    x = len(whole)
    chunk = x/100
    booster = open(d, "r+b")
    booster.seek(addr2)
    for x in range(100):
        data = flash.read(chunk)
        booster.write(data)
        time.sleep(0.05)
