import numpy as np
from scipy.signal import convolve2d # for NeighborSum
#from anytree import NodeMixin
from math import inf, nan
import random
from random import randint
from numpy.random import choice


def view1D(a, b): # a, b are arrays
    a = np.ascontiguousarray(a)
    b = np.ascontiguousarray(b)
    void_dt = np.dtype((np.void, a.dtype.itemsize * a.shape[1]))
    return a.view(void_dt).ravel(),  b.view(void_dt).ravel()

def isin_nd(a,b):
    # a,b are the 3D input arrays to give us "isin-like" functionality across them
    A,B = view1D(a.reshape(a.shape[0],-1),b.reshape(b.shape[0],-1))
    return np.isin(A,B)

def npinlist(x,y):
    # to check if x in y
    # x is a ndarray, y is a ndarray(or python list) of ndarrays
    return any((x==z).all() for z in y)

def npsetdiff2d(a,b):
    # a and b are 2d ndarrays, this func returns a-b(set operation)
    a1_rows = a.view([('', a.dtype)] * a.shape[1])
    a2_rows = b.view([('', b.dtype)] * b.shape[1])
    c = np.setdiff1d(a1_rows, a2_rows).view(a.dtype).reshape(-1, a.shape[1])
    return c

def npsetinter2d(arr1,arr2):
    # a and b are 2d ndarrays, this func returns a and b(set operation)
    arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    intersected = np.intersect1d(arr1_view, arr2_view)
    return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

def get8idx(idx, xrange, yrange):
    # this return the valid indices of neighbor given an center index
    x = idx[0]
    y = idx[1]
    n = np.array([[x-1, y-1], [x-1, y], [x-1, y+1],[x, y-1], [x, y+1],[x+1, y-1], [x+1, y], [x+1, y+1]])

    # delete x<0 or x>xrange
    x = n[:,0]
    n = np.delete(n, np.where(np.logical_or(x < 0, x >= xrange))[0], axis=0)
    
    # delete y<0 or y>yrange
    y = n[:, 1]
    n = np.delete(n, np.where(np.logical_or(y < 0, y >= yrange))[0], axis=0)

    return n.astype('int32')

def NeighborSum(s):
    # compute the neighbor sum of each in the matrix
    return convolve2d(s,np.ones((3,3),dtype=int),'same') - s

def getEleLen(e):
    # get the domain size of a element in Domain
    if e is None:
        return 500 # for represent of int inf
    else:
        return len(e)
vgetEleLen = np.vectorize(getEleLen)

def maxDomain(e): 
    # bug for empty element!!!
    # get the max in domain
    if e is None:
        return 0
    else:
        return e.max()
    
vmaxDomain = np.vectorize(maxDomain)

def minDomain(e):
    # bug for empty element!!!
    # get the min in domain
    if e is None:
        return 0
    else:
        return e.min()
    
vminDomain = np.vectorize(minDomain)
