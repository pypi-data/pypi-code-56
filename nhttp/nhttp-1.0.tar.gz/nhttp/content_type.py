
__all__ = ['ContentType', 'content_type_manager']


class ContentType:
    def __init__(self, type_ :str, subtype :str, parameter :str=''):
        self.type = type_
        self.subtype = subtype
        self.parameter = parameter

    def __str__(self):
        return '%s/%s %s' % (self.type, self.subtype, 
                             ';%s' % (self.parameter))

    def __repr__(self) -> str:
        return 'ContentType(\'%s\', \'%s\', \'%s\')' % (self.type, self.subtype, self.parameter)


class __ContentTypeManager:
    __TYPE_MAP = {
        ('.js',): ContentType('application', 'javascript'),
        ('.htm', '.html'): ContentType('text', 'html'),
        ('.css',): ContentType('text', 'css'),
    }

    __ANY_CONTENT_TYPE = ContentType('*', '*')

    def get(self, fext :str) -> ContentType:
        for ext, ct in self.__TYPE_MAP.items():
            if ext == fext:
                return ct
        return self.__ANY_CONTENT_TYPE

    def get_type_with_parameter(self, k, parameter :str) -> ContentType:
        t = self.__getitem__(k)
        t.parameter = parameter

        return t


content_type_manager = __ContentTypeManager()


if __name__ == '__main__':
    ct = ContentType('text', 'html', 'charest=utf8')
    print(str(ct))
    print(repr(ct))
