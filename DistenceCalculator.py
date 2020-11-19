import geopandas as gpd
import csv
import pandas as pd
import numpy as np
from qgis.core import QgsVectorFileWriter

# change the file name as per user requirements
floodLinePath = 'path/to/flood_line.shp'
riverBankPath = 'path/to/river_bank.shp'
outputCsvPath = 'path/to/output_folder/river_bank.csv'

# do not change the name of the file.
# provide the path to the empty folder
chain_RefrenceLinePath = 'path/to/output_folder/chain_refLine.shp'
perpendicularsPath = 'path/to/output_folder/perpendiculars.shp'
riverIntersectionWithGeo = 'path/to/output_folder/RiverIntersectionWithGeo.shp'
floodIntersectionWithGeo = 'path/to/output_folder/FloodIntersectionWithGeo.shp'
csvFilepath = 'path/to/output_folder/Coords.csv'

# extra files (delete automaticly when algorithm finishs)
exFiles = []
chain_RefrenceLine1Path = 'path/to/output_folder/chain_refLine1.shp'
riverIntersectionWithNoGeoPath = 'path/to/output_folder/RiverIntersectionWithNoGeo.shp'
floodIntersectionWithNoGeoPath = 'path/to/output_folder/FloodIntersectionWithNoGeo.shp'
# add files to the list you want to delete after finish
exFiles.append(chain_RefrenceLine1Path)
exFiles.append(riverIntersectionWithNoGeoPath)
exFiles.append(floodIntersectionWithNoGeoPath)

#------------------------------------------------------------------------------------------------------------------
# create XY on ref line

processing.run('qgis:exportaddgeometrycolumns',\
{'INPUT': chain_RefrenceLinePath,\
'CALC_METHOD':1,\
'OUTPUT': chain_RefrenceLine1Path})

print("Generating Reference Line geo coordinates...")
#------------------------------------------------------------------------------------------------------------------
# create CSV of ref line XY Coords

filePath = chain_RefrenceLine1Path
data = gpd.read_file(filePath)

coord = []
for d in range(len(data)):
    x = data['xcoord'][d]
    y = data['ycoord'][d]
    coord.append([x, y])
    # print(d, coord[d])

filePath = csvFilepath
file = open(filePath, "w+", newline='')
header = ['x', 'y']

with file:
    write = csv.writer(file, delimiter=',')
    write.writerow(header)
    write.writerows(coord)

print("Geo coordinates for the reference line are stored in '",csvFilepath,"'")

#------------------------------------------------------------------------------------------------------------------
# Plot perpendicular lines on the ref line

print("Plotting perpendicular lines...")

csvFile = pd.read_csv(csvFilepath)
filePath = perpendicularsPath

layerFields = QgsFields()
layerFields.append(QgsField('id', QVariant.Int))
layerFields.append(QgsField('x1coord', QVariant.Double))
layerFields.append(QgsField('y1coord', QVariant.Double))
layerFields.append(QgsField('x2coord', QVariant.Double))
layerFields.append(QgsField('y2coord', QVariant.Double))

