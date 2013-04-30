#!/usr/bin/env python
# encoding: utf-8

import ctypes
from numpy.ctypeslib import load_library, ndpointer
import numpy as np
import pylab as pl

_float1d = ndpointer(ctypes.c_double, ndim=1, flags='CONTIGUOUS')
_float2d = ndpointer(ctypes.c_double, ndim=2, flags='CONTIGUOUS')
_uint2d = ndpointer(ctypes.c_size_t, ndim=2, flags='CONTIGUOUS')
_byte2d = ndpointer(ctypes.c_uint8, ndim=2, flags='CONTIGUOUS')


lib = load_library('visual', 'pracweb')

grad = lib.test_gradient
grad.restype = None
grad.argtypes = [
    ctypes.c_size_t,
    ctypes.c_size_t,
    ndpointer(ctypes.c_uint8, ndim=3, flags='CONTIGUOUS')
]

_native_visualize = lib.visualize
_native_visualize.restype = None
_native_visualize.argtypes = [
    ctypes.c_size_t,
    ctypes.c_size_t,
    _float2d,
    _float2d,
    _uint2d,
    _float1d,
    _float1d,
    _byte2d,
    _byte2d,
    _byte2d,
    _byte2d,
    _byte2d,
]


def test_visualize():
    w, h = 300, 300
    n = w * h
    k = 2
    Fprobs = np.random.rand(n, k)
    cmap = np.array(
            [[255, 0, 0], [0, 255, 0]],
            dtype=ctypes.c_double
            )

    newimg = lambda: np.empty(
        (Fprobs.shape[0], 3),
        dtype=ctypes.c_uint8
    )
    toimg = lambda v: v.reshape((h, w, 3))

    viz_argmax = newimg()
    viz_intensity = newimg()
    viz_linspace = newimg()
    viz_linspace_clamped = newimg()
    viz_diff = newimg()

    print 'calling native code'
    _native_visualize(
        Fprobs.shape[0],
        Fprobs.shape[1],
        Fprobs,
        cmap,
        np.empty((Fprobs.shape[0], 2), dtype=ctypes.c_size_t),  # argmaxs
        np.empty(Fprobs.shape[1], dtype=ctypes.c_double),  # diff_norms
        np.empty(Fprobs.shape[1], dtype=ctypes.c_double),  # ks
        viz_argmax,
        viz_intensity,
        viz_linspace,
        viz_linspace_clamped,
        viz_diff,
    )
    print 'native code returned'
    pl.imshow(toimg(viz_argmax))
    pl.show()


def test_gradient():
    w, h = 300, 300
    img = np.empty((w, h, 3), dtype=ctypes.c_uint8)
    grad(w, h, img)

    pl.imshow(img)
    pl.show()


if __name__ == '__main__':
    test_visualize()
