import ipywidgets as widgets
import os
import natsort 
from IPython.display import Image

class jupyslides:

  def __init__(self, 
               slides_path,
               default_width=720,
               height_to_width_ratio=810/1080):

    """
    Initiate the jupyslides object with the path to the ppt images.
    An image needs to be labeled with a number to indicate its order
    in the entire slides

    Params:
      slides_path : the path to the ppt slides folder

      default_width : the default width of the slide

      height_to_width_ratio : the ratio between height and width of the 
        slide, namely, ratio = height / width

    return:
      None
    """

    self._default_width = default_width
    self._default_height = default_width*height_to_width_ratio # default height
    self._slides = self._read_slides(slides_path) # read and keep the slides 

  def _read_slides(self, slides_path):

    """
    Read the slides in image format from the path to the folder that keeps 
    the slide images 

    Params:
      slides_path : the path to the ppt slides folder

    Return:
      slides : a list of slides that is stored as an Image object
        with the pre-defined width and height 
    """

    # filter the slide name which has a number in it to indicate its order 
    # in the folder 
    slide_names = [sn for sn in os.listdir(slides_path) if any(map(str.isdigit, sn))]

    try:
      # sort out the slide names based on the number to make sure the images
      # are displayed in sequence
      slide_names_sorted = natsort.natsorted(slide_names, reverse=False)
    except ValueError as e:
      print(f'Error: {e}, please make sure the images have numbers to indicate the order')
      raise

    # construct a list of slide images 
    slides = [Image(filename=f'{slides_path}/{slide_name}', 
                    width=self._default_width,
                    height=self._default_height) \
              for slide_name in slide_names_sorted]

    return slides 

  def _current_slide(self,
                     zoom, 
                     page):

    """
    A helper function to locate and format the size of the slide image
    given a specfic page number 

    Params:
      zoom : zoom factor, how much you want to expand or shrink the 
        image 

      page : the current page number you are displaying on the jupyter
        notebook

    Return:
      current_slide : the current slide that you want to display in the 
        notebook
    """

    current_slide = self._slides[page-1]
    current_slide.width = self._default_width*zoom
    current_slide.height = self._default_height*zoom
    return current_slide

  def slideshow(self,
                min_zoom=0.6,
                max_zoom=2,
                step_zoom=0.2):

    """
    The function that is meant to be called by the end users, this is 
    what you can call to display your slides in jupyter notebook

    Params:
      min_zoom : the minimum shrink factor, basically the left end of the 
        zoom slider 

      max_zoom : the maximum expand factor, essentially the right end of 
        the zoom slider 

      step_zoom : this is the step of each zoom, evenly distributed among 
        min_zoom to max_zoom, and number of steps = (max_zoom-min_zoom) / step_zoom

    Return:
      The interactive widget that allows you to display the slides (please 
        make sure that you are in the jupyter notebook environment)
    """

    return widgets.interact(self._current_slide, 
                            page=widgets.IntSlider(min=1, 
                                                   max=len(self._slides), 
                                                   step=1),
                            zoom=widgets.FloatSlider(value=1, 
                                                     min=min_zoom, 
                                                     max=max_zoom, 
                                                     step=step_zoom))