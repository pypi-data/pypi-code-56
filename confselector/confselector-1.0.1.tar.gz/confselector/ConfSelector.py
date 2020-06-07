# -*- coding: utf-8 -*-
import os
import types


class ConfSelector(object):
    """
    静态类
    """
    DEFAULT_SEARCH_DIRS = [
    ]
    SELECTED_CONFIG_ABSFILENAME = None
    SELECTED_CONFIGOBJ = None

    @classmethod
    def configure(cls, defaultSearchDirs):
        """
        example as:

SELFDIR = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
PROJECTDIR = os.path.dirname(SELFDIR).replace('\\', '/')
ConfSelector.configure([
    PROJECTDIR,
    os.path.join(PROJECTDIR, 'config').replace('\\', '/'),
    os.path.join(PROJECTDIR, 'conf').replace('\\', '/'),
    SELFDIR,
])

        """
        cls.DEFAULT_SEARCH_DIRS = defaultSearchDirs
        return cls

    @classmethod
    def pyfile(cls):
        if cls.SELECTED_CONFIG_ABSFILENAME is None:
            raise RuntimeError('Please call `select` method before you call this method!')
        return cls.SELECTED_CONFIG_ABSFILENAME

    @classmethod
    def configobj(cls):
        if cls.SELECTED_CONFIGOBJ is None:
            raise RuntimeError('Please call `select` method before you call this method!')
        return cls.SELECTED_CONFIGOBJ

    @classmethod
    def selected(cls, providedflag=None, provideddir=None):
        cls.select(providedflag, provideddir)
        return cls.SELECTED_CONFIG_ABSFILENAME, cls.SELECTED_CONFIGOBJ

    @classmethod
    def select(cls, providedflag=None, provideddir=None):
        absfilename = cls.match(providedflag, provideddir)
        if absfilename is None:
            raise RuntimeError('Can not match any config file!!! 无法匹配到配置文件！！！ providedflag is `%s`' % providedflag)

        cls.SELECTED_CONFIG_ABSFILENAME = absfilename
        cls.SELECTED_CONFIGOBJ = cls.frompyfile(absfilename)
        return cls

    @classmethod
    def match(cls, providedflag=None, provideddir=None):
        providedflag = providedflag.lower() if providedflag is not None else ''  # here pay attention
        for flag, filename, absfilename in cls.search(provideddir):
            if flag.lower() == providedflag:
                return absfilename
        return None

    @classmethod
    def search(cls, provideddir=None):
        dirs = cls.DEFAULT_SEARCH_DIRS  # here pay attention
        if provideddir is not None:
            if isinstance(provideddir, str):
                dirs = [provideddir, ]
            elif isinstance(provideddir, (list, tuple)):
                dirs = list(provideddir)
        results = []
        for thedir in dirs:
            if os.path.exists(thedir) and os.path.isdir(thedir):
                for filename in os.listdir(thedir):
                    if filename.endswith('.py') and filename.lower().startswith('config'):  # here pay attention
                        absfilename = os.path.join(thedir, filename).replace('\\', '/')
                        if os.path.exists(absfilename) and os.path.isfile(absfilename):
                            flag = filename[6:-3]  # here pay attention  # 6 == len('config')  # 3 == len('.py')
                            results.append([flag, filename, absfilename])
        return results

    @classmethod
    def frompyfile(cls, absfilename):
        m = types.ModuleType('configmodulename')
        m.__file__ = absfilename
        with open(absfilename, mode='rb') as f:
            exec(compile(f.read(), absfilename, 'exec'), m.__dict__)
        return m

    # @classmethod
    # def fromobject(cls, obj):
    #     dct = {}
    #     for key in dir(obj):
    #         if key.isupper():
    #             dct[key] = getattr(obj, key)
    #     return dct
