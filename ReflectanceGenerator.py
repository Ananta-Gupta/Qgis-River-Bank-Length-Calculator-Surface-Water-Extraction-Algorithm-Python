band = QgsRasterLayer('path/to/Landsat-8_Band.tif')
output = 'path/to/output_folder/output.tif'

entries = []
ras = QgsRasterCalculatorEntry()
ras.ref = 'ras@1'
ras.raster = band
ras.bandNumber = 1
entries.append(ras)

formula = '((0.0000200 * ras@1) + (-0.100)) / Cos(21.732483) * (3.141592 / 180)'
calc = QgsRasterCalculator(formula , output, 'GTiff',\
band.extent(), band.width(), band.height(), entries)

calc.processCalculation()