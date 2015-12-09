# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 08:31:42 2015

@author: fergal

$Id$
$URL$
"""

__version__ = "$Id$"
__URL__ = "$URL$"



import matplotlib.pyplot as mp
import numpy as np

import greatcircle as gc
import scenery
import apj
import os

def main():

    hdCatFile = "/home/fergal/all/kepler/twowheel/hdcat.txt"
    nCompanions = 10

    print "Loading ..."
    hdCat = scenery.loadHdCatalogue(hdCatFile, maxMag=12)

    fn = "distMat.npz"
    if os.path.exists(fn):
        print "Using cached values..."
        npzFile = np.load(fn)
        distMat = npzFile['distMat']
        mags = npzFile['mags']
        npzFile.close()
        pass
    else:
        print "Computing ..."
        distMat, mags = computeDistMatrix(hdCat, magCol=3, maxMag=8)
        np.savez(fn, distMat=distMat, mags=mags)

    mp.clf()
    apj.pre()
#    mp.imshow(distMat, interpolation="nearest")

    print "Computing focal plane radius..."
    for nCompanions in [30, 10,3]:
        radius = computeDistToNNearestStars(distMat, nCompanions)
        mp.plot(mags, radius, '-', label="%i stars" %(nCompanions))

    mp.xlabel("Magnitude")
    mp.ylabel("Distance (degrees)")
    mp.legend(loc=1)
    mp.title("Distance to nearest bright stars")
    mp.ylim(0,40)
    apj.post()
    return distMat, mags


def computeDistMatrix(hdCatIn, raCol=0, decCol=1, magCol=2, maxMag=6):
    #Construct cat of bright stars only, sorted increasing magnitude
    idx = hdCatIn[:, magCol] <= maxMag
    cat = hdCatIn[idx]
    idx = np.argsort(cat[:,magCol])
    cat = cat[idx]

    nStar = len(cat)
#    nStar = 100  #Useful debugging code
    dist = np.zeros((nStar, nStar))

    for i in range(1, nStar):
        for j in range(0, i):
            dist[i,j] = gc.sphericalAngSep(cat[i, raCol], cat[i, decCol],
                                           cat[j, raCol], cat[j, decCol])

    return dist, cat[:nStar, magCol]


def computeDistToNNearestStars(distMat, nCompanions):
    nStar = len(distMat)

    radius = np.ones(nStar)*180  #Default value
#    nStar = 20
    for i in range(nCompanions+1, nStar):
        starArray = sorted(distMat[i, :i])
        radius[i] = starArray[nCompanions]

    return radius
