import rasterio


# Open raster file
def open_raster(raster_file):
    return rasterio.open(raster_file)


# Save raster file
def save_raster(data, raster_file, width, height, transform):
    raster = rasterio.open(raster_file, 'w', driver='Gtiff',
                           width=width, height=height,
                           count=1,
                           transform=transform,
                           dtype='float64')
    raster.write(data, 1)
    raster.close()
