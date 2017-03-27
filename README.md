# socialMediaGeoImageCollector

grab social media photos and videos by location 

stripPict gets exif data using gdal for a point value from a picture

the other scripts grab images off of either Instagram or Flickr within a bounding box

flickr2.py uses a different python module, flickrapi, which can return a more complete dictionary and reduces the number of calls to Flickr, making the colection process faster.

[readme.pdf](https://github.com/debboutr/socialMediaGeoImageCollector/files/871195/readme.pdf)



Traceback (most recent call last):

  File "<ipython-input-14-b2840fc0b2da>", line 4, in <module>
    data = getPhotoCount(url)

  File "<ipython-input-3-09804a657fd2>", line 4, in getPhotoCount
    urlResponse = urllib2.urlopen(url).read()

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 154, in urlopen
    return opener.open(url, data, timeout)

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 435, in open
    response = meth(req, response)

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 548, in http_response
    'http', request, response, code, msg, hdrs)

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 473, in error
    return self._call_chain(*args)

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 407, in _call_chain
    result = func(*args)

  File "C:\Users\Hank\Anaconda2\envs\dul\lib\urllib2.py", line 556, in http_error_default
    raise HTTPError(req.get_full_url(), code, msg, hdrs, fp)

HTTPError: -
