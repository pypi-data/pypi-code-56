#!C:\Users\Thilo\AppData\Local\Programs\Python\Python38-32\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'isoquant-diff==0.0.15','console_scripts','isoquant_diff'
__requires__ = 'isoquant-diff==0.0.15'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('isoquant-diff==0.0.15', 'console_scripts', 'isoquant_diff')()
    )
