import os
import pickle
import json
from pathlib import Path
import jsonpickle

class FileManager(object):
    """description of class"""
    
    @staticmethod
    def save(object, path, method = None):
        """ Save file
        Args:
            path: provide a string path to where the file will be saved
            object: provide the object you want to save in that file
            method: save using either json or pickle, json is set by default
        Returns:
            bool representing if the save operation succedded
        """

        if method == None and (method != 'json' or method != 'pickle'):
            method = 'json'
        
        counter = 0
        while counter < 5:
            try:
                list_files = os.listdir(Path(path).parent)
                default_file  = None
                try:
                    default_file = next(f for f in list_files if f == Path(path).name)
                except StopIteration:
                    pass

                if default_file != None:
                    os.remove(path)

                file = None
                if method == 'json':
                    #with open(path, 'w') as outfile:
                    #    json.dump(object.__dict__, outfile)
                    with open(path, "w") as att_file:                    
                        att_file.write(jsonpickle.encode(object))
                    
                    with open(path, "r") as att_file:     
                        file = jsonpickle.decode(att_file.read())

                elif method == 'pickle':
                    with open(path, 'wb') as f:
                        pickle.dump(object, f)
                    with open(path, 'rb') as file_pickle:
                        file = pickle.load(file_pickle)

                if file != None:
                    return True
                else:
                    counter += 1
            except Exception as err:                
                print("Saving file has failed, try n: " + str(counter), err)
                counter += 1
        return False

    @staticmethod
    def get(path, method = None):
        """ Get file
        Args:
            path: provide a string path to where the file is saved           
            method: save using either json or pickle, json is set by default
        Returns:
            False if the path is not correct or it is not a file path
            the content txt file in case of using json method and object in case of using the pickle method
        """
        if path == None or path =='':
            return False

        if not os.path.exists(path):
            print('File you are trying to get does not exist!')
            return False

        if method == None and (method != 'json' or method != 'pickle'):
            method = 'json'
        
        counter = 0
        while counter < 5:
            try:
                folder = Path(path).parent
                list_files = os.listdir(folder)
                defaultSetting  = None
                try:
                    default_file = next(f for f in list_files if f == Path(path).name)
                except StopIteration:
                    pass                   
                if default_file != None:
                    if method == 'json':
                        #with open(path) as json_file:
                        #    file = json.load(json_file, cls = cls_value)
                        
                        with open(path, "r") as file:
                            file = jsonpickle.decode(file.read())

                    
                    elif method == 'pickle':
                        with open(path, 'rb') as file_pickle:
                            file = pickle.load(file_pickle)
                    if file != None:
                        return file
                    else:
                        counter += 1
            except Exception as err:
                print("Reading file has failed, try n: " + str(counter), err)
                counter += 1
        return None

    @staticmethod
    def delete(path):
        """ Delete file
        Args:
            path: provide a string path to where the file will be deleted          
        Returns:
            bool representing if the delete operation succedded
        """

        if not os.path.exists(path):
            print('File you are trying to delete does not exist!')
            return True

        if not os.path.isfile(path):
            print('Please check the provided path')

        counter = 0
        while counter < 5:
            try:                
                list_files = os.listdir(Path(path).parent)
                default_file  = None
                try:
                    default_file = next(f for f in list_files if f == Path(path).name)
                except StopIteration:
                    pass

                if default_file != None:
                    os.remove(path)
                                    
                if os.path.exists(path):
                    print('A try to delete the file did not succed')
                    counter += 1
                else:
                    return True               
                    
            except Exception as err:                
                print("Saving file has failed, try number: " + str(counter), err)
                counter += 1
        return False