#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(E,filename='E',comment=''):
    """Takes numpy E in with shape (N_q,N_branch) and writes to binary file."""
    f=open(filename,'w')
    f.write(pack('<64s','E'))
    f.write(pack('<i',version))
    f.write(pack('<1024s',comment))
    #print E
    #print E.shape
    f.write(pack('<i',E.shape[0]))
    f.write(pack('<i',E.shape[1]))
    E = tuple( E.reshape(-1))
    f.write(pack('<%id' % len(E),*E))

def read(filename='E'):
    """Takes filename, returns a tuple with information and E as a numpy."""
    f=open(filename,'r').read()
    i = 0
    filetype, = unpack('<64s',f[i:i+64*strSize])          ; i += 64*strSize
    version,  = unpack('<i',f[i:i+intSize])               ; i += intSize
    comment,  = unpack('<1024s',f[i:i+1024*strSize])      ; i += 1024*strSize
    N_q,N_branch = unpack('<2i',f[i:i+2*intSize])            ; i += 2*intSize
    #print  N_q,N_branch
    E         = unpack('<%id' % (N_q*N_branch),f[i:])
    E = numpy.array(E)
    E.shape = (N_q,N_branch)
    #print E
    return (filetype.strip('\x00'),version,comment.strip('\x00')),E

