# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:09:26 2016

@author: Rdebbout
"""

import flickr_api
import webbrowser
import pandas as pd
import numpy as np
from datetime import datetime as dt
from django.utils.encoding import smart_str
import time

home = 'D:/Projects/Panoramio'

key = 'b02389167452adc6203d953bdfe172eb'
secret = 'f4854805c1a8164e'
flickr_api.set_keys(api_key = key, api_secret = secret)
a = flickr_api.auth.AuthHandler() #creates the AuthHandler object
perms = "read" # set the required permissions
url = a.get_authorization_url(perms)
webbrowser.open_new_tab(url)
#set from the <oauth_verifier> tag 
a.set_verifier('d6ea0ed14bfaf185')
a.save('{}/flickr_api_auth.txt'.format(home))



# add a way to dynamically call this file into the script
flickr_api.auth.AuthHandler.load('{}/flickr_api_auth.txt'.format(home))

# set bounding x,y values - DULUTH
#minX = -92.335981
#minY = 46.630695
#maxX = -91.946101
#maxY = 46.804721
# set bounding x,y values - MILTOWN
minX = -88.231662
minY = 42.838153
maxX = -87.789201
maxY = 43.444837
box = '%s,%s,%s,%s' % (minX,minY,maxX,maxY)



cols = ['latitude', 'longitude', 'picID', 'create_date', 'post_date', 
        'time', 'username', 'title', 'url', 'unix_time']
pics = flickr_api.Photo.search(bbox=box, format='parsed-json')
pages = pics.info['pages']
# this is assuming that the first record returned is the most recent
holdDate = flickr_api.Photo.getInfo(pics[0])['posted'] 
gotten = []
# date and time are recorded from the time and date that they were taken, 
# not the date that they were posted necessarily


def loopPages(picTbl, holdDate):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                   page=1, max_upload_date=holdDate)
    pages = pics.info['pages']
    for x in range(4,pages+1):
        pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                       page=x, max_upload_date=holdDate)
        print 'Page: %s' % x
        addTbl = pics2table(pics)
        if len(addTbl) == 0:
            print 'broken'
            holdDate = picTbl.unix_time.min()
            if x == 1:
                break
                return None
            loopPages(picTbl, holdDate)
        picTbl = pd.concat([picTbl, addTbl])
        picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)
        
        
def pics2table(flickrList):
    tbl = pd.DataFrame()
    count = 0
    for f in flickrList:
        picID = smart_str(f['id'])
        if not picID in gotten:
            try:
                info = flickr_api.Photo.getInfo(f)
                minDate = info['posted']
                post = dt.fromtimestamp(int(minDate)).strftime('%Y-%m-%d')
                latitude = smart_str(info['location']['latitude'])
                longitude = smart_str(info['location']['longitude'])        
                title = smart_str(f['title'])
                print f['owner']
                username = smart_str(f['owner']['username'])
                url = smart_str(f.getPhotoFile('Medium'))
            except:
                continue
            date = smart_str(info['taken'].split(' ')[0])
            t = smart_str(info['taken'].split(' ')[1])
            it = [latitude, longitude, picID, date, post, t, 
                  username, title, url, minDate]
            tbl = tbl.append(pd.DataFrame([it],columns=cols),ignore_index=True)
            gotten.append(picID)            
            print count
            count += 1   
    return tbl

###############################################################################
# first loop through all of the original returns retaining the holdDate as the 
# minimum to pas to next loop
picTbl = pd.DataFrame()
for x in range(1,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                   page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl = pics2table(pics)
    if len(addTbl) == 0:
        print 'broken'
        holdDate = picTbl.unix_time.min()
        if x == 1:
            break
        loopPages()
    picTbl = pd.concat([picTbl, addTbl])
    picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)

###############################################################################
dt.fromtimestamp(int(holdDate)).strftime('%Y-%m-%d')
gotten = picTbl.picID.tolist()
flickr_api.Photo.search(bbox=box, format='parsed-json', 
                        page=1, max_upload_date=holdDate)
picTbl = pd.read_csv('{}/flickPics_MIL.csv'.format(home))
all(x in picTbl.picID.values for x in addTbl.picID.values)
for f in pics:
    picID = smart_str(f['id'])
    if not picID in gotten:
        print picID
xtras = 'geo, tags, media, url_m'
xtras = 'owner_name'
xtras = ['date_upload', 'geo', 'url_m']

pics = flickr_api.Photo.search(bbox=box, extras=xtras, format='parsed-json', 
                               max_upload_date=int(time.time()))
f= pics[0]
pics.info['pages']
smart_str(f['id']) in gotten
f['url_m']
f['tags']
f['media']
f['owner']['username']
f['description']
f['original_format']
pics.info['location']['latitude']
f['location']['latitude']
f['location']['longitude']
f['posted']
f['taken']
f['geo']
f['date_upload']
f['username']
f['farm']
pics['photos']

def pics2table2(flickrList):
    tbl = pd.DataFrame()
    count = 0
    for f in flickrList:
        picID = smart_str(f['id'])
        if not picID in gotten:  
            print f['owner']
            print f['posted']
            minDate = f['posted']
            post = dt.fromtimestamp(int(minDate)).strftime('%Y-%m-%d')
            latitude = smart_str(f['location']['latitude'])
            longitude = smart_str(f['location']['longitude'])        
            title = smart_str(f['title'])
            username = smart_str(f['owner']['username'])
            try:
                url = smart_str(f['url_m'])
            except:
                continue
            date = smart_str(f['taken'].split(' ')[0])
            t = smart_str(f['taken'].split(' ')[1])
            tbl = tbl.append(pd.DataFrame([[latitude, longitude, picID, date, post, t, username, title, url, minDate]], columns=cols), ignore_index=True)
            gotten.append(picID)            
            print count
            count += 1   
    return tbl

addTbl = pics2table2(pics)


#holdDate = 1261705750
picTbl = picTbl.drop_duplicates('picID')


        
final = loopPages(picTbl, holdDate)        

        
def findUniquereturns(flickrList):
    for f in flickrList:
        picID = smart_str(f['id'])
        if not picID in gotten:
            gotten.append(picID)
    
def loopUniqueVals(pages):
    for x in range(1,pages+1):
        print x
        pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                       page=x, max_upload_date=holdDate)
        findUniquereturns(pics)
    
loopUniqueVals(pages)    
len(set(gotten))

#holdDate = str(holdDate).decode("utf-8")


for x in range(1,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                   page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl = pics2table(pics)
    if len(addTbl) == 0:
        print 'broken'
        holdDate = picTbl.unix_time.min()
        break
    picTbl = pd.concat([picTbl, addTbl])
    picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)


###############################################################################

picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)
picTbl = pd.read_csv('{}/flickPics_MIL.csv'.format(home))
holdDate = picTbl.unix_time.min()
x=1
pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                               page=x, max_upload_date=holdDate)
pages = pics.info['pages']
for x in range(1,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                   page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl = pics2table(pics)
    if len(addTbl) == 0:
        print 'broken'
        holdDate = picTbl.unix_time.min()
        break
    picTbl = picTbl.append(addTbl)
    picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)

picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)
picTbl = pd.read_csv('{}/flickPics_MIL.csv'.format(home))
holdDate = picTbl.unix_time.min()
x=1
pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                               page=x, max_upload_date=holdDate)
pages = pics.info['pages']
for x in range(1,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', 
                                   page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl = pics2table(pics)
    if len(addTbl) == 0:
        print 'broken'
        holdDate = picTbl.unix_time.min()
        break
    picTbl = pd.concat([picTbl, addTbl])
    picTbl.to_csv('{}/flickPics_MIL.csv'.format(home), index=False)