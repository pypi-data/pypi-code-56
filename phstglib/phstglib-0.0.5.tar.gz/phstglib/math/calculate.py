import cmath

def xy2radian(x, y):
    """坐标转弧度

    Parameters
    ----------
    
    Return
    ------
    radian : float
        弧度，0-2*pi
    """
    cn = complex(x, y)
    angle = cmath.polar(cn)[1]
    return angle if angle > 0 else angle + cmath.pi*2