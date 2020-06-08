"""
This package is to find the delimiter of any file.
The file should have minimum 2 rows in it.
find_delim(file_name,number_of_col)
where
file_name : Name of the file
col : Number of columns in the file.
"""
__author__ = "Arun Jaiswal <arun@deexams.com>"
import random

def _add_doc(func, doc):
    """Add documentation to a function."""
    func.__doc__ = doc

"""
Variable delim_list is default list of delimiters, one which should be the delimiter of source file.
The extra delimiter can be added into delim_list using below:
delim_list.append('YOUR-DELIMITER')
"""
delim_list = [',', '"', '_', '$', '#', '@', '&', '*','%','\t',' ','|']

def _blocks(files,size=65536):
    """
    This function should not be called directly outside of this package
    """
    while True:
        b=files.read(size)
        if not b:break
        yield b
_add_doc(_blocks,"This function should not be called directly outside of this package")

def _brut_force(first_line,random_line,cols):
    """
    This function should not be called directly outside of this package
    """
    dc,found,cf=0,str(),0
    for i,d in enumerate(delim_list,1):
        del_count_first = first_line.count(d)
        del_count_rand = random_line.count(d)
        dc=dc+1 if del_count_first>=(cols-1)  else dc
        cf=1 if del_count_first>(cols-1) else cf
        if del_count_first==(cols-1) and del_count_first==del_count_rand:
            found=d
            break
    return found,dc,cf
_add_doc(_brut_force,"This function should not be called directly outside of this package")

def find_delim(file_name,cols):
    """
    :param file_name:Input file name for which delimiter has to be determined
    :param cols: Number of columns in input file name
    :return: It will return the delimiter of file name if found, else '-1'
    delimiter = find_delim(file_name,cols)
    """
    first_line,random_line='',''
    try:
        f= open(file_name,'r')
    except IOError as e:
        print("File cannot be accessed . {}".format(e))
        return '-2'
    else:
        with f:
            rows=sum(b1.count('\n') for b1 in _blocks(f))
    if (rows <= 1):
        print("Minimum 2 rows are required")
        return '-2'
    try:
        f=open(file_name,'r')
    except IOError as e:
        print('File cannot be accessed {} .'.format(e))
    else:
        with f:
            first_line=f.readline().rstrip()
            if rows<=100:
                rn=random.randint(2,rows)
            else:
                rn = random.randint(2, 100)
            for _ in range(1,rn):
                random_line=f.readline().rstrip()
            found,d,cf=_brut_force(first_line,random_line,cols)
            k=0
            while not found:
                k+=1
                if d:
                    f.seek(0,0)
                    for _ in range(k):
                        f.readline()
                    if cf:
                        first_line=f.readline().rstrip()
                    try:
                        if rows<=100:
                            rn = random.randint(k+2,rows)
                        else:
                            rn = random.randint(k + 2, 100)
                    except ValueError as e:
                        return '-1'
                    for _ in range(k+1,rn):
                        random_line=f.readline().rstrip()
                    found, d,cf = _brut_force(first_line, random_line, cols)
                else:
                    found='-1'
            else:
                return found
_add_doc(find_delim,"""
    :param file_name:Input file name for which delimiter has to be determined
    :param cols: Number of columns in input file name
    :return: It will return the delimiter of file name if found, else '-1'
    delimiter = find_delim(file_name,cols)
    """)
if __name__=='__main__':
    print(find_delim.__doc__)
    __file_name__ = 'testdata.txt'
    __col__=10
    d=find_delim(__file_name__,__col__)
    if d!='-1':
        print("Delimiter of the file {} is :{}".format(__file_name__,'Space' if d.isspace() else d))
    else:
        print('Delimiter not found from list {}'.format(delim_list))
