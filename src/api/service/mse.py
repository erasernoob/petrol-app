import numpy as np
import pandas as pd
from service import utils

# 导入参数
def calcu_mse(file_path):
    canshu = pd.read_excel(file_path, dtype=np.float64).values
    # 禁用除以零和无效计算的警告
    np.seterr(divide='ignore', invalid='ignore')
    # 提取数据
    Depth = canshu[:, 0]  # 井深
    WOB = canshu[:, 1]    # 钻压
    Db = canshu[:, 2]     # 直径
    RPM = canshu[:, 3]    # 转速
    ROP = canshu[:, 4]    # 机械钻速

    # 计算变量
    u = 0.5
    # 单位转换（保持与MATLAB完全相同的操作，即使存在潜在错误）
    WOB = WOB.astype(np.float64) * 1000 / 4.448222   # 注意：此处疑似单位转换方向错误
    Db = Db.astype(np.float64) / 25.4
    Ab = np.pi * (Db ** 2) / 4
    T = (1 / 36) * u * WOB * Db
    rop = ROP.astype(np.float64) / 0.3048

    # 直接计算MSE（允许除零产生Inf/NaN）
    MSE = (WOB / Ab) + (120 * np.pi * RPM * T) / (Ab * rop)
    MSE *= 0.0068947  # 单位转换

    wob = WOB
    rpm = RPM

    return Depth, wob, ROP, RPM, MSE