from distutils.core import setup
from os import path # read the contents of your README file
import pypandoc

long_description = """
jupyslides
==========

A tool that allows you to display embedded slides in jupyter notebook. This is a simple widget to help you display your PPT / slides inside the jupyter notebook environment for better presentation experience. 

How to install
--------------

You can install the package by typing this command in your terminal: 

``pip install jupyslides``

How to use the package 
----------------------

* **Step 1** - Export the PPT in image format 

  The essential mechanism of this package is that you are displaying images instead of displaying the PPT itself. Therefore, the most critical step is to export your PPT in image format. 
  
  Luckily, if you are working with Microsoft PowerPoint, you can export your PPT internally by clicking the following tabs in your PPT menu: ``File > Export... > File Format > PNG > Save Every Slide > Export``. By doing so, PowerPoint will automatically generate a folder whose name is the same as your PPT file name. Inside this folder, each slide is exported as a ``.png`` image file. 
  
  Notice that, the name of each image file ends with a number - this is critical as it tells the tool the sequence of the slides, for example, ``Slide1.png``, ``Slide2.png``, ``Slide3.png`` etc. The slides will then be sorted in ascending order. 
  
  Under any circumstance that PowerPoint does not generate these numbers, please manually add the number at the end of the file. Any file without a number in the end will be IGNORED. If you are not working with Microsoft PowerPoint, please make sure that you have fulfilled the above requirements. 
  
* **Step 2** - Initialization

  Starting from this step, you are assumed to have already exported your PPT in a folder with a bunch of images. Please make sure that you are aware of the path of this folder. If you are not sure where the folder is, you can ``cd`` into the PPT folder, and type the command ``pwd`` to check where it is located in your system. 
  
  Below is the quickest way to initiate your slides 
  
  ``from jupyslides import jupyslides``

  You can adhere to the default dimension of your slides, which is ``width = 720px`` and ``height_to_width_ratio = 810/1080``

  ``slides_path = 'path/to/your/PPT/folder'``\n
  ``js = jupyslides(slides_path)``
  
  You do have some level of control over the default size of the width of your slide, as well as the ratio between the height and width of your slides, you can make such customization by doing the following
  
  ``js = jupyslides(slides_path, default_width=1000, height_to_width_ratio=12/30)``

* **Step 3** - Slideshow

  As of now, you have initialized the slides already, the last step is to display the slides embedded in your jupyter notebook. 
  The simplest method to showcase your embedded slides is

  ``js.slideshow()``

  In this case, you are adhering to the default zoom-in, zoom-out and zoom-step factors. However, if you do want to have some control over the zooming feature, you can modify the parameters ``min_zoom``, ``max_zoom`` and ``step_zoom``.
  
  ``js.slideshow(min_zoom=0.2, max_zoom=3, step_zoom=0.1)``

  That's it for the tutorial, if you have any questions, please contact me at ``nding17@outlook.com``
"""

setup(
  name = 'jupyslides',         
  packages = ['jupyslides'],
  version = '0.194',
  license = 'MIT',
  description = 'A jupyter notebook widget that allows you to create an embedded ppt slides',
  long_description_content_type = "text/markdown",
  long_description = long_description,
  author = 'Naili Ding',
  author_email = 'nding17@outlook.com',
  url = 'https://github.com/nding17/jupyslides',
  download_url = 'https://github.com/nding17/jupyslides/archive/v_013.tar.gz',
  keywords = [
    'jupyter notebook', 
    'embedded ppt', 
    'embedded slides'
  ],
  install_requires = [
    'ipywidgets',
    'natsort',
    'IPython',
  ],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)