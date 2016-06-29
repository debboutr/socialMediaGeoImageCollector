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

# set bounding x,y values - DULUTH
minX = -92.335981
minY = 46.630695
maxX = -91.946101
maxY = 46.804721
box = '%s,%s,%s,%s' % (minX,minY,maxX,maxY)



cols = ['latitude', 'longitude', 'picID', 'date', 'time', 'username', 'title', 'url']


key = '08efe8fb64319b6dec58512d23408004'
secret = '07b1081fb8daed0f'
flickr_api.set_keys(api_key = key, api_secret = secret)

flickr_api.auth.AuthHandler.load('C:/Users/Rdebbout/Desktop/flickr_api_auth.txt')

#a = flickr_api.auth.AuthHandler() #creates the AuthHandler object
#perms = "read" # set the required permissions
#url = a.get_authorization_url(perms)
#webbrowser.open_new_tab(url)
##set from the <oauth_verifier> tag 
#a.set_verifier('1412deda6763fddc')
#a.save('C:/Users/Rdebbout/Desktop/flickr_api_auth.txt')
##pics = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, radius=1, format='parsed-json')


pics = flickr_api.Photo.search(bbox=box, format='parsed-json')
pages = pics.info['pages']
holdDate = flickr_api.Photo.getInfo(pics[0])['posted'] # this is assuming that the first record returned is the most recent
gotten = new.picID.tolist()
# date and time are recorded from the time and date that they were taken, 
# not the date that they were posted necessarily

def pics2table(flickrList, tbl, hDate):
    tbl = pd.DataFrame()
    count = 0
    for f in flickrList:
        picID = smart_str(f['id'])
        if not picID in gotten:
            info = flickr_api.Photo.getInfo(f)
            minDate = info['posted']
            if hDate > minDate:
                hDate = minDate
            latitude = smart_str(info['location']['latitude'])
            longitude = smart_str(info['location']['longitude'])        
            title = smart_str(f['title'])
            print f['owner']
            #userid = smart_str(f['owner']['id'])
            username = smart_str(f['owner']['username'])
            url = smart_str(f.getPhotoFile('Medium'))
            date = smart_str(info['taken'].split(' ')[0])
            t = smart_str(info['taken'].split(' ')[1])
            tbl = tbl.append(pd.DataFrame([[latitude, longitude, picID, date, t, username, title, url]], columns=cols), ignore_index=True)
            gotten.append(picID)            
            print count
            count += 1   
    return tbl, hDate
 
picTbl, holdDate = pics2table(pics, tbl, holdDate)
##############################################################################################
# first loop through all of the original returns retaining the holdDate as the minimum to pas to next loop
for x in range(2,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl, holdDate = pics2table(pics, tbl, holdDate)
    if len(addTbl) == 0:
        break
    picTbl = pd.concat([picTbl, addTbl])
    picTbl.to_csv('D:/Projects/Panoramio/flickPics_test2.csv', index=False)
    
    
chk2 = []    
for f in pics:
    chk2.append(f['id'])
    
for x in chk:
    if x not in chk2:
        print x
##############################################################################################
    pics = flickr_api.Photo.search(bbox='%s,%s,%s,%s' % (minX,minY,maxX,maxY), format='parsed-json', max_upload_date=holdDate)
    
    
for f in pics:
    info = flickr_api.Photo.getInfo(f)
    tags = []        
    for tag in info['tags']:      
        tags.append(tag['text'])
    print str(tags)
##############################################################################################   
count = 0
                date = dt.fromtimestamp(info['posted']).strftime('%Y-%m-%d')
                t = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%H:%M:%S')
    #f['title']
    print f['id']
    count+=1
    f['owner']
    raw = f.getExif()[19]['raw']
    date = raw.split(' ')[0]
    time = raw.split(' ')[1]
    print f.getPhotoFile('Medium')
    
flickr_api.Photo.getInfo(f)    

out = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, radius=1, format='parsed-json', page=24)
  
out2 = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, accuracy=16, format='json')
tbl = pd.read_csv('D:/Projects/Panoramio/flickPics_test1.csv')
b = pd.read_csv('L:/Priv/CORFiles/Geospatial_Library/Data/Project/StreamCat/NRSA13_14_FinalTables/NRSA13_14_Landscape_Metrics.csv')

b.columns[:6]
b.columns[6:].sort_values()

len(pd.unique(picTbl.picID.tolist()))
new = picTbl.ix[picTbl.picID.isin(pd.unique(picTbl.picID.tolist()))]
new = picTbl.drop_duplicates('picID')
new.to_csv('D:/Projects/Panoramio/flickPics_test1.csv', index=False)
picID in new.picID.values
new = pd.concat([new, tbl])

new['date'].min()


addTbl = tbl.copy()

picTbl = new.copy()
import time
minDate = int(time.time())
info['posted'] < minDate

dt.now()

dt.utcnow()

dt.today()
time.gmtime()
dt.utcfromtimestamp(time.time())
