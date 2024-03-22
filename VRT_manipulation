from osgeo import gdal

# Replace these with your values
large_raster_filename = 'large_file.tif'
subset_extent = (easting_min, northing_min, easting_max, northing_max)
nodata_value = 99

# Open the large raster
large_raster = gdal.Open(large_raster_filename)

# Create the subset VRT (ds1) directly using the VRT driver
driver = gdal.GetDriverByName('VRT')
subset_vrt = driver.Create('', large_raster.RasterXSize, large_raster.RasterYSize, 1)
subset_vrt.SetGeoTransform(large_raster.GetGeoTransform())

# Set VRT parameters for the subset
band = subset_vrt.GetRasterBand(1)
band.SetMetadata({'source_0': large_raster_filename})  # Set source filename
band.SetMetadataItem('source_1', str(1), 'Band')  # Set source band
band.SetMetadataItem('Subset', 'YES')
subset_vrt.SetMetadataItem('PixelFunctionType', 'complex')
subset_vrt.SetMetadata({'SimpleSource': '<SourceFilename relativeToVRT="1">%s</SourceFilename>' % large_raster_filename})
subset_vrt.SetMetadataItem('SourceRegion', "%d,%d,%d,%d" % (subset_extent[0], subset_extent[1], subset_extent[2], subset_extent[3]))

# ... (rest of the code remains the same)

