##################################################################################
# Name: photoQuery.py
# Description: Gets photos from website and converts them to point shapefile
# Author: Rick Debbout
# Date: May, 28 2016
##################################################################################

# import dependencies
import urllib2,json
import numpy as np
import pandas as pd
from django.utils.encoding import smart_str
import time
from datetime import datetime as dt
#import geopandas as gpd
#from shapely.geometry import Point
##################################################################################
# VARIABLES

# set working directory
workingPath = '/media/rick/600ABCCF0ABCA386/Users/rick/Documents/instripTrick/ouput'

# set ouput file path/name
outFileName = workingPath + '/outputFromScript_MIL.csv'

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
km = 0.0056144625  # 0.625
dist = 625

#  0.0449157  # 5 km #       5000
#  0.02245785  # 2.5 km      2500
#  0.011228925  #1.25 km     1250
#  0.0056144625  # 0.625 km  625
#  0.00280723125 # 0.3125 km 313
##################################################################################
# FUNCTIONS  5 km spacing 0.04491265  0.0449157  div by 2 : 0.022456325
class getMedia(object):
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """
    def __init__(self, name, balance=0.0):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.name = name
        self.balance = balance

    def withdraw(self, amount):
        """Return the balance remaining after withdrawing *amount*
        dollars."""
        if amount > self.balance:
            raise RuntimeError('Amount greater than available balance.')
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        """Return the balance remaining after depositing *amount*
        dollars."""
        self.balance += amount
        return self.balance
    
def getPhotoCount(url):
    # query website, parse JSON, and return photo count
    urlResponse = urllib2.urlopen(url).read()
    parsedResponse = json.loads(urlResponse)
    queryCount = parsedResponse['data']
#    print 'Query count returned: ' + str(len(queryCount))
    return queryCount
  
klip = [] 
recirc = []
cols = ['latitude', 'longitude', 'unique_ID', 'date', 'time', 'username', 'title', 'tags', 'url', 'video']
tbl = pd.DataFrame()
token = '1771051239.ab103e5.7e013b99ce924cb7a894ecd0dd030be5'
count = 0
print 'Phase 1: '
print '# of reads : %s' % str(len(np.arange(minX, maxX, km)) * len(np.arange(minY, maxY, km)))
for xcoord in np.arange(minX, maxX, km):
    for ycoord in np.arange(minY, maxY, km):
        url = 'https://api.instagram.com/v1/media/search?lat=%s&lng=%s&distance=%s&access_token=%s&callback=?&count=500' % (ycoord, xcoord, dist, token)  # &callback=?&count=500
        try:    
            data = getPhotoCount(url)
        except urllib2.HTTPError:
            time.sleep(20)        
            data = getPhotoCount(url)
            print len(tbl)
        count += 1
        print count
        if len(data) == 100:
            print 'X: %s Y: %s has %s returns.' % (xcoord, ycoord, str(len(data)))
        if type(data) is list:
            for loc in range(len(data)):
                chk = data[loc]['id']
                if chk not in klip:
                    if data[loc].has_key('location') and data[loc]['location'].has_key('id'):
                        ID = data[loc]['location']['id']
                    else:
                        continue
                    if ID not in recirc:                
                        recirc.append(ID)
                    date = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%Y-%m-%d')
                    t = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%H:%M:%S')
                    latitude = data[loc]['location']['latitude']
                    longitude = data[loc]['location']['longitude']
                    title = smart_str(data[loc]['location']['name'])
                    video = 'N'
                    if 'videos' in data[loc]:
                        url = data[loc]['videos']['standard_resolution']['url']
                        video = 'Y'
                    else:    
                        url = smart_str(data[loc]['images']['standard_resolution']['url'])
                    username = smart_str(data[loc]['user']['username'])
                    tags = smart_str(", ".join(data[0]['tags']))
                    tbl = tbl.append(pd.DataFrame([[latitude, longitude, chk, date, t, username, title, tags, url, video]], columns=cols), ignore_index=True)
                    klip.append(chk)
                    video = 'N'
        else:
            continue
print 'Recirc: %s' % str(len(recirc))
tbl2 = pd.DataFrame()
print 'Phase 2: '
count = 0
for rec in recirc:
    url = 'https://api.instagram.com/v1/locations/%s/media/recent?access_token=%s&count=500' % (rec, token)
    try:    
        data = getPhotoCount(url)
    except urllib2.HTTPError:
        time.sleep(20)        
        data = getPhotoCount(url)
    count += 1
    print count
    if type(data) is list:
        for loc in range(len(data)):
            chk = data[loc]['id']
            if chk not in klip: 
                if data[loc].has_key('location') and data[loc]['location'].has_key('id'):
                    ID = data[loc]['location']['id']
                else:
                    continue
                date = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%Y-%m-%d')
                t = dt.fromtimestamp(int(data[loc]['created_time'])).strftime('%H:%M:%S')
                latitude = data[loc]['location']['latitude']
                longitude = data[loc]['location']['longitude']
                title = smart_str(data[loc]['location']['name'])
                video = 'N'
                if 'videos' in data[loc]:
                    url = data[loc]['videos']['standard_resolution']['url']
                    video = 'Y'
                else:    
                    url = smart_str(data[loc]['images']['standard_resolution']['url'])
                username = smart_str(data[loc]['user']['username'])
                tags = smart_str(", ".join(data[0]['tags']))
                tbl2 = tbl2.append(pd.DataFrame([[latitude, longitude, chk, date, t, username, title, tags, url, video]], columns=cols), ignore_index=True)
                klip.append(chk)
                video = 'N'
    else:
        continue
    
    
chktbl = pd.concat([tbl,tbl2])
            
chktbl.to_csv(outFileName, index=False)
print 'Recirc: %s' % str(len(recirc))
print len(tbl)
print len(tbl2)
print len(chktbl)
print outFileName
#crs = {u'datum': u'WGS84', u'no_defs': True, u'proj': u'longlat'}
#geometry = [Point(xy) for xy in zip(chktbl.longitude, chktbl.latitude)]
#geo_df = gpd.GeoDataFrame(chktbl, crs=crs, geometry=geometry)
#
#'%s.shp' % outFileName.split('.')[0]
#
#hop = tbl2.drop_duplicates('url')


#look = pd.read_csv('D:/Projects/Panoramio/outputFromScript.csv')
#
#len(look.url.unique())
