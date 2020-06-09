import numpy as np
from numpy.linalg import inv
import argparse

'''
This is just for practice purpose. Scipy and numpy
have already provided enough tools.
'''
def x_hat(A, b):
    aTa = A.T.dot(A)
    aTa_inv = inv(aTa)
    return aTa_inv.dot(A.T).dot(b)

def project(A, b):
    '''
    * is dot product
    p = P*b = a*inv(aT*a)*aT*b
    '''
    aTa = A.T.dot(A)
    aTa_inv = inv(aTa)
    x_bar = aTa_inv.dot(A.T)
    p = A.dot(x_bar).dot(b)
    return p, x_bar

def main():
    arg = argparse.ArgumentParser(description='Calculations in Linear Algebra')
    sub_parsers = arg.add_subparsers(help='projection', dest='command')
    projection_args = sub_parsers.add_parser('project')
    projection_args.add_argument('-A', '--A', help='matrix to be projected on. example: [[1,2,3], [1,2,3]] is a 2x3 matrix.')
    projection_args.add_argument('-b', '--b', help='matrix to poject')

    arbi = sub_parsers.add_parser('arb')
    arbi.add_argument('-A', '--A')

    a = arg.parse_args()

    if a.command == 'project':
        print(project(np.array(eval(a.A)), np.array(eval(a.b))))


if __name__ == '__main__':
    # A = np.array([1,0,1,1,1,2]).reshape(3,2)
    # b = np.array([6,0,0])
    # print(x_hat(A, b))
    main()