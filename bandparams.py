"""Parameters of a band: max, barycenter, width etc

It works for single bands. Works best for unimodal bands (single maximum),
but may also work for bands having side maxima in addition to the main max.
In such cases, max_pos and max_val refer to the global maximum.
FWHM determination may need to be carefully checked in such cases.
"""

import argparse
import pandas as pd
import numpy as np

def bandparams(df, colname=None):
    """Calculate band parameters: maximum, barycenter and FWHM

    Parameters:
    -----------
    df (pd.DataFrame): spectral band as dataframe indexed by energy.
    
    colname (str or None): identify the column containing the intensity;
       default: name of the first column in df.

    Returns:
    --------
    band parameters as dictionary with keys:
    'barycenter', 
    'max_pos' (position of the maximum), 
    'max_val' (the maximum value),
    'fwhm' (FwHM = full width at half maximum).

    If there are several maxima, 'max_pos' and 'max_val' refer to the global maximum.
    In such cases, one should be careful with the calculated FWHM.
    """
    yname = df.columns[0]
    max_pos = df.idxmax()[yname]
    max_val = df[yname][max_pos]
    barycenter = np.average(a=df.index, weights=df['y'])
    # FWHM
    hh = max_val / 2
    xhh = []
    initialized = False
    for x,row in df.iterrows():
        y=row['y']
        if initialized:
            if prev_y < hh and y >= hh:
                xhh.append( x + (hh - y) * (x - prev_x) / (y - prev_y) )
            elif prev_y >= hh and y < hh:
                xhh.append( x + (hh - y) * (x - prev_x) / (y - prev_y) )
        prev_x = x
        prev_y = y
        initialized = True
    fwhm = max(xhh) - min(xhh)
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
    ap.add_argument('--barycenter', '-com', '-b', action='store_const',
                        dest='only_print', const='barycenter',
                        help='only print the barycenter')
    ap.add_argument('--max_pos', '-x0', action='store_const',
                        dest='only_print', const='max_pos',
                        help='only print position of the maximum')
    ap.add_argument('--max_val', '-y0', action='store_const',
                        dest='only_print', const='max_val',
                        help='only print maximum value')
    ap.add_argument('--fhwm', '-w', action='store_const',
                        dest='only_print', const='fwhm',
                        help='only print FWHM')
    ap.add_argument('--x-digits', metavar='M', type=int, default=2,
                        help='display abscissa variable (x) with M digits')
    ap.add_argument('--y-digits', metavar='N', type=int, default=3,
                        help='display ordinate variable (y) with N digits')
    
    args = ap.parse_args()
    df = pd.read_table(args.datafile, sep='\s+', index_col=False, names=['x', 'y']).set_index('x')
    bp = bandparams(df)
    for k in bp:
        if k == 'max_val':
            digits = args.y_digits
        else:
            digits = args.x_digits
        if args.only_print is None:
            print(f"{k+':':12s} {round(bp[k],digits)}")
        elif k == args.only_print:
            print(f"{round(bp[k],digits)}")

        
