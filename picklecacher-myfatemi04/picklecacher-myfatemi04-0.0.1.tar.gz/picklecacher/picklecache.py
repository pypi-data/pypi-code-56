import os
import pickle
import random

def rand_str(length=32):
    return ''.join(chr(random.randint(65, 90)) for x in range(length))

class Picache:
    INDEX_FILE = ".index"

    def __init__(self, directory='./picache'):
        if directory is None:
            self.use_files = False
        else:
            self.use_files = True
            self.directory = directory
            self.indexfilename = os.path.join(self.directory, Picache.INDEX_FILE)
            self.index = {}
            if not os.path.isdir(directory):
                os.mkdir(directory)

            self._load_index()
        
        self.livecache = {}

    def _rel(self, filename):
        return os.path.join(self.directory, filename)

    def _load_index(self):
        if os.path.isfile(self._rel(".index")):
            with open(self._rel(".index"), "rb") as indexfile:
                try:
                    self.index = pickle.load(indexfile)
                except EOFError:
                    pass

    def _genfile(self):
        values = self.index.values()
        name = rand_str()

        while name in values:
            name = rand_str()

        return name

    # removes memory existance and file footprint
    def reset(self):
        self.clear_live()
        if self.use_files:
            self.remove_files()

    # completely deletes the live index from memory
    def clear_live(self):
        for key in self.livecache:
            del self.livecache[key]

    # removes all files created by the cache
    def remove_files(self):
        for filename in index.values():
            tobedeleted = self.rel(filename)
            os.remove(tobedeleted)

        os.remove(self.indexfilename)

    def _save(self, cachefile, result):
        with open(self._rel(cachefile), "wb") as towrite:
            pickle.dump(result, towrite)
    
    def __call__(self, subgroup='', picache_key_gen=lambda args, kwargs: (tuple(args), tuple(kwargs.items()))):
        def _decorator(func):
            def _wrap(*args, picache_key=None, **kwargs):
                if picache_key is None:
                    picache_key = picache_key_gen(args, kwargs)

                fn_picache_key = (subgroup, picache_key)
                
                # if the key is in the cache in memory already
                if fn_picache_key in self.livecache:
                    return self.livecache[fn_picache_key]
                
                # check if we are using files
                if self.use_files:
                    # if the key is in the index already
                    if fn_picache_key in self.index:
                        # locate the file
                        filename = self._rel(self.index[fn_picache_key])
                        
                        # check if file still exists
                        if os.path.exists(filename):
                            # load the file
                            with open(filename, "rb") as cachedobject:
                                # store it to memory
                                self.livecache[fn_picache_key] = pickle.load(cachedobject)
                                return self.livecache[fn_picache_key]
                        else:
                            # this shouldn't be in the index
                            del self.index[fn_picache_key]

                            # it will be added back soon

                # data is not cached yet
                result = func(*args, **kwargs)

                # store this data in memory
                self.livecache[fn_picache_key] = result
                
                # store this data to a file if necessary
                if self.use_files:
                    # generate a filename
                    cachefile = self._genfile()

                    # store this data in the index
                    self.index[fn_picache_key] = cachefile

                    # save this file in the cache
                    self._save(cachefile, result)

                    # overwrite previous index save data
                    self._save(Picache.INDEX_FILE, self.index)

                return result
            
            return _wrap

        return _decorator
