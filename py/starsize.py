# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:44:53 2015

@author: fmullall
"""

__version__ = "$Id$"
__URL__ = "$URL$"

import numpy as np
import nca

def schmidtKaler():
    """Data on mass, radius and effective temperature of stars.

    Taken from Appendix E of Carroll & Ostlie, which in turn
    takes it from Schmidth-Kaler (1982). I can't find a copy
    of the original reference though.

    Compare and contrast with HabetHeinz, below.

    Inputs:
    ----------
    None

    Returns:
    ------------
    A Nca of temperature, radius and mass. Units are Kelvin, solar
    radii and solar masses.
    """

    data = np.array([ \
        [7200, 1.6, 1.6], \
        [6440, 1.4, 1.4], \
        [6030, 1.1, 1.05], \
        [5770, .89,  .92], \
        [5250, .79,  .79], \
        [4350, .68,  .67], \
        [3850, .63,  .51], \
        [3580, .55,  .40], \
        [3240, .33,  .21], \
        [2640, .17,  .06], \
        ])

    out = nca.Nca(data)
    out.setLookup(1, "teff radius mass".split())
    return out


def habetsHeinze():
    """Data on mass, radius and effective temperature of stars.

    Taken from Table VIII or Habets & Heinze (1981 A&AS 46, 193)

    Compare and contrast with HabetHeinz, below.

    Inputs:
    ----------
    None

    Returns:
    ------------
    A Nca of temperature, radius and mass. Units are Kelvin, solar
    radii and solar masses.
    """


    data = np.array([ \
        [7610, 1.4,   1.4], \
        [7040, 1.31,  1.34], \
        [6690, 1.23,  1.29], \
        [6400, 1.16,  1.24], \
        [6150, 1.09,  1.19], \
        [5950, 1.04,  1.15], \
        [5770,  .986, 1.11], \
        [5640,  .933, 1.07], \
        [5510,  .879, 1.03], \
        [5370,  .829,  .997], \
        [5200,  .781,  .959], \
        [4930,  .738,  .925], \
        [4590,  .693,  .888], \
        [4260,  .647,  .849], \
        [3990,  .585,  .795], \
        [3700,  .454,  .676], \
        [3400,  .262,  .474], \
        [3100,  .124,  .292], \
        [2875,  .0677, .198], \
      ])

    out = nca.Nca(data)
    out.setLookup(1, "teff mass radius".split())
    return out


#T_eff		R(R_sun)		M(M_sun)

def huber():

    lines = HUBER_TEXT.split("\n")
    num = len(lines)
    data = np.empty( (num, 6))
    for i,row in enumerate(lines):
        words = row.split()
        data[i] = np.array(words).astype(float)


    out = nca.Nca(data)
    out.setLookup(1, "teff teffUnc radius radiusUnc mass massUnc".split())
    return out


def getParam(teff, param="radius", source=habetsHeinze):
    data = source()

    idx = np.argsort(data[:,'teff'])
    val = np.interp(teff, data[idx, 'teff'], data[idx, param])
    return val

import matplotlib.pyplot as mp
import apj
def main():

    sk = schmidtKaler()
    hh = habetsHeinze()
    hb = huber()

    mp.clf()
    apj.pre()
    col = 'radius'
    mp.plot(sk[:,'teff'], sk[:, col], 'o-', label="SK")
    mp.plot(hh[:,'teff'], hh[:, col], 'o-', label="HH")
    mp.plot(hb[:,'teff'], hb[:, col], 'o', label="Huber")

    mp.legend(loc=2)
    mp.xlabel("Teff")
    mp.ylabel(col)

    mp.axvline(5770, color='grey', lw=.5)
    mp.axhline(1,  color='grey', lw=.5)










HUBER_TEXT= \
    """ 5850	50	0.95	0.02	0.94	0.05
        6350	80	1.991	0.018	1.52	0.036
        5753	75	1.747	0.042	1.13	0.065
        5781	76	1.533	0.04	1.092	0.073
        5825	75	1.49	0.035	1.08	0.063
        6325	75	1.361	0.018	1.242	0.045
        5302	75	2.437	0.072	1.262	0.089
        5669	75	0.921	0.02	0.909	0.057
        5627	44	1.056	0.021	0.895	0.06
        5896	75	2.527	0.059	1.33	0.069
        6169	50	1.424	0.024	1.273	0.061
        5642	50	0.979	0.02	0.97	0.06
        6027	75	1.962	0.066	1.318	0.089
        6378	75	2.075	0.07	1.391	0.098
        5862	97	1.586	0.061	1.201	0.091
        5845	88	1.436	0.039	1.094	0.068
        5543	79	1.58	0.064	1.103	0.097
        5851	75	1.411	0.047	1.142	0.068
        5747	85	1.357	0.04	1.023	0.07
        5854	92	2.192	0.121	1.377	0.089
        5699	74	1.415	0.039	1.084	0.076
        5952	75	1.323	0.037	1.039	0.065
        5828	100	1.548	0.048	1.078	0.077
        6270	79	1.309	0.023	1.187	0.06
        5417	75	0.772	0.026	0.803	0.068
        5793	74	1.243	0.019	1.079	0.051
        6184	81	1.188	0.022	1.18	0.053
        6239	94	1.358	0.024	1.188	0.059
        6225	75	1.584	0.031	1.259	0.072
        5784	98	1.574	0.039	1.045	0.064
        6343	85	1.366	0.026	1.23	0.058
        6463	110	1.447	0.026	1.318	0.057
        5588	99	1.467	0.033	0.969	0.053
        6106	106	1.359	0.035	1.24	0.086
        5739	75	1.081	0.019	1.069	0.048
        6072	75	1.659	0.038	1.184	0.074
        5770	83	1.641	0.051	1.197	0.094
        5982	82	1.185	0.026	1.076	0.061
        5911	66	1.626	0.019	1.071	0.043
        6215	89	1.57	0.085	1.346	0.084
        6134	91	1.042	0.026	1.032	0.07
        5622	106	1.406	0.041	0.884	0.066
        5884	75	1.127	0.033	0.934	0.059
        5871	94	1.703	0.048	1.207	0.084
        6174	92	2.114	0.042	1.49	0.082
        5882	87	2.064	0.076	1.325	0.096
        6144	106	1.85	0.05	1.319	0.101
        5198	95	3.207	0.107	1.552	0.154
        6004	102	1.12	0.033	0.922	0.059
        4883	75	2.69	0.114	1.15	0.12
        6253	75	1.851	0.044	1.27	0.086
        6131	44	1.86	0.02	1.34	0.01
        5066	75	5.324	0.107	1.372	0.073
        5009	75	3.585	0.09	1.327	0.094
        4991	75	2.935	0.066	1.298	0.076
        5055	75	3.733	0.176	1.429	0.162
        5015	97	7.062	0.258	1.782	0.193
        4840	97	4.23	0.15	1.32	0.13
        6034	92	1.592	0.05	1.12	0.083
        4995	78	4.16	0.12	1.353	0.101
        5048	75	3.549	0.104	1.345	0.102
        6260	116	1.824	0.049	1.366	0.101
        6104	74	1.225	0.027	1.079	0.069
        6044	117	1.327	0.041	1.008	0.08
        6173	93	1.506	0.035	1.27	0.082
        6081	75	1.954	0.064	1.294	0.093
        6099	75	1.557	0.04	1.206	0.083
        4992	75	3.79	0.19	1.41	0.214
        5844	75	2.49	0.055	1.443	0.08
        5460	75	0.893	0.018	0.918	0.057
        5923	77	1.735	0.082	1.142	0.084
        5904	85	1.47	0.06	1.083	0.071
        4605	97	6.528	0.352	1.344	0.169
        4553	97	10.472	0.696	1.616	0.256
        6131	75	2.134	0.134	1.417	0.093
        4854	97	7.478	0.246	1.274	0.11"""
