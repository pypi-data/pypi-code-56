from .content_type_table import CONTENT_TYPE_DICT


__all__ = ['ContentType', 'content_type_manager']


class ContentType:
    def __init__(self, type_ :str, subtype :str, parameter :str=''):
        self.type = type_
        self.subtype = subtype
        self.parameter = parameter

    @staticmethod
    def new_from_str(content_str :str):
        try:
            t, st = content_str.split('/', 1)
            nst = content_str.replace(' ', '', 1)
            _, *p = nst.split(';', 1)
            
            p = p[0] if p else ''

            return ContentType(t, st, p)

        except ValueError:
            return None

    def __str__(self):
        return '%s/%s %s' % (self.type, self.subtype, 
                             ';%s' % (self.parameter) if self.parameter else '')

    def __repr__(self) -> str:
        return 'ContentType(\'%s\', \'%s\', \'%s\')' % (self.type, self.subtype, self.parameter)


class __ContentTypeManager:
    __BIN_CONTENT_TYPE = ContentType('application', 'octet-stream')

    def get(self, fext :str) -> ContentType:
        return ContentType.new_from_str(CONTENT_TYPE_DICT.get(fext, CONTENT_TYPE_DICT['.*']))

    def get_type_with_parameter(self, fext, parameter :str) -> ContentType:
        t = self.get(fext)
        t.parameter = parameter

        return t


content_type_manager = __ContentTypeManager()


if __name__ == '__main__':
    ct = content_type_manager.get('.jpg')

    print(str(ct))
    print(repr(ct))
