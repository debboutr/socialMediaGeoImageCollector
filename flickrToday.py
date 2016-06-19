# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:09:26 2016

@author: Rdebbout
"""

import flickrapi

api_key = '08efe8fb64319b6dec58512d23408004'

api_secret = '07b1081fb8daed0f'
flickr = flickrapi.FlickrAPI(api_key, api_secret)
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
photos = flickr.photos.geo.photosForLocation(lat=44.563594,lon=-123.2642559)
flickr.token_valid()
flickr.test.login()
flickr.token.path
flickr.get_access_token(flickr.get_request_token())
if not flickr.token_valid(perms='read'):
    print 'coming'
    flickr.get_request_token(oauth_callback='oob')
    authorize_url = flickr.auth_url(perms='read')
    webbrowser.open_new_tab(authorize_url)
    verifier = unicode(raw_input('Verifier code: '))
    flickr.get_access_token(verifier)

    
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
sets   = flickr.photosets.getList(user_id='73509078@N00')

sets   = flickr.photos.geo.photosForLocation(lat=44.563594,lon=-123.2642559)


title  = sets['photosets']['photoset'][0]['title']['_content']

print('First set title: %s' % title)


45.527116, -122.667783

flickr.authenticate_via_browser(perms='read')

import webbrowser
webbrowser.open_new_tab(url)
verifier = unicode('576903713')
flickr.get_access_token(verifier)
resp = flickr.photos.getInfo(photo_id='7658567128')
type(verifier)


################################################################################
import flickr_api
import webbrowser

key = '08efe8fb64319b6dec58512d23408004'
secret = '07b1081fb8daed0f'

flickr_api.set_keys(api_key = key, api_secret = secret)

a = flickr_api.auth.AuthHandler() #creates the AuthHandler object
perms = "read" # set the required permissions
url = a.get_authorization_url(perms)
webbrowser.open_new_tab(url)
#set from the <oauth_verifier> tag 
a.set_verifier('e0e10f4a9a90e349')
user = flickr_api.set_auth_handler(a)
out = flickr_api.Photo.photosForLocation(lat=46.789748,lon=-92.101478)
out = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, accuracy=11, format='parsed-json')
for f in out:
    f['title']
    f['id']
    raw = f.getExif()[19]['raw']
    date = raw.split(' ')[0]
    time = raw.split(' ')[1]
    print f.getPhotoFile('Medium')
    
a.save('C:/Users/Rdebbout/Desktop/flickr_api_auth.txt')

out2 = flickr_api.Photo.search(lat=46.789748, lon=-92.101478, accuracy=16, format='json')
g = out2[0]
f = out[0]
type(g)
g['title']
type(f)
f['id']
f['']
f.getInfo
f['title']
f['location']['latitude']
f['location']['longitude']
raw = f.getExif()[19]['raw']
date = raw.split(' ')[0]
time = raw.split(' ')[1]
f.getLocation
f.getPageUrl()
f.getPhotoUrl()
f.getPhotoFile('Medium')
count = 0
for f in out2:
    print f['id']
    print f['title']
    count += 1

f['location']    
f

h = out[1]
g.show()
out.count
beef.index

user = flickr_api.Person.findByUserName('~rickyD')



flickr_api.test.login()




latitude	longitude	unique_ID	date	time	username	title	tags	url	video



