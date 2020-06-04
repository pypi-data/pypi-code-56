# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 12:45:47 2019

@author: yuanq
"""

import PIL
from nltk.corpus import words
import pytesseract
import numpy as np

from dd8.utility.utils import Folder, File, find_file
from dd8.data_science.nlp import Dictionary
from dd8.data_science.enums import ENUM_DICTIONARY_LANGUAGE, ENUM_DICTIONARY_SOURCE

class OCR(object):
    def __init__(self, image,
                 str_tesseract_full_path = ''):
        self.image = image
        self.dictionary = None
        self.text = ''
    
    def set_tesseract_folder(self, str_full_path = ''):
        try:
            if not str_full_path:
                str_full_path = find_file('tesseract.exe')        
            
            pytesseract.pytesseract.tesseract_cmd = str_full_path
            return str_full_path
        except:
            return None        
    
    def image_to_string(self, bln_auto_adjust_image=False,
                        enum_dictionary_source=None,
                        enum_dictionary_language=None):
        self.text = pytesseract.image_to_string(self.image)
        if bln_auto_adjust_image:
            if not enum_dictionary_source:
                enum_dictionary_source = ENUM_DICTIONARY_SOURCE.NLTK_WORDS
                
            if not enum_dictionary_language:
                enum_dictionary_language = ENUM_DICTIONARY_LANGUAGE.ENGLISH
            
            self.dictionary = Dictionary(ENUM_DICTIONARY_SOURCE.NLTK_WORDS, ENUM_DICTIONARY_LANGUAGE.ENGLISH)
            temp = [word.lower() for word in self.text]
            
        else:            
            return self.text

class Images(object):
    def __init__(self, str_directory):
        self.directory = str_directory
        self.images = []
        
    def load_images(self, str_image_format = '.jpg'):
        folder = Folder(self.directory)
        files = folder.get_files([str_image_format])
        for file in files:
            if File(file).file_exists:
                self.images.append(Image(file))
    
class Image(object):
    def __init__(self, str_file_path):
        self.file_path = None
        self.image = None
        self.__lst_fwd_operations = []
        self.__lst_bwd_operations = []
        
    def from_file(self, str_file_path):        
        self.file_path = str_file_path
        try:
            self.image = PIL.Image.open(self.file_path)        
            return True
        except:
            return False
    
    def from_array(self, npa_image):
        try:
            self.image = PIL.Image.fromarray(npa_image)
            return True
        except:
            return False
    def to_array(self):
        return np.array(self.image)        
        
    def show(self):
        if self.image:
            self.image.show()
        else:
            return None
            
    def change_brightness(self, dbl_ratio=1.0):
        enhancer = PIL.ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(dbl_ratio)
        self.__lst_fwd_operations.append(('brightness', dbl_ratio, enhancer))
        return self.image
    
    def change_contrast(self, dbl_ratio=1.0):
        enhancer = PIL.ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(dbl_ratio)
        self.__lst_fwd_operations.append(('contrast', dbl_ratio))
        return self.image
    
    def change_sharpness(self, dbl_ratio=1.0):
        enhancer = PIL.ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(dbl_ratio)
        self.__lst_fwd_operations.append(('sharpness', dbl_ratio))
        return self.image
    
    def change_colour_balance(self, dbl_ratio=1.0):
        enhancer = PIL.ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(dbl_ratio)
        self.__lst_fwd_operations.append(('color_balance', dbl_ratio))
        return self.image
    
    def rotate(self, dbl_degrees_counter_clockwise=0.0):
        self.image = self.image.rotate(dbl_degrees_counter_clockwise)
        self.__lst_fwd_operations.append(('rotate', dbl_degrees_counter_clockwise))
        return self.image
    
    def undo(self):
        op = self.__lst_fwd_operations[-1]
        if self.__lst_fwd_operations:
            if op[0] == 'brightness':
#                enhancer = PIL.ImageEnhance.Brightness(self.image)
#                self.image = enhancer.enhance(1.0/op[1])
                enhancer = op[2]
                self.image = enhancer.enhance(1.0)
                self.__lst_bwd_operations.append(self.__lst_fwd_operations.pop())
                return self.image
            elif op[0] == 'contrast':
                enhancer = PIL.ImageEnhance.Contrast(self.image)
                self.image = enhancer.enhance(1.0/op[1])
                self.__lst_bwd_operations.append(self.__lst_fwd_operations.pop())
                return self.image
            elif op[0] == 'rotate':
                self.image = self.image.rotate(360.0 - op[1])
                return self.image
        
        return False
    
    def redo(self):
        pass
    
    def get_fwd_operations(self):
        return self.__lst_fwd_operations
    
    def get_bwd_operations(self):
        return self.__lst_bwd_operations
        