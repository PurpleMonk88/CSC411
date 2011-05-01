#!/usr/bin/env python
# Author: Carl Sandrock

import numpy

def cumf(s, f):
    """ apply a binary function to a signal in a cumulative way, using
    the accumulated value as the first argument and the signal value
    at a point as the second.  This can be used to construct other
    functions.  For instance cumf(s, lambda a, b: a+b) is the same as cumsum(s)."""
    r = numpy.zeros_like(s)
    a = s[0]
    for i, v in enumerate(s):
        a = r[i] = f(a, v)
    return r

# straight cumulative minimum - quaranteed to be below the signal and strictly descending
cummin = lambda s: cumf(s, min)
# straight cumulative maximum - quaranteed to be above the signal and strictly ascending
cummax = lambda s: cumf(s, max) 

def follow(s, xu, xd):
    """ Slightly more involved than cummin - first order movement to the signal
    xu and xd are fractions (between 0 and 1). 
    follow(s, 0, 1) is like cummin
    follow(s, 1, 0) is like cummax
    """
    r = numpy.zeros_like(s)
    envelope = r[0]
    for i, v in enumerate(s):
        if envelope < v: # move up
            envelope = envelope*(1-xu) + xu*v
        else: # move down
            envelope = envelope*(1-xd) + xd*v
        r[i] = envelope
    return r
        
if __name__=="__main__":
    import matplotlib.pyplot as pl
    x = numpy.linspace(0, 5*numpy.pi)
    y = numpy.sin(x) - x/4

    pl.plot(x, y, x, cummin(y), x, follow(y, 0.1, 0.9), x, follow(y, 0.9, 0.1))
    pl.legend(['Signal', 'cummin(y)', 'follow(y, 0.1, 0.9)', 'follow(y, 0.9, 0.1)'])
    pl.show()
