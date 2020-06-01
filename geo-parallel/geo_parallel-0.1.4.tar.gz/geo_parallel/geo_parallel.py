import rasterio


# Open raster file
def open_raster(raster_file):
    return rasterio.open(raster_file)