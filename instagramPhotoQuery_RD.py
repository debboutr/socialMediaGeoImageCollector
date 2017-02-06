##################################################################################
# Name: photoQuery.py
# Description: Gets photos from website and converts them to point shapefile
# Author: Rick Debbout
# Date: May, 28 2016
##################################################################################
# IMPORTANT Token website for authentication :  http://services.chrisriversdesign.com/instagram-token/
# import dependencies
import os
import urllib2,json
import numpy as np
import pandas as pd
from django.utils.encoding import smart_str
import time
from datetime import datetime as dt
import geopandas as gpd
from shapely.geometry import Point
#from Tkinter import *
from Tkinter import Tk,Label,Scrollbar,Listbox,Button,Y,RIGHT,END, W, IntVar, StringVar, Radiobutton
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory

# Tk().withdraw() -questionable
###############################################################################

def getPhotoCount(url):
    # query website, parse JSON, and return list of images
    try:
        urlResponse = urllib2.urlopen(url).read()
        parsedResponse = json.loads(urlResponse)
    except urllib2.HTTPError, err:
        if err.code == 429: 
            time.sleep(7200) # not enough time passes here
            urlResponse = urllib2.urlopen(url).read()
        if err.code == 502:
            time.sleep(20)
            urlResponse = urllib2.urlopen(url).read()
        else:
            raise
    except ValueError:
        return ()
    if 'data' in parsedResponse:
        queryCount = parsedResponse['data']
        return queryCount
    else:
        return ()

class getDist():
    def __init__(self, master):
        self.master=master
        self.startwindow()
        #self.b=0      # no need for this, directly store in the global variable

    def startwindow(self):

        self.var1 = IntVar()
        self.textvar = StringVar()

        self.Label1=Label(self.master, text="Search distance (meters)")
        self.Label1.grid(row=0, column=0)

        self.Label2=Label(self.master, textvariable=self.textvar)
        self.Label2.grid(row=2, column=0)

        self.rb1 = Radiobutton(self.master, text="5000", variable=self.var1,
                               value=5000, command=self.cb1select)
        self.rb1.grid(row=1, column=0, sticky=W)

        self.rb2 = Radiobutton(self.master, text="625", variable=self.var1,
                               value=625, command=self.cb1select)
        self.rb2.grid(row=1, column=1, sticky=W)

        self.rb3 = Radiobutton(self.master, text="160", variable=self.var1,
                               value=160, command=self.cb1select)
        self.rb3.grid(row=1, column=2, sticky=W)
        
        self.Button1=Button(self.master, text="ok", command=self.ButtonClick)
        self.Button1.grid(row=2, column=2)
    def ButtonClick(self):
        global dist
        dist = self.var1.get()
        self.master.quit()

    def cb1select(self):
        return self.var1.get()

if __name__ == '__main__':
    root=Tk()
    window=getDist(root)
    root.mainloop()
    print dist
    
    f = askopenfilename(title='Select the file with UID and SITE_ID (*.csv,*.dbf,*.shp)',initialdir=os.getcwd())
    bb = gpd.read_file(f)
    #bb = gpd.read_file('/home/rick/projects/ashtabula/bbox.shp')
    geoser = bb.geometry.bounds.ix[bb.index[0]]
    minX,minY,maxX,maxY = geoser
    print minX,minY,maxX,maxY
    print f.split('.')[0].split('/')[-1]
    path = askdirectory(title='Select directory where GRIDs are stored...',initialdir=os.getcwd())
    
    dvals = {5000:0.0449157,625:0.0056144625,160:0.001403615625}
    km = dvals[dist]
    
    # VARIABLES
    startTime = dt.now()
    # set working directory
    #workingPath = 'D:/Projects/Panoramio'
    path = '/home/rick/projects/ashtabula'
    # set ouput file path/name
    outFileName = path + '/ash_5000.csv'
    
    
    
      
    klip = []  # isolate only unique photoIDs and keep only those that haven't been retreived
    recirc = []  # keep location IDs and use to loop again by locationID to pick up more images
    # build the table to store data
    cols = ['latitude', 'longitude', 'unique_ID', 'date', 'time', 'username', 'title', 'tags', 'url', 'video']
    tbl = pd.DataFrame()
    # set token and loop through points throughout bounding box with overlapping serch radii
    token = '3644730954.e029fea.fb216a0714c643268268cacbfdba3f29' # gotten here: services.chrisriversdesign.com/instagram-token/
    count = 0
    print 'Phase 1: '
    print '# of reads : %s'  % str(len(np.arange(minX, maxX, km)) * len(np.arange(minY, maxY, km)))
    for xcoord in np.arange(minX, maxX, km):
        for ycoord in np.arange(minY, maxY, km):
            url = 'https://api.instagram.com/v1/media/search?lat=%s&lng=%s&distance=%s&access_token=%s&callback=?&count=500' % (ycoord, xcoord, dist, token)  # &callback=?&count=500
            data = getPhotoCount(url)
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
    # Initialize new table to loop by collected locationIDs
    print 'Recirc: %s' % str(len(recirc))
    tbl2 = pd.DataFrame()
    print 'Phase 2: '
    count = 0
    for rec in recirc:
        url = 'https://api.instagram.com/v1/locations/%s/media/recent?access_token=%s&count=500' % (rec, token)   
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
    # Concatenate the 2 tables from above, check that all IDs are unique, write to csv   
    chktbl = pd.concat([tbl,tbl2])
    r = chktbl.drop_duplicates('unique_ID')            
    #chktbl.to_csv(outFileName, index=False)
    # Take csv and convert to shapefile
    #chktbl = pd.read_csv(outFileName)
    crs = {u'datum': u'WGS84', u'no_defs': True, u'proj': u'longlat'}
    geometry = [Point(xy) for xy in zip(r.longitude, r.latitude)]
    geo_df = gpd.GeoDataFrame(r, crs=crs, geometry=geometry)
    geo_df.to_file(path + '/' + f.split('.')[0].split('/')[-1] + '_' + str(dist) + '.shp')
    print "elapsed time " + str(dt.now()-startTime)

##############################################################################
## set bounding x,y values - DULUTH
#minX = -92.335981
#minY = 46.630695
#maxX = -91.946101
#maxY = 46.804721
## set bounding x,y values - MILTOWN
#minX = -88.231662
#minY = 42.838153
#maxX = -87.789201
#maxY = 43.444837
## set bounding x,y values - Ashtabula
#minX = -80.9047045078156
#minY = 41.7975881835618
#maxX = -80.6410243157302
#maxY = 41.9532138083304
## set distance for search area and increments to move points through bbox -- 
## km set to estimated value of km in decimal degrees at the given latitude 
#km = 0.0056144625   
#dist = 625
##  0.0449157        # 5 km #        5000
##  0.02245785       # 2.5 km        2500
##  0.011228925      # 1.25 km       1250
##  0.0056144625     # 0.625 km      625
##  0.00280723125    # 0.3125 km     313
##  0.001403615625   # 0.15625 km    160
##############################################################################