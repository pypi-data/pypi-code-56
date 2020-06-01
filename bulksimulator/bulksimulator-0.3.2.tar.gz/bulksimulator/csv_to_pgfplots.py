import numpy as np 

def _detect_shape(arr):
    start_point = arr[0,0]
    diff = arr[1,0] - arr[0,0]
    idx1 = 0
    print(start_point,diff)
    for i,row in enumerate(arr):
        print(row[0])
        if np.isclose(row[0],start_point,rtol=diff*0.01) and i > 0:
            idx1 = i
            break
    
    return (idx1,int(arr.shape[0]/(idx1)),3)


def _readin(filename,sep=',',header=True):
    headers = [' ']
    idx_offset = 0
    with open(filename,'r') as file:
        lines = file.read().splitlines()

    if header:
        headers = [col for col in lines[0].split(sep)]
        # remove '\n'
        headers[-1] = headers[-1][:-1]
        lines = lines[1:]

    linelengths = [len(l.split(sep)) for l in lines]

    if all(np.isclose(linelengths,3)):
        print('csv is of suitable format')
    elif all(np.isclose(linelengths,4)) and (headers[0] == 'idx' or headers[0] == 'index'):
        idx_offset = 1
    else:
        print("Not all rows have 3 entries.")
        quit()

    arr = np.empty((len(lines),3)) 

    for i,l in enumerate(lines):
        elements = l.split(sep)
        arr[i,0] = float(elements[0+idx_offset])
        arr[i,1] = float(elements[1+idx_offset])
        arr[i,2] = float(elements[2+idx_offset])
        
    return arr
    
        

def convert(filename,outputname,sep=',',header=True):
    '''
    Converts a csv called `filename` to a text file `outputname` which can be used to produce a pgfplot in latex of the parameter space.
    '''
    arr = _readin(filename,sep,header)

    shape = _detect_shape(arr)

    arr = arr.reshape(shape)

    with open(outputname,'w') as output:
        for block in arr:
            for row in block:
                for item in row:
                    output.write(f'{item} ') 
                output.write('\n')
            output.write('\n')