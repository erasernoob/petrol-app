import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from service.curve_utils import abcfunc4
from service import utils



def main(guiji, zuanju, Holedia, ml, js):
    # 调用 abcfunc4 函数计算 fh 和 fs
    fh, fs = abcfunc4(guiji, Holedia, ml, zuanju, js)

    return fh, fs
