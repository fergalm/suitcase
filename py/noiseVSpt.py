# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 09:33:20 2015

@author: fergal

$Id$
$URL$

Todo:
Let starsep continue to run
noiseVSpt needs to a MMAST query for many modules,
    and a fit to the trend
    and a subtraction of known terms,
    and a sky noise estimator.
"""

__version__ = "$Id$"
__URL__ = "$URL$"



import matplotlib.pyplot as mp
import numpy as np
import nca

def main():

    fn = "sg12q14.txt"
    data = np.loadtxt(fn, delimiter=",")


    fp = open(fn, 'r')
    hdr = fp.readline()
    cols = hdr[1:].split(',')

    data = nca.Nca(data)
    data.setLookup(1, cols)
    idx = data[:, 'Logg'] > 4.5

    mp.clf()
    teff = data[idx, 'Teff']
    s = data[idx, 'cdpp6']
    mp.subplot(211)
    mp.scatter(data[idx, 'RA'], data[idx, 'Dec'], s=s, c=teff)
    mp.colorbar()
    mp.clim(3e3, 7e3)

    mp.subplot(212)
    mp.plot(data[idx, 'Teff'], s, 'ko')