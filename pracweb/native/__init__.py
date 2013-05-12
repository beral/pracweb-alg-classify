import os.path
import numpy as np
from numpy.ctypeslib import load_library, ndpointer
import ctypes

# Type aliases
_float1d = ndpointer(ctypes.c_double, ndim=1, flags='CONTIGUOUS')
_float2d = ndpointer(ctypes.c_double, ndim=2, flags='CONTIGUOUS')
_uint2d = ndpointer(ctypes.c_size_t, ndim=2, flags='CONTIGUOUS')
_byte2d = ndpointer(ctypes.c_uint8, ndim=2, flags='CONTIGUOUS')

_visual_lib = load_library(
    'visual',
    os.path.dirname(__file__)
)

visualize = _visual_lib.visualize
visualize.restype = None
visualize.argtypes = [
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
