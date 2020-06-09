import cv2
import matplotlib
matplotlib.use('Qt5Agg') # Prevent MAC from crashing using this backend
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def show_image(image, title='No Title', cvTwo=True, bit=8):
    '''
    To show image using matplotlib
    Using Qt5Agg backend to prevent MAC from crashing
    Image - Standard uint8/16 array
    Title - Figure title as string
    cvTwo - cv2 reads images as BGR, thus giving incorrect colour. Default = True, which converts BGR to RGB
    '''
    
    # Check if image is color of grayscale
    # Seek for length of the array shape
    # If length = 3, image is 3D array/color image
    # If length = 2, image is 2D array/grayscale image
    foo = len(image.shape) 
    
    # Check bit depth and set pixel value max limit for displaying gray image
    if image.dtype == 'uint8':
        pvmax = 255
    else:
        pvmax = 2**16-1
    
    plt.figure()
    if foo == 2:
        plt.imshow(image, cmap=cm.gray, vmin=0, vmax=pvmax)
        plt.title(title)
        plt.show()
    else:
        if cvTwo == True:
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title(title)
            plt.show()   
        else:
            plt.imshow(image)
            plt.title(title)
            plt.show()
        
def color2gray(image, bgr=True):
    '''
    Convert color image to grayscale image
    Image - Standard uint8/16 array
    bgr=True; cv2 reads an image with channels in BGR order, default is BGR
    bgr=False; Specify this, if the image channels are in RGB order
    '''
    if bgr==True:
        im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        im = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return im

def normalize_image (image):
    '''
    Parameters
    ----------
    image : uint8 or uint16 image as numpy.ndarray

    Returns
    -------
    im : Normalized array of type float in 0 - 1 range
    '''
    if image.dtype != 'uint8' and image.dtype != 'uint16':
        print('Image is not of type uint8 nor uint16. Please check.')
        return None
    if image.dtype == 'uint8':
        im = image/255
    else:
        im = image/(2**16-1)
    return im


    
def show_im(image, title='No Title', cvTwo=True, bit=8):
    '''
    To show image using matplotlib
    Using Qt5Agg backend to prevent MAC from crashing
    Image - Standard uint8/16 array
    Title - Figure title as string
    cvTwo - cv2 reads images as BGR, thus giving incorrect colour. Default = True, which converts BGR to RGB
    '''
    
    # Check if image is color of grayscale
    # Seek for length of the array shape
    # If length = 3, image is 3D array/color image
    # If length = 2, image is 2D array/grayscale image
    foo = len(image.shape) 
    
    # Check bit depth and set pixel value max limit for displaying gray image
    if image.dtype == 'uint8':
        pvmax = 255
    else:
        pvmax = 2**16-1
    
    plt.figure()
    if foo == 2:
        plt.imshow(image, cmap=cm.gray, vmin=0, vmax=pvmax)
        plt.title(title)
        plt.show()
    else:
        if cvTwo == True:
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title(title)
            plt.show()   
        else:
            plt.imshow(image)
            plt.title(title)
            plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    