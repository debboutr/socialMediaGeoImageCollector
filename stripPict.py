# -*- coding: utf-8 -*-
"""
Created on Thu May 26 23:27:17 2016

@author: rick
"""

import sys

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom)

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom)
    
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat *= -1

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon *= -1

    return lat, lon


################
# Example ######
################
if __name__ == "__main__":
    # load an image through PIL's Image object
    if len(sys.argv) < 2:
        print "Error! No image file specified!"
        print "Usage: %s <filename>" % sys.argv[0]
        sys.exit(1)

    image = Image.open(sys.argv[1])
    exif_data = get_exif_data(image)
    print get_lat_lon(exif_data)
import os
import sys
import gdal
from gdalconst import *
filename = '/home/rick/Desktop/IMG_20160526_215459257.jpg'
filename = '/media/rick/600ABCCF0ABCA386/Users/rick/Documents/macDunn/IMG_20160528_170902043.jpg'

class photo_xy(object):
    def __init__(self, name):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.name = name
        dataset = gdal.Open(self.name, GA_ReadOnly)    
        self.meta = dataset.GetMetadata()
        self.lat = metadata['EXIF_GPSLatitude']
        self.latlatRef = metadata['EXIF_GPSLatitudeRef']
        self.lon = metadata['EXIF_GPSLongitude']
        self.latlonRef = metadata['EXIF_GPSLongitudeRef']
        self.latDD = latDD(self.lat)
        self.lonDD = lonDD(self.lon)
#    def latDD(self):
#        D = int(self.lat[1:3])
#        M = int(self.lat[6:8])
#        S = int(self.lat[11:13])
#        self.latDD = D + float(M)/60 + float(S)/3600
#        return self.latDD
#    def lonDD(self):
#        D = int(self.lon[1:4])
#        M = int(self.lon[7:9])
#        S = int(self.lon[12:14])
#        self.lonDD = D + float(M)/60 + float(S)/3600
#        return self.lonDD

photo = photo_xy(filename)
photo.latDD
photo.lonDD

all_dir = '/media/rick/600ABCCF0ABCA386/Users/rick/Documents/Corvallis2Coast/Ride_05_29'
for img in os.listdir('/media/rick/600ABCCF0ABCA386/Users/rick/Documents/Corvallis2Coast/Ride_05_29'):
    filename = '{}/{}'.format(all_dir, img)
dataset = gdal.Open( filename, GA_ReadOnly)
metadata = dataset.GetMetadata()
lat = metadata['EXIF_GPSLatitude']
latRef = metadata['EXIF_GPSLatitudeRef']
lon = metadata['EXIF_GPSLongitude']
lonRef = metadata['EXIF_GPSLongitudeRef']
      
#      lat = _convert_to_degress(lat)
#            if gps_latitude_ref != "N":                     
#                lat *= -1
#
#            lon = _convert_to_degress(lon)
#            if gps_longitude_ref != "E":
#                lon *= -1
#                
#lat.replace(" ", "").split(')')
#DD = {}
#for clip in len(lat.replace(" ", "").replace("(","").split(')')):
#     lat.replace(" ", "").replace("(","").split(')')[clip]


#def latDD(x):
#  D = int(x[1:3])
#  M = int(x[3:5])
#  S = float(x[5:])
#  DD = D + float(M)/60 + float(S)/3600
#  return DD

# Expression
def latDD(x):
    D = int(x[1:3])
    M = int(x[6:8])
    S = int(x[11:13])
    DD = D + float(M)/60 + float(S)/3600
    return DD
def lonDD(x):
    D = int(x[1:4])
    M = int(x[7:9])
    S = int(x[12:14])
    DD = D + float(M)/60 + float(S)/3600
    return DD
latDD = latDD(lat)
lonDD = lonDD(lon)
print '{}{}, {}{}'.format(latDD, latRef, lonDD, lonRef)
lat.replace(" ", "").replace("(","").split(')')