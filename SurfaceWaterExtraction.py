red = QgsRasterLayer('path/to/red_band.tif')
NIR = QgsRasterLayer('path/to/NIR_band.tif')
output = 'path/to/output_folder/NDWI.tif'

entries = []
ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@1'
ras.raster = red
ras.bandNumber = 1
entries.append(ras)

ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@2'
ras.raster = NIR
ras.bandNumber = 1
entries.append(ras)

formula = '(ras@1 - ras@2) / (ras@1 + ras@2)'
calc = QgsRasterCalculator(formula , output, 'GTiff',\
red.extent(), red.width(), red.height(), entries)

calc.processCalculation()

NDWI = QgsRasterLayer(output)
output2 = 'path/to/output_folder/Surface_Water.tif'

ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@1'
ras.raster = NDWI
ras.bandNumber = 1
entries.append(ras)

formula = 'ras@1 > 0'
calc = QgsRasterCalculator(formula , output2, 'GTiff',\
NDWI.extent(), NDWI.width(), NDWI.height(), entries)

calc.processCalculation()