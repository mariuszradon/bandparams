"""Parameters of a band: max, barycenter, width etc

It works for single bands. Works best for unimodal bands (single maximum),
but may also work for bands having side maxima in addition to the main max.
In such cases, max_pos and max_val refer to the global maximum.
FWHM determination may need to be carefully checked in such cases.
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

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

def read_spc(filepath_or_buffer):
    """Read spectrum from file and return dataframe
    
    Parameters:
    -----------
    filepath_or_buffer : str, path object or file-like object
             file to read

    Returns:
    --------
    DataFrame
          spectrum as dataframe with column names 'x' and 'y'
    """
    return pd.read_table(
        filepath_or_buffer,
        sep='\s+', index_col=False, names=['x', 'y']).set_index('x')


def main():
    ap = argparse.ArgumentParser('bandparams')
    ap.add_argument('datafile', metavar='DATAFILE', type=argparse.FileType('rt'),
                        help="ASCII with a band data in table format (x y)")
    ap.add_argument('--barycenter', '-com', '-b', '-bc', action='store_const',
                        dest='only_print', const='barycenter',
                        help='only print the barycenter')
    ap.add_argument('--max-pos', '--max_pos', '-x0', action='store_const',
                        dest='only_print', const='max_pos',
                        help='only print position of the maximum')
    ap.add_argument('--max-val', '--max_val', '-y0', action='store_const',
                        dest='only_print', const='max_val',
                        help='only print maximum value')
    ap.add_argument('--fwhm', '-w', action='store_const',
                        dest='only_print', const='fwhm',
                        help='only print FWHM')
    ap.add_argument('--format-x', metavar='FORMAT', type=str, default='.4f',
                        help='format for printing the abscissa variable (x)')
    ap.add_argument('--format-y', metavar='FORMAT', type=str, default='.4e',
                        help='format for printing the ordinate variable (y)')
    
    args = ap.parse_args()
    df = read_spc(args.datafile)
    bp = bandparams(df)
    for k in bp:
        if k == 'max_val':
            fmt = args.format_y
        else:
            fmt = args.format_x
        if args.only_print is None:
            print(f"{k+':':12s} {format(bp[k],fmt)}")
        elif k == args.only_print:
            print(f"{format(bp[k],fmt)}")

        
