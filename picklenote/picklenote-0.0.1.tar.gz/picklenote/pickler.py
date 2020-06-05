import pickle

class PickleNote(object):
    def __init__(self, obj, note=''):
        self.obj = obj
        self.note = note
    
    @classmethod
    def load(cls, file, fix_imports=True, encoding='ASCII', errors='strict'):
        obj_d = load_obj_dict(file, fix_imports=fix_imports, encoding=encoding)
        return cls(obj=obj_d['obj'], note=obj_d['note'])

    def dump(self, file, protocol=None, fix_imports=True):
        dump(self.obj, self.note, file, protocol=protocol, fix_imports=fix_imports)


def load_obj_dict(file, fix_imports=True, encoding='ASCII', errors='strict'):
    # TODO: Check if `file` is text or a handler
    obj_d = None
    try:
        with open(file, 'rb') as f:
            obj_d = pickle.load(
                f,
                fix_imports=fix_imports,
                encoding='ASCII',
                errors='strict')
    except Exception as e:
        # TODO: Catch specific errors
        raise e
    return obj_d


def load(file, fix_imports=True, encoding='ASCII', errors='strict'):
    return PickleNote.load(file, fix_imports=fix_imports, encoding=encoding, errors=errors)

def dump(obj, note, file, protocol=None, fix_imports=True):
    obj_d = {'obj': obj, 'note': note}
    try:
        with open(file, 'wb') as f:
            pickle.dump(obj_d, f, protocol=protocol, fix_imports=fix_imports)
    except Exception as e:
        # Catch specific errors
        raise e            
