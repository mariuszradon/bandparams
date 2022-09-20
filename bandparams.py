"""Parameters of a band: max, barycenter, width etc

Assumes that the band is unimodal (single maximum)
"""

import argparse
import pandas as pd
import numpy as np

def bandparams(df):
    max_pos = df.idxmax()['y']
    max_val = df['y'][max_pos]
    barycenter = np.average(a=df.index, weights=df['y'])
    # FWHM
    hh = max_val / 2
    initialized = False
    for x,row in df.iterrows():
        y=row['y']
        if initialized:
            if prev_y < hh and y >= hh:
                x1 = x + (hh - y) * (x - prev_x) / (y - prev_y)
            elif prev_y >= hh and y < hh:
                x2 = x + (hh - y) * (x - prev_x) / (y - prev_y)
                break
        prev_x = x
        prev_y = y
        initialized = True
    fwhm = x2 - x1
    return {
        'barycenter': barycenter,
        'max_pos': max_pos,
        'fwhm': fwhm,
        'max_val': max_val,
    }

def main():
    ap = argparse.ArgumentParser('bandparams')
    ap.add_argument('datafile', metavar='DATAFILE', type=argparse.FileType('rt'),
                        help="ASCII with a band data in table format (x y)")
    ap.add_argument('--x-digits', '-x', metavar='M', type=int, default=2,
                        help='display abscissa variable (x) with M digits')
    ap.add_argument('--y-digits', '-y', metavar='N', type=int, default=3,
                        help='display ordinate variable (y) with N digits')
    
    args = ap.parse_args()
    df = pd.read_table(args.datafile, sep='\s+', index_col=False, names=['x', 'y']).set_index('x')
    bp = bandparams(df)
    for k in bp:
        if k == 'max_val':
            digits = args.y_digits
        else:
            digits = args.x_digits
        print(f"{k+':':12s} {round(bp[k],digits)}")

        
