import numpy as np
from scipy.signal import savgol_filter



def deal_curve_data2(data1):

    return Mk,mk,Sk,alphak,phik

def deal_input_data(data):

    return Length,Xs,Ys,Zs

def deal_trank(Sk,alpha,phi):

    return Length,Xs,Ys,Zs

def diff_func(vars, span):
    vars = np.asarray(vars).flatten()  # 确保 vars 是 1D 数组
    span = np.asarray(span).flatten()

    diff_var1 = np.zeros_like(vars)

    # 计算数值导数
    for i in range(len(vars)):
        if i == 0:  # 前向差分
            diff_var1[i] = (vars[i + 1] - vars[i]) / (span[i + 1] - span[i])
        elif i == len(vars) - 1:  # 后向差分
            diff_var1[i] = (vars[-1] - vars[-2]) / (span[-1] - span[-2])
        else:  # 中心差分
            diff_var1[i] = (vars[i + 1] - vars[i - 1]) / (span[i + 1] - span[i - 1])

    # 平滑处理（等价于 MATLAB 的 smooth）
    diff_var = savgol_filter(diff_var1, window_length=101, polyorder=3, mode='nearest')  # 101 是窗口大小，可调整

    return diff_var

def prepare_data():

    
    
    
