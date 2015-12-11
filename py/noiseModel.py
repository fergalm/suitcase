# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:59:49 2015

@author: fmullall
"""

__version__ = "$Id$"
__URL__ = "$URL$"

import matplotlib.pyplot as mp
import numpy as np
import const
import apj

import starsize as sp
def plotPerfVSpectralType():

    teff = np.linspace(3000, 7000, 9)

    prad_earth = 4
    prad = prad_earth  * const.earthRadius/const.solarRadius
    srad = sp.getParam(teff)

    mp.clf()
    apj.pre()

    for m in [9,12,15]:
        signal_ppm = 1e6*(prad/srad)**2
        noise_ppm = noiseModel_ppm(m, expTime_sec=1800, teff_K=teff)
        snr = signal_ppm/noise_ppm

        mp.plot(teff, snr, '-', lw=4, label="V=%i" %(m))

    apj.post()
    mp.xlim([7000, 3000])
#    mp.ylim(0, 50)
    mp.legend(loc=2)
    mp.xlabel("Stellar Temperature (K)")
    mp.ylabel("Expected Signal-to-Noise")
    mp.gca().set_yscale('log')
    mp.grid(True, which='both')
    mp.title("Estimated SNR For %.1f Re radius planet" %(prad_earth))
    apj.pgid()

def noiseModel_ppm(mag, apertureSize_m=0.3, expTime_sec=1800, \
    teff_K=5780, optAp_pix=1):
    """Construct a noise model for a suitcase sat telescope.

    Assumes properties of Kepler CCD are equivalent to the suitcase
    sat.

    Inputs:
    ------------
    mag
        (1d np array) Magnitude(s) of star. Assume the zeropoints of
        Kepler and the suitcase star are the same, for simplicity


    Optional Inputs:
    -----------------
    apertureSize_m
        (float) Aperture size of suitcase sat. Units: metres

    expTime_sec
        (float)  Exposure time in seconds

    teff_K
        (float) Effective temperature of star. Used to select noise
        properties of star. Currently ignored.

    optAp_pix
        (1d np array) Size of optimal aperture in pixels.


    Todo:
    ---------
    Add an estimate of background noise.
    """

    shot = computeShotNoise_ppm(mag, apertureSize_m, expTime_sec)
    print shot

    #Taken from Gilliland 2015 section 3.2 where he gives the
    #variance as 98ppm^2. I treat this as a constant independent
    #of exp time.
#    instrument = 10.

    #TESS numbers from Ricker (2014) Figure 8
    instrument = 60.

    stellar = computeStellarNoise_ppm(teff_K, expTime_sec)

    read = computeReadNoise_ppm( optAp_pix)

    total = shot**2 + instrument**2 + stellar**2 + read**2
    total = np.sqrt(total)

    return total


def computeReadNoise_ppm(optAp_pix):
    """Read noise is taken from \S 4.3 of Kepler Instrument Handbook
    where it is given as 120 e-/frame.
    270 frames = 1 cadence => 7e-/cadence/pixel
    """
    return 7/np.sqrt(optAp_pix)


def computeStellarNoise_ppm(teff_K, expTime_sec):
    """Stellar noise is a function of spectral type and
    exposure time. I have computed neither term (in particular
    the variance with exposure time might be complicated),
    so a default to a typical value.

    This values provenance is complicated.
    Gilliland (2015) gives the sum of stellar and Poisson variance as
    664ppm^2, or noise == 25ppm.

    Koch (2010) gives the shot noise as 20ppm, and
    sqrt(25*2 - 20**2) = 15.
    That's averaged over 1 LC. But I assume the noise is constant
    with exposure time (which isn't necessarily true).
    """

    return 15.

def computeShotNoise_ppm(mag, apertureSize_m, expTime_sec):
    """Compute shot noise.

    Taken from Koch (2010) which gives a requirement for Kepler
    of 1.4e6 e-/s for Kepler, which corresponds to 845ppm/second

    Kepler aperture of .95m given in Koch (2010)
    """

    expn = (mag-12)/5.
    print expn
    shot = 845 * np.sqrt(1/float(expTime_sec)) * 10**expn

    #Scale by aperture size
    shot *= 0.95/apertureSize_m

    return shot

