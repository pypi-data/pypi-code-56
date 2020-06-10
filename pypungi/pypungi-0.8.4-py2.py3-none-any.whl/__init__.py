'''Connects to pypungi app'''

__version__ = "0.8.4"

from .main import link

if __name__ == '__main__':
    import pypungi
    
    pp = pypungi.link()
    pp.stash('hi')
    pp.getStash()
    