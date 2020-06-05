import os
import tempfile

# By default mkstemp() creates a file with
# a name that begins with 'tmp' (lowercase)
tmphandle, tmppath = tempfile.mkstemp()
CASE_SENSITIVE = not os.path.exists(tmppath.upper())
