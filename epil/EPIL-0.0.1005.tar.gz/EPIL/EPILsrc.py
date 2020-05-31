import PIL
import PIL.ImageOps
import PIL.ImageFilter
import PIL.ImageDraw
import numpy

class WIM():

    '''
    ______________________________------------------------
    ______________________________|Thanks for using EPIL!|
    ______________________________------------------------
    ______________________________Convert image to RGBA!
    '''

    def __init__(self, image):

        '''
        WIM --- WorkwithIMages
        '''
        
        self.image = image
    
    def replace_color(self, color_from, color_to):
        
        # thanks for https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color ...

        data = numpy.array(self.image)
        red, green, blue, alpha = data.T

        white_areas = (red == color_from[0]) &\
                      (green == color_from[1]) &\
                      (blue == color_from[2])
        data[..., :-1][white_areas.T] = color_to

        self.image = PIL.Image.fromarray(data)

        # ... end of the thanks

    def invert_color(self):
        self.image = PIL.ImageOps.invert(self.image.convert('RGB')).convert('RGBA')
        
    def past_image(self, other, x, y):

        '''
        Other image is a WIM object!
        '''
        
        self.image.paste(other.image, (x, y), other.image)

    def resize_image(self, width, height):
        self.image = self.image.resize((width, height))

    def crop_image(self, x, y, width, height):
        self.image = self.image.crop((x, y, x + width, y + height))

    def quantize(self, quantize_to):
        self.image = self.image.quantize(quantize_to).convert('RGBA')

    def rotate(self, degree, flip_horizontal=False, flip_vertical=False):

        '''
        degree is 90 or 180 or 270
        '''
        
        if flip_horizontal:
            self.image = self.image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            self.image = self.image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        if degree == 90:
            self.image = self.image.transpose(PIL.Image.ROTATE_90)
        if degree == 180:
            self.image = self.image.transpose(PIL.Image.ROTATE_180)
        if degree == 270:
            self.image = self.image.transpose(PIL.Image.ROTATE_270)

    def gaussianBlur(self, radius):

        '''
        poor eyesight :)
        '''
        
        self.image = self.image.filter(PIL.ImageFilter.GaussianBlur(radius=radius))

    def relighting(self, relight):

        '''
        make image dark   (if relight < 0)
        make image bright (if relight > 0)
        '''
        
        data = []
        pixels = self.image.load()
        image = PIL.Image.new('RGBA', self.image.size)
        draw = PIL.ImageDraw.Draw(image)
        
        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                draw.point((x, y),
                          (pixels[x, y][0]+relight,
                           pixels[x, y][1]+relight,
                           pixels[x, y][2]+relight))

        self.image = image
        

    def return_image(self):
        return self.image