writer = QgsVectorFileWriter(filePath, 'UTF-8', layerFields,\
QgsWkbTypes.LineString, QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

startX = float(csvFile['x'][0])
startY = float(csvFile['y'][0])
for l in range(len(csvFile)):
    pass
endX = float(csvFile['x'][l])
endY = float(csvFile['y'][l])

slope = float((endY - startY) / (endX - startX))
slope = float(-1 / slope)

feat = QgsFeature()
indx = 1
for data in range(len(csvFile)):
    x = float(csvFile['x'][data])
    y = float(csvFile['y'][data])
    c = float(y - (slope * x))
    x2 = float(x + 0.1)
    y2 = float((slope * x2) + c)
    feat.setGeometry(QgsGeometry.fromPolyline([QgsPoint(x,y), QgsPoint(x2,y2)]))
    feat.setAttributes([indx, x, y, x2, y2])
    writer.addFeature(feat)
    indx += 1

iface.addVectorLayer(filePath, '', 'ogr')

del(writer)

print("Perpendicular lines plotted.")

#------------------------------------------------------------------------------------------------------------------
# create intersection points on perpendicular lines

print("Generating intersection on the perpendicular line...")

processing.run("qgis:lineintersections",\
{'INPUT':perpendicularsPath,\
'INTERSECT':riverBankPath,\
'OUTPUT':riverIntersectionWithNoGeoPath})

processing.run("qgis:lineintersections",\
{'INPUT':perpendicularsPath,\
'INTERSECT':floodLinePath,\
'OUTPUT':floodIntersectionWithNoGeoPath})

processing.run('qgis:exportaddgeometrycolumns',\
{'INPUT':riverIntersectionWithNoGeoPath,\
'CALC_METHOD':1,\
'OUTPUT':riverIntersectionWithGeo })

processing.run('qgis:exportaddgeometrycolumns',\
{'INPUT':floodIntersectionWithNoGeoPath,\
'CALC_METHOD':1,\
'OUTPUT':floodIntersectionWithGeo })

iface.addVectorLayer(riverIntersectionWithGeo, '', 'ogr')
iface.addVectorLayer(floodIntersectionWithGeo, '', 'ogr')

print("Intersections created.")

#------------------------------------------------------------------------------------------------------------------
# deleting extra files

print("Delecting Extra file...")

for path in exFiles:
    print("deleting",path,"...")
    QgsVectorFileWriter.deleteShapeFile(path)

print("Extra files deleted.")

#------------------------------------------------------------------------------------------------------------------
# Calculating distances

print("Calculating distance...")

riverLayer = QgsProject.instance().mapLayersByName('RiverIntersectionWithGeo')
floodLayer = QgsProject.instance().mapLayersByName('FloodIntersectionWithGeo')

#print(lyr)

rRightBorder = []
rLeftBorder = []
flag = 0
for feat in riverLayer[0].getFeatures():
#    print(feat['id'], feat['Name'], feat['xcoord'], feat['ycoord'])
    indx = feat['id']
    x = float(feat['xcoord'])
    y = float(feat['ycoord'])
#    point = QgsPoint(x,y)
    if flag == 0:
        rLeftBorder.append([indx,x,y])
        flag = 1
    elif flag == 1:
        rRightBorder.append([indx,x,y])
        flag = 0

floodBorder = []
for feat in floodLayer[0].getFeatures():
#    print(feat['id'], feat['Name'], feat['xcoord'], feat['ycoord'])
    indx = feat['id']
    x = float(feat['xcoord'])
    y = float(feat['ycoord'])
    floodBorder.append([indx,x,y])
#print("#############################################")

disData = []
lineNo = 1
for data in range(len(rRightBorder)):
    p4 = QgsPointXY(floodBorder[data][1],floodBorder[data][2])
    p3 = QgsPointXY(rRightBorder[data][1],rRightBorder[data][2])
    p2 = QgsPointXY(rLeftBorder[data][1],rLeftBorder[data][2])
    p1 = QgsPointXY(coord[data][0],coord[data][1])

    distance = QgsDistanceArea()
    crs = QgsCoordinateReferenceSystem()
    crs.createFromSrsId(4326)
    distance.sourceCrs()
    #distance.setEllipsoidalMode(True)
    distance.setEllipsoid('WGS84')
    l1 = distance.measureLine(p2,p1)
    l2 = distance.measureLine(p3,p1)
    l3 = distance.measureLine(p4,p1)

    disData.append([lineNo, l1, l2, l3])
    lineNo += 1
    print("Line",rRightBorder[data][0], "Distance --> {:.2f}".format(l1), "m, ",\
    "{:.2f}".format(l2), "m, ",\
    "{:.2f}".format(l3), "m")

print("Distance Calculated.")

#------------------------------------------------------------------------------------------------------------------
#Final Output to CSV

print("Generating output csv...")

file = open(outputCsvPath, "w+", newline='')
header = ['Line Number',\
'Reference Line to Right Border(in meter)',\
'Reference Line to Left Border(in meter)',\
'Reference Line to Flood Line(in meter)']

with file:
    write = csv.writer(file, delimiter=',')
    write.writerow(header)
    write.writerows(disData)

print("CSV generated. Path -->",outputCsvPath)