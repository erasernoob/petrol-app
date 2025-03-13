import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from service.curve_utils import abcfunc4
from service import utils



def main(guiji, zuanju, Holedia, ml, js):
    # 调用 abcfunc4 函数计算 fh 和 fs
    fh, fs = abcfunc4(guiji, Holedia, ml, zuanju, js)

    output = utils.get_output_folder("屈曲临界载荷")
    timestamp = utils.get_timestamp()

    # 导出正弦屈曲临界载荷数据
    fs_df = pd.DataFrame(fs)
    fs_df.to_excel( output / f'正弦屈曲临界载荷_{timestamp}.xlsx', index=False, header=False)

    # 导出螺旋屈曲临界载荷数据
    fh_df = pd.DataFrame(fh)
    fh_df.to_excel( output / '螺旋屈曲临界载荷_{timestamp}.xlsx', index=False, header=False)

    return fh, fs
