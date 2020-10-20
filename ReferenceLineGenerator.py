from qgis.core import *
import pandas as pd

# output path of reference line. do not change the fine name.
refLine = 'path/to/output_folder/referenceLine.shp'

# input path of bridge coordinates csv
bridge_csvFilePath = 'path/to/Bridge_Coordinate.csv'

# read bridge coordinate csv file
csvFile = pd.read_csv(bridge_csvFilePath)

# function for generating reference line
p1x = float(csvFile['xCoord'][0])
p1y = float(csvFile['yCoord'][0])
for l in range(len(csvFile)):
	pass
p2x = float(csvFile['xCoord'][l])
p2y = float(csvFile['yCoord'][l])

slope = float((p2y - p1y) / (p2x - p1x))

c = float(p1y - (slope * p1x))
p3y = float(csvFile['yCoord'][24] - 0.05)
p3x = float((p3y - c) / slope)

slope = float((p3y - p1y) / (p3x - p1x))
slope = float(-1/slope)

filePath = refLine

layerFields = QgsFields()
layerFields.append(QgsField('id', QVariant.Int))

writer = QgsVectorFileWriter(filePath, 'UTF-8', layerFields,\
QgsWkbTypes.LineString, QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

feat = QgsFeature()
x = p3x
y = p3y
c = float(y - (slope * x))
#up-stream
x1 = float(x - 0.05)
y1 = float((slope * x1) + c)

#down-stream
x2 = float(x + 0.02)
y2 = float((slope * x2) + c)

feat.setGeometry(QgsGeometry.fromPolyline([QgsPoint(x1,y1), QgsPoint(x2,y2)]))
feat.setAttributes([1])
writer.addFeature(feat)

# load the referenceLine.shp file on the canvas
iface.addVectorLayer(filePath, '', 'ogr')

# delete the csv writer
del(writer)