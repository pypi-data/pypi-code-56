'''
vision stuff for generall purpose
version: 0.1.0
date: 02.06.2020
'''
import sys
import os
import random
import numpy as np
import cv2


def script_path():
    '''change dir, to current script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def blank_image(height, width, layers=3, value=255):
    '''create blank image, with specified shape, layers and initial value'''
    img = np.ones((height, width, layers), dtype=np.uint8)*value
    return img
    
    
def save_img(path, img, new_dir='NEW_DIR'):
    '''save img to specified directory'''
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
        
    path = os.path.join(new_dir, path)
    cv2.imwrite(path, img)
    return True
    
    
def shrink_image(img, width=640, height=640, resize=True):
    '''perform image, to fit frame; width and height are shape of full image
    todo:
        -think of detecting main object and move on x(y) axis to cut it
    '''
    
    out = img.copy()
    frame_img_height, frame_img_width = out.shape[:2]
    
    proper_frame_width = width
    proper_frame_height = height
    proper_frame_ratio = proper_frame_width/proper_frame_height
    
    
    # calc value to cut
    if frame_img_height/frame_img_width < proper_frame_ratio:
        new_width = round(frame_img_height/proper_frame_ratio)
        cut_width = round((frame_img_width - new_width)/2)
        out = out[:, cut_width: frame_img_width - cut_width]
    else:
        new_height = round(frame_img_width/proper_frame_ratio)
        cut_height = round((frame_img_height - new_height)/2)
        out = out[cut_height: frame_img_height - cut_height, :]
        
    if resize:
        # resize to frame size
        out = cv2.resize(out, (proper_frame_width, proper_frame_height))
    return out
    
    
def shrink_and_store_images_dir(directory, width=640, height=640, resize=True):
    '''shrink all images from specified directory and store them into new directory named (directory + "_converted")'''
    try:
        files = [(file, os.path.join(directory, file)) for file in os.listdir(directory)]
    except FileNotFoundError:
        print('no such directory: {}'.format(directory))
        return False
        
    converted_images = []
    for key, (file, file_path) in enumerate(files):
        # print(key)
        img = cv2.imread(file_path, 1)
        converted = shrink_image(img, width, height, resize)
        converted_images.append(converted)
        save_img(file, converted, new_dir='{}_converted'.format(directory))
    return None
    
    
def shrink_img_cli():
    '''shrink single image, cli tool'''
    print(42)
    return True
    
    
def shrink_dir_cli():
    '''shrink directory, cli tool'''
    print(42)
    return True
    
    
def shrink_example(img, width=400, height=400, resize=True):
    '''not completed for now'''
    breakpoint()
    
    # **** example part ****
    full_example = blank_image(1080, 1920)  # put there example images
    example_first = img.copy()  # first image, to be shown as example
    print(example_first.shape)
    example_first_text = 'shape\n{}'.format(example_first.shape[:2])
    show_image('example_first', example_first)
    
    
    out = img.copy()
    frame_img_height, frame_img_width = out.shape[:2]
    
    proper_frame_width = width
    proper_frame_height = height
    proper_frame_ratio = proper_frame_width/proper_frame_height
    
    
    # calc value to cut
    if frame_img_height/frame_img_width < proper_frame_ratio:
        new_width = round(frame_img_height/proper_frame_ratio)
        cut_width = round((frame_img_width - new_width)/2)
        out = out[:, cut_width: frame_img_width - cut_width]
        
        # **** example part ****
        example_second = img.copy()
        # draw square on second image
        # example_second = cv2.rectangle(example_second, (x1, y1), (x2, y2), (255,0,0), 2)
        example_second = cv2.rectangle(
            example_second,
            (cut_width, 0),
            (frame_img_width - cut_width, frame_img_height-1),
            (50, 255, 50),
            2
        )
        
        
    else:
        new_height = round(frame_img_width/proper_frame_ratio)
        cut_height = round((frame_img_height - new_height)/2)
        out = out[cut_height: frame_img_height - cut_height, :]
        
        # **** example part ****
        example_second = img.copy()
        # draw square on second image
        example_second = cv2.rectangle(
            example_second,
            (0, cut_height),
            (frame_img_width-1, frame_img_height - cut_height,),
            (50, 255, 50),
            2
        )
        
        
    # **** example part ****
    print(example_second.shape)
    example_second_text = 'shape\n{}'.format(example_second.shape[:2])
    show_image('example_second', example_second)
    
    
    # shrink square from original image
    example_third = out.copy()
    print(example_third.shape)
    example_third_text = 'shape\n{}'.format(example_third.shape[:2])
    show_image('example_third', example_third)
    
    
    if resize:
        # resize to frame size
        out = cv2.resize(out, (proper_frame_width, proper_frame_height))
        
        
        # **** example part ****
        # resize example image
        example_fourth = out.copy()
        print(example_fourth.shape)
        example_fourth_text = 'shape\n{}'.format(example_fourth.shape[:2])
        show_image('example_fourth', example_fourth)
        
    return out
    
    
    
if __name__ == "__main__":
    print('vision stuff, by streanger')
    
    # script_path()
    # shrink_and_store_images_dir('example_images', 640, 640)
    
    # img = cv2.imread('example.jpg', 1)
    # shrink_example(img, width=400, height=400, resize=True)
    
    
    
'''
function to use:
    -shrink_image
    -shrink_and_store_images_dir
    
cli tools:
    -shrink_images file <width> <height>        # default 640x640
    -shrink_dir directory <width> <height>      # default 640x640
        -make some progress bar
        
    
'''
