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

key = '08efe8fb64319b6dec58512d23408004'
secret = '07b1081fb8daed0f'
flickr_api.set_keys(api_key = key, api_secret = secret)
# add a way to dynamically call this file into the script
flickr_api.auth.AuthHandler.load('C:/Users/Rdebbout/Desktop/flickr_api_auth.txt')

# set bounding x,y values - DULUTH
minX = -92.335981
minY = 46.630695
maxX = -91.946101
maxY = 46.804721
box = '%s,%s,%s,%s' % (minX,minY,maxX,maxY)

cols = ['latitude', 'longitude', 'picID', 'date', 'time', 'username', 'title', 'url']
pics = flickr_api.Photo.search(bbox=box, format='parsed-json')
pages = pics.info['pages']
holdDate = flickr_api.Photo.getInfo(pics[0])['posted'] # this is assuming that the first record returned is the most recent
gotten = []
# date and time are recorded from the time and date that they were taken, 
# not the date that they were posted necessarily

def pics2table(flickrList, hDate):
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
pics = flickr_api.Photo.search(bbox=box, format='parsed-json', page=x, max_upload_date=holdDate) 
picTbl, holdDate = pics2table(pics, tbl, holdDate)
##############################################################################################
# first loop through all of the original returns retaining the holdDate as the minimum to pas to next loop
picTbl = pd.DataFrame()
for x in range(1,pages+1):
    pics = flickr_api.Photo.search(bbox=box, format='parsed-json', page=x, max_upload_date=holdDate)
    print 'Page: %s' % x
    addTbl, nextDate = pics2table(pics, holdDate)
    if len(addTbl) == 0:
        holdDate = nextDate
        break
    picTbl = pd.concat([picTbl, addTbl])
    kDate = nextDate
    picTbl.to_csv('D:/Projects/Panoramio/flickPics_test2.csv', index=False)
    
    
chk2 = []    
for f in pics:
    chk2.append(f['id'])
    
for x in chk:
    if x not in chk2:
        print x
##############################################################################################
   
#len(pd.unique(picTbl.picID.tolist()))
#new = picTbl.drop_duplicates('picID')
#a = flickr_api.auth.AuthHandler() #creates the AuthHandler object
#perms = "read" # set the required permissions
#url = a.get_authorization_url(perms)
#webbrowser.open_new_tab(url)
##set from the <oauth_verifier> tag 
#a.set_verifier('1412deda6763fddc')
#a.save('C:/Users/Rdebbout/Desktop/flickr_api_auth.txt')
##pics = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, radius=1, format='parsed-json')
#out = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, radius=1, format='parsed-json', page=24) 
#out2 = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, accuracy=16, format='json')
#t = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%H:%M:%S')