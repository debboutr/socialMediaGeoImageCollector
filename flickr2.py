# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 09:47:13 2016

@author: Rdebbout
"""

from flickrapi import FlickrAPI
import time
import pandas as pd
#import numpy as np
from datetime import datetime as dt
from django.utils.encoding import smart_str

def pics2table(flickrList):
    tbl = pd.DataFrame()
    for f in flickrList:
        try:
            picID = smart_str(f['id'])
            minDate = f['dateupload']
            post = dt.fromtimestamp(int(minDate)).strftime('%Y-%m-%d')
            latitude = smart_str(f['latitude'])
            longitude = smart_str(f['longitude'])        
            title = smart_str(f['title'])
            username = smart_str(f['ownername'])
            url = smart_str(f['url_m'])
        except:
            continue
        tbl = tbl.append(pd.DataFrame([[latitude, longitude, picID, post, username, title, url, minDate]], columns=cols), ignore_index=True)           
    return tbl
    
def loopPages(picTbl, holdDate):
    for x in range(1,25):
        pics = flickr.photos.search(bbox=box, page=x, extras=xtras, max_upload_date=holdDate)
        #print 'Page: %s' % x
        addTbl = pics2table(pics['photos']['photo'])
        picTbl = pd.concat([picTbl, addTbl])
        picTbl.to_csv(f, index=False)
        
def drill(picTbl, holdDate):
    diff = 1
    while diff > 0:
        l1 = len(picTbl)
        loopPages(picTbl, holdDate)
        picTbl = pd.read_csv(f)
        picTbl = picTbl.drop_duplicates('picID')
        l2 = len(picTbl)
        diff = abs(l1-l2)
        holdDate = picTbl.unix_time.min()
        print dt.fromtimestamp(int(holdDate)).strftime('%Y-%m-%d')
    
FLICKR_PUBLIC = '08efe8fb64319b6dec58512d23408004'
FLICKR_SECRET = '07b1081fb8daed0f'

# set bounding x,y values - DULUTH
minX = -92.335981
minY = 46.630695
maxX = -91.946101
maxY = 46.804721
# set bounding x,y values - MILTOWN
#minX = -88.231662
#minY = 42.838153
#maxX = -87.789201
#maxY = 43.444837
box = '%s,%s,%s,%s' % (minX,minY,maxX,maxY)
f = 'D:/Projects/Panoramio/doubleDownDUL2.csv'
picTbl = pd.DataFrame()
holdDate = int(time.time())
flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
cols = ['latitude', 'longitude', 'picID', 'post_date', 'username', 'title', 'url', 'unix_time']
xtras='geo, tags, media, url_m, date_upload, owner_name'
drill(picTbl, holdDate)

#################################################################################################
#picTbl = pd.read_csv('D:/Projects/Panoramio/flickPicsQuick_MIL.csv')
#picTbl = picTbl.drop_duplicates('picID')
#holdDate = picTbl.unix_time.min()
#print dt.fromtimestamp(int(holdDate)).strftime('%Y-%m-%d')
#pics = flickr.photos.search(bbox=box, page=1, extras=xtras, max_upload_date=holdDate)
#pages = pics['photos']['pages']
#picTbl = loopPages(picTbl, holdDate)

#################################################################################################

#picTbl = picTbl.drop_duplicates('picID')
#tbl = pd.read_csv('D:/Projects/Panoramio/flickPicsQuick_DUL.csv')
#tbl2 = pd.read_csv('D:/Projects/Panoramio/doubleDownDUL.csv')
#tbl.dtypes
#picTbl.dtypes
#new = tbl2.picID.values
#old = tbl.picID.values
#keep = []
#for x in old:
#    if not x in new:
#        keep.append(x)
#        
#        win = tbl.ix[tbl.picID.isin(keep)]
#        win.to_csv('D:/Projects/Panoramio/check_MIL.csv', index=False)
#        nerd = pd.concat([picTbl,win])
#        
#for x in new:
#    if not x in old:
#        keep.append(x)
#nerd = nerd.drop_duplicates('picID')
#nerd.columns
#nerd = nerd.drop(['create_date','time'], axis=1)
#nerd.to_csv('D:/Projects/Panoramio/flickPicsQuick_MIL.csv', index=False)