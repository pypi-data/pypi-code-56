import os

def print_error(exc_type, unknown, exc_tb,err='',msg=''):
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(err), fname, exc_tb.tb_lineno,msg))   