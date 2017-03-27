# socialMediaGeoImageCollector

### Collect social media photos and videos by location from flickr, instagram, and panaramio

These scripts search for public media within a given bounding box.

## Necessary Packages
* geopandas
* django
* requests
* pandas
* urllib2

_if collecting from flickr:_
* flickrapi

_flickr2.py uses a different python module, flickrapi, which can return a more complete dictionary and reduces the number of calls to Flickr, making the colection process faster._

![readme](https://cloud.githubusercontent.com/assets/7052993/24336890/1c29c2c0-124b-11e7-8d8a-41930e335320.png)

#### stripPict.py gets exif data using gdal for a point value from a picture
