import rasterio
import numpy
from scipy import ndimage


# Open raster file
def open_raster(raster_file):
    return rasterio.open(raster_file)


# Save raster file
def save_raster(data, raster_file, width, height, crs, transform):
    raster = rasterio.open(raster_file, 'w', driver='Gtiff',
                           width=width, height=height,
                           count=1,
                           crs=crs,
                           transform=transform,
                           dtype='float64')
    raster.write(data, 1)
    raster.close()


# Calculate NDVI
def ndvi(red, nir):
    return numpy.where(nir + red == 0.,
                       0,
                       (nir - red) / (nir + red))


# Apply sobel filter
def sobel(band):
    return ndimage.sobel(band)
