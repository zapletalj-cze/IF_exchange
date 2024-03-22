from osgeo import gdal
import geopandas as gpd
from tools import get_extent_vector, align_extent_to_snap
import sys

large_raster_filename = r'D:\157_CanadaFlood_v3\impervious_areas_5m\big_rasters\TEST.tif'
domain_test = r'D:\157_CanadaFlood_v3\impervious_areas_5m\small_area.gpkg'
snap_raster = r'\\euprafapp003\FLST01\01_Projects\157_Canada_Flood_v3\01_MD\01_HAZARD\00_GIS\01_SnapRaster\snap_raster_60.tif'
vrt_test = r'D:\157_CanadaFlood_v3\impervious_areas_5m\big_rasters\test.vrt'

extent = get_extent_vector(domain_test)
extent_snapped = align_extent_to_snap(extent, snap_raster, 5)
print(extent_snapped)
subset_extent = (extent_snapped[0], extent_snapped[2], extent_snapped[1], extent_snapped[3])
nodata_value = 99

# Open the large raster
large_raster = gdal.Open(large_raster_filename)

# Create the subset VRT (ds1) directly using the VRT driver
driver = gdal.GetDriverByName('VRT')
subset_vrt = driver.Create('', large_raster.RasterXSize, large_raster.RasterYSize, 1)
subset_vrt.SetGeoTransform(large_raster.GetGeoTransform())

# Set VRT parameters for the subset
band = subset_vrt.GetRasterBand(1)
band.SetMetadataItem('Subset', 'YES')
subset_vrt.SetMetadataItem('PixelFunctionType', 'complex')
subset_vrt.SetMetadata({'SimpleSource': '<SourceFilename relativeToVRT="1">%s</SourceFilename>' % large_raster_filename})
subset_vrt.SetMetadataItem('SourceRegion', "%d,%d,%d,%d" % (subset_extent[0], subset_extent[1], subset_extent[2], subset_extent[3]))

# Update target GeoTIFF (optional, can be the same as large_raster_filename)
target_filename = 'updated_large_file.tif'

# Copy VRT data to target GeoTIFF
driver = gdal.GetDriverByName('GTiff')
driver.CopyDataset(ds2_vrt, target_filename)

# Close datasets
ds1 = None
ds2_vrt = None

