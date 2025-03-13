import numpy as np
import pandas as pd
from service import utils

# 导入参数
def calcu_mse(file_path):
    canshu = pd.read_excel(file_path, header=None, skiprows=1).values
    print(canshu)



    Depth = canshu[:, 0]  # 井深
    WOB = canshu[:, 1]    # 钻压
    Db = canshu[:, 2]     # 直径
    RPM = canshu[:, 3]    # 转速
    ROP = canshu[:, 4]    # 机械钻速

    wob = WOB
    rpm = RPM
    rop = ROP
    u = 0.5
    # 定义变量

# **单位转换**
    WOB = WOB * 1000 / 4.448222  # 钻压单位转换（lbf 转换为 N）
    Db = Db / 25.4  # 直径单位转换（英寸转换为米）
    Ab = np.pi * (Db ** 2) / 4  # 面积计算

    # **计算扭矩**
    T = (1 / 36) * u * WOB * Db  # 扭矩计算

    # **机械钻速单位转换**
    ROP = ROP / 0.3048  # 机械钻速单位转换（英尺/小时 -> 米/小时）

    # **计算 MSE**
    # 避免除零错误：ROP 或 Ab 可能含有零，需要进行保护
    Ab_safe = np.where(Ab == 0, np.nan, Ab)  # 避免除以 0
    ROP_safe = np.where(ROP == 0, np.nan, ROP)  # 避免除以 0

    MSE = (WOB / Ab_safe) + (120 * np.pi * RPM * T / (Ab_safe * ROP_safe))

    # **单位转换为 MPa**
    MSE = MSE * 0.0068947  # (psi 转 MPa)

    # **处理 NaN 值**
    MSE = np.nan_to_num(MSE, nan=0.0)  # 若因除零产生 NaN，则替换为 0

    time = utils.get_timestamp()
    output_folder = utils.get_output_folder("MSE")
    # 保存 MSE 数据

    pd.DataFrame(MSE).to_excel( output_folder / f'MSE_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 钻压 (wob) 数据
    pd.DataFrame(wob).to_excel( output_folder /f'wob_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)


    # 保存 转速 (rpm) 数据
    pd.DataFrame(rpm).to_excel( output_folder / f'rpm_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 机械钻速 (rop) 数据
    pd.DataFrame(rop).to_excel( output_folder / f'rop_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 井深 (Depth) 数据
    pd.DataFrame(Depth).to_excel( output_folder / f'Sk_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)
        

    return Depth, WOB, rop, rpm, MSE