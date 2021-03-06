# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 09:47:13 2016

This script uses the flickrapi package to find images/videos from flickr 
within a given bounding box, which needs to be in a geographic projection.

@author: Rdebbout
"""

from flickrapi import FlickrAPI
import time
import pandas as pd
from datetime import datetime as dt
from django.utils.encoding import smart_str

def pics2table(flickrList):
    '''
    __author__ = "Rick Debbout <debbout.rick@epa.gov>"

    Strips out the dictionary info for each image returned from the flickr 
    search request and returns a pandas table with the results.

    Arguments
    ---------
    flickrList     : a list of dictionaries returned from the search request.
    '''
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
        it = [latitude, longitude, picID, post, username, title, url, minDate]
        tbl = pd.concat([tbl,pd.DataFrame([it], columns=cols)])
    return tbl
    
def loopPages(picTbl, holdDate):
    '''
    __author__ = "Rick Debbout <debbout.rick@epa.gov>"

    Loops through pages that are returned in the search function, stops at 25 
    because there are never new unique pics past page 18.

    Arguments
    ---------
    picTbl     : pandas tableholding the accumulated results while collecting
    holdDate   : retains unix date value for search function max_upload_date.
    '''
    for x in range(1,25):
        pics = flickr.photos.search(bbox=box, page=x, 
                                    extras=xtras, max_upload_date=holdDate)
        addTbl = pics2table(pics['photos']['photo'])
        picTbl = pd.concat([picTbl, addTbl])
        picTbl.to_csv(f, index=False)
        
def drill(picTbl, holdDate):
    '''
    __author__ = "Rick Debbout <debbout.rick@epa.gov>"

    Loops through pages that are returned in the search function, stops at 25 
    because there are never new unique pics past page 18.

    Arguments
    ---------
    picTbl     : pandas tableholding the accumulated results while collecting
    holdDate   : retains unix date value for search function max_upload_date.
    '''
    diff = 1
    while diff > 0:
        try:
            l1 = len(picTbl)
            loopPages(picTbl, holdDate)
            picTbl = pd.read_csv(f)
            picTbl = picTbl.drop_duplicates('picID')
            l2 = len(picTbl)
            diff = abs(l1-l2)
            holdDate = picTbl.unix_time.min()
            print dt.fromtimestamp(int(holdDate)).strftime('%Y-%m-%d')
        except:
            continue
    
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
# identify the working directory -- home
home = 'D:/Projects/Panoramio'
# identify the name of the file to hold the resulting table -- name
name = 'scriptTest_DUL'
f = '{}/{}.csv'.format(home, name)
picTbl = pd.DataFrame()
holdDate = int(time.time())
flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
cols = ['latitude','longitude','picID','post_date',
        'username','title','url','unix_time']
xtras='geo, tags, media, url_m, date_upload, owner_name'
drill(picTbl, holdDate)
picTbl = picTbl.drop_duplicates('picID')
print "Finished collecting images within the bounding box"
###############################################################################

