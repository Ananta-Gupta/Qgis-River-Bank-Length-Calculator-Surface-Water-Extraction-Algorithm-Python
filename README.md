# Qgis- River Bank Length Calcutalor & Surface Water Extraction Algorithm (Python)

## Index:
	a) Working
	b) Pre-Required
	c) Steps for calculating River Bank Lengths
	d) Steps for extracting Surface Water

## Working:
	1st algorithm is use for calculating the distance between the river banks, distance till the flood line.
	2nd algorithm is use for extracting surface water from the landsat-8 images.

## Pre-Required
	Software:
		QGIS 3.xx or above.
		Python 2.x or above.
	
	Python Libraries/Packages*:
		1. Numpy
		2. GDAL**
		3. pyshp
		4. Shapely
		5. Fiona**
		6. geopy
		7. pyproj
		8. geopandas

	*Note: These python libraries have to be installed in order as mentained above. All libraries are interdependent to each other.
	**if an error occure while installing from python comand line, download them manually from "https://www.lfd.uci.edu/~gohlke/pythonlibs/".
	Only download the version compatible to your python version and python version bit (i.e. 32 or 64).
	
	To check python version details use
		$> python
<img width="647" alt="Python Version" src="https://user-images.githubusercontent.com/58319462/99643966-5a541e80-2a73-11eb-8d37-abf02b960901.PNG">

	To Download Python Package
<img width="551" alt="Package Version" src="https://user-images.githubusercontent.com/58319462/99643981-5d4f0f00-2a73-11eb-934c-68ef6110712b.PNG">


(1st Algorithm)
## Steps to calculating River Bank Length perfectly:
	1. Create and empty output folder in your working directory.
	2. Choose any one method to proceed with the algorithm.
	   (If choose method I, run 'ReferenceLineGenerator.py’ python script.)
			 		 or
	   (If choose method II, draw a refence line on the canvas, save the shp file with 'referenceLine.shp’ name.)
	3. Use QChanage plugin to generate equidistant point on the reference line.
	4. Save the QChanage file to output folder with 'chain_refLine.shp’ name.
	5. Run 'DistenceCalculator.py’ python script for calculating the distance.
	   (read the comments properly. Change the path as mentioned in the comments.)
	6. Algorithm finish.
### Method I – (taking Bridge as a refence line)
	1. Generate start and end coordinates of the bridge and store then in a csv file.
  	2. Run 'ReferenceLineGenerator.py’ python script to generate a reference line perpendicular to the bridge.
  	3. Use QChanage plugin for generating equidistance points on the reference line.
  	4. Run 'DistenceCalculator.py’ python script to calculate the river bank length.
### Method II – (drawing own reference line)
  	1. Draw a reference line on the canvas parallel to the river water flow.
  	2. Use QChanage plugin for generating equidistant points on the reference line.
  	3. Run 'DistenceCalculator.py’ python script to calculate the river bank length. 

(2nd Algorithm)
## Steps for extracting Surface Water from the Landsat-8 image:
### Method I – (using Python script)
	1. Run 'ReflectanceGenerator.py' python script.
  	2. Set the paths.
  	3. Run 'SurfaceWaterExtraction.py' python script to generate surface water.
  	4. (optional) Change the colours of the NDWI layer.
### Method II – (using Raster Calculator)
  	1. Open Raster Calculator.
  	2. Calculate Reflectance of the require band layer.
  	3. Calculate NDWI from the Reflectance layer.
  	4. Calculate surface water from NDWI layer.
  	5. (optional) Change the colours of the NDWI layer.
  		(all formulas are given below)

## Formulas:
	Reflectance: -
		((0.0000200 * Landsat8_Band_no) + (-0.100)) / Cos(21.732483) * (3.141592 / 180)
		(only for Landsat-8 Data)
  	NDWI: -
    	(Green - NIR) / (Green + NIR)
		(for surface water)
  	Surface Water: -
    	NDWI > 0
