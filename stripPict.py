# -*- coding: utf-8 -*-
"""
Created on Thu May 26 23:27:17 2016

@author: rick
"""
import os
import gdal
from gdalconst import *
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

def getDD(string, ref, start = '(', stop = ')'):
    for x in range(3):
        if x == 0:
            D = int(string[string.index(start)+1:string.index(stop)])
        if x == 1:
            M = float(string[string.index(start)+1:string.index(stop)])
        if x == 2:
            S = float(string[string.index(start)+1:string.index(stop)])
        string = string [string.index(stop) + 1 :]
    DD = D + (M/60) + (S/3600)
    if ref in ['S', 'W']:
        DD = DD * -1    
    return DD

pic_dir = '/media/rick/600ABCCF0ABCA386/Users/rick/Documents/Corvallis2Coast/Ride_05_29'
cols = ['latitude', 'longitude', 'image_loc']
tbl = pd.DataFrame()
crs = {u'datum': u'WGS84', u'no_defs': True, u'proj': u'longlat'}
for img in os.listdir(pic_dir):
    if '.jpg' in img:
        filename = '{}/{}'.format(pic_dir, img)
        try:
            dataset = gdal.Open( filename, GA_ReadOnly)
        except:
            continue
        metadata = dataset.GetMetadata()
        if metadata.has_key('EXIF_GPSLatitude'):
            lat = metadata['EXIF_GPSLatitude']
            latRef = metadata['EXIF_GPSLatitudeRef']
            lon = metadata['EXIF_GPSLongitude']
            lonRef = metadata['EXIF_GPSLongitudeRef']
        else:
            continue
        latitude = getDD(lat, latRef) 
        longitude = getDD(lon, lonRef)
        dataset = None 
        tbl = tbl.append(pd.DataFrame([[latitude, longitude, filename]], columns=cols), ignore_index=True)
geometry = [Point(xy) for xy in zip(tbl.longitude, tbl.latitude)]
geo_df = gpd.GeoDataFrame(tbl, crs=crs, geometry=geometry)
geo_df.to_file('%s/shape/nora.shp' % pic_dir)
    
#class stripper(object):
#    def __init__(self, meta):
#        """Return a Customer object whose name is *name* and starting
#        balance is *balance*."""
#        self.lat = meta['EXIF_GPSLatitude']
#        self.latRef = meta['EXIF_GPSLatitudeRef']
#        self.lon = meta['EXIF_GPSLongitude']
#        self.lonRef = meta['EXIF_GPSLongitudeRef']
#    def makeDMS(self, start = '(', stop = ')'):
#        for x in range(3):    
#            if x == 0:
#                D = int(string[string.index(start)+1:string.index(stop)])
#            if x == 1:
#                M = float(string[string.index(start)+1:string.index(stop)])
#            if x == 2:
#                S = float(string[string.index(start)+1:string.index(stop)])
#            string = string [string.index(stop) + 1 :]
#        DD = D + M/60 + S/3600
#        return DD 
#    def makeDMS(self):
#        self.lonDD = D + M/60 + S/3600
#        return self.lonDD