import numpy as np
import math



def get_shape(argv):


    
    shape = argv.setdefault('shape','square')
   
    if type(shape) == list:
     assert(len(shape)==len(argv['base']))
     shapes_str = shape
    else:
     shapes_str = len(argv['base'])*[shape]   


    #compute area weigths
    argv.setdefault('area_ratios',np.ones(len(argv['base'])))
    areas =  [argv.setdefault('porosity')* i /sum(argv['area_ratios'])  for i in argv['area_ratios']]
    

    #-------------------

    shapes = []
    for n,shape in enumerate(shapes_str):

     #area  = argv.setdefault('porosity')/len(argv['base'])
     area= areas[n]
     #print(area,area2)
     #quit()

     if shape == 'square':
       shapes.append(np.array(make_polygon(4,area)))

     if shape == 'triangle':
       shapes.append(np.array(make_polygon(3,area)))

     elif shape == 'circle':
       shapes.append(np.array(make_polygon(24,area)))

     elif shape == 'custom':
      options = argv.setdefault('shape_options',{})
      options.update({'area':area})

      shapes.append(argv['shape_function'](options))

    return shapes  



def make_polygon(Na,A):
 
   dphi = 2.0*math.pi/Na;
   r = math.sqrt(2.0*A/Na/math.sin(2.0 * math.pi/Na))
   poly_clip = []
   for ka in range(Na):
     ph =  dphi/2 + (ka-1) * dphi
     px  = r * math.cos(ph) 
     py  = r * math.sin(ph) 
     poly_clip.append([px,py])

   return poly_clip  



def get_smoothed_square(**argv):

     
     smooth = argv['smooth']
     area = argv['area']
     Na = argv['Na']
     L = np.sqrt(area+smooth*smooth*(4-np.pi))

     p = []
     dphi = math.pi/Na/2;
     for ka in range(Na+1):
      ph =  dphi * ka
      px  = L/2 - smooth + smooth * math.cos(ph)
      py  = L/2 - smooth + smooth * math.sin(ph)
      p.append([px,py])

     dphi = math.pi/Na/2;
     for ka in range(Na+1):
      ph = np.pi/2 +  dphi * ka
      px  = - L/2 + smooth + smooth * math.cos(ph)
      py  = + L/2 - smooth + smooth * math.sin(ph)
      p.append([px,py])

     dphi = math.pi/Na/2;
     for ka in range(Na+1):
      ph = np.pi +  dphi * ka
      px  = - L/2 + smooth + smooth * math.cos(ph)
      py  = - L/2 + smooth + smooth * math.sin(ph)
      p.append([px,py])

     dphi = math.pi/Na/2;
     for ka in range(Na+1):
      ph = 1.5*np.pi +  dphi * ka
      px  = + L/2 - smooth + smooth * math.cos(ph)
      py  = - L/2 + smooth + smooth * math.sin(ph)
      p.append([px,py])

     return p







