'''Wrapper, ERFA and SOFA version information.'''

# Set the version numbers a bit indirectly, so that Sphinx can pick up
# up the docstrings and list the values.
from . import ufunc


erfa_version = ufunc.erfa_version
'''Version of the C ERFA library that is wrapped.'''

sofa_version = ufunc.sofa_version
'''Version of the SOFA library the ERFA library is based on.'''

del ufunc

# Note that we need to fall back to the hard-coded version if either
# setuptools_scm can't be imported or setuptools_scm can't determine the
# version, so we catch the generic 'Exception'.
try:
    from setuptools_scm import get_version
    version = get_version(root='..', relative_to=__file__)
    '''Version of the python wrappers.'''
except Exception:
    version = '1.7.0'
else:
    del get_version
