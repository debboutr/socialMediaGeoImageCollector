##################################################################################
# Name: panoramioPhotoQuery.py
# Description: Gets photos from panoramio website and converts them to 
# point shapefile
# arcpy REQUIRED!!! the other script in this repo can be used to 
# get around needing arcpy
#
# Author: Tad Larsen, edited by Jon Launspach
# Date: August, 10 2016
##################################################################################

# import dependencies
import urllib2,json,arcpy,datetime
##################################################################################
# VARIABLES

## Start time to see how long the process takes
startTime = datetime.datetime.now()

# Set working directory
workingPath = '' # Put in the directory where the script will store the output data.

# Set polygon shapefile
Sfile = '' # Put in the polygon grid that will be used to loop through and collect photos. Typically we used a 250 by 250 meter grid.

# Set search cursor
sCur = arcpy.SearchCursor(Sfile)

# Set variable count
j = 1

# Fetch each feature from the cursor and examine the extent properties
for row in sCur:
    try:
        geom = row.shape
        ext = geom.extent  # or row.Shape.extent
        #print ext.XMin,ext.YMin,ext.XMax,ext.YMax 

        minXa = ext.XMin
        minYa = ext.YMin
        maxXa = ext.XMax
        maxYa = ext.YMax

        # Output file 
        outFileName = workingPath + '/outputPhotoList_' + str(j)+ '.csv'
        
        # Set up panoramio query strings
        initialGET = 'http://www.panoramio.com/map/get_panoramas.php?set=full&from=0&to=100&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=false'%(minXa,minYa,maxXa,maxYa)
        stringGET_1 = 'http://www.panoramio.com/map/get_panoramas.php?set=full&from='
        stringGET_2 = '&to='
        stringGET_3 = '&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=false'%(minXa,minYa,maxXa,maxYa)

        # Output field name dictionary
        outFileHeaders = ['upload_date','owner_name','photo_id','longitude','height','width','photo_title','latitude','owner_url','photo_url','photo_file_url','owner_id']

        # Arcpy variables
        inTable = workingPath + '/outputPhotoList_' + str(j)+ '.csv'
        xCoords = 'longitude'
        yCoords = 'latitude'
        outLayer = 'pointLayer'
        savedLayer = workingPath + '/photoPoints_' + str(j)+ '.shp'
        spRef = "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"
             
        ##################################################################################
        # FUNCTIONS

        def getPhotoCount(url):
            # Query website, parse JSON, and return photo count
            urlResponse = urllib2.urlopen(url).read()
            parsedResponse = json.loads(urlResponse)
            queryCount = parsedResponse['count']
            return queryCount

        def getPhotos(url):
            # Query website, parse JSON into dictionary, and return photo dictionary
            print url
            urlResponse = urllib2.urlopen(url).read()
            parsedResponse = json.loads(urlResponse)
            photoDict = parsedResponse['photos']
            return photoDict
            
        def writeRecords(photoDictionary,outFile):
            for photo in photoDictionary:
                valueString = ''
                for key, value in sorted(photo.iteritems()):
                    if key in outFileHeaders:
                        try:
                            val = str(value)
                        except:
                            val = ''
                        valString = val.replace(',',';')
                        valueString = valueString + valString + ','
                valueString = valueString.rstrip(',')
                outFile.write(valueString + '\n')
                
        def importPoints():


            # Set directory overwrite
            arcpy.env.overwriteOutput = True
            
            # Make the XY event layer and save to shapefile...
            arcpy.MakeXYEventLayer_management(inTable, xCoords, yCoords, outLayer, spRef)
            arcpy.arcpy.CopyFeatures_management(outLayer, savedLayer)
           #if there is an exception print message.
    
        ##################################################################################
        # MAIN SCRIPT

        # Get the total number of photos in the bounding box
        photoCount = getPhotoCount(initialGET)
        print photoCount
        # Process first 100 photos
        photoDict = getPhotos(initialGET)
        fieldString = ''
        for header in sorted(outFileHeaders):
            fieldString = fieldString + header + ','
            
        fieldString = fieldString.rstrip(',')

        # Setup csv file
        outputFile = open(outFileName,'w')
        outputFile.write(fieldString + '\n')


        # Loop through photos; starting with the initialGET
        writeRecords(photoDict,outputFile)
        i = 100
        while i <= photoCount:
            getQueryString = stringGET_1 + str(i) + stringGET_2 + str(i + 100) + stringGET_3
            newPhotoDict = getPhotos(getQueryString)
            writeRecords(newPhotoDict,outputFile)
            i = i + 100

        j= j + 1             
        outputFile.close()

        importPoints()

    except Exception as e:
        print e.message
            
        # If using this code within a script tool, AddError can be used to return messages 
        #   back to a script tool.  If not, AddError will have no effect.
        arcpy.AddError(e.message)
        continue

## End time to see how long it took
endTime = datetime.datetime.now()

print ' -> Processing time: ' + str(endTime-startTime)    
