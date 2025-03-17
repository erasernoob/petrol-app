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
    ROP = ROP.astype(np.float64) / 0.3048

    # 直接计算MSE（允许除零产生Inf/NaN）
    MSE = (WOB / Ab) + (120 * np.pi * RPM * T) / (Ab * ROP)
    MSE *= 0.0068947  # 单位转换




    wob = WOB
    rpm = RPM
    rop = ROP



    # 保存 MSE 数据

    output_folder = utils.get_output_folder("MSE")
    time = utils.get_timestamp()
    pd.DataFrame(MSE).to_excel( output_folder / f'MSE_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 钻压 (wob) 数据
    pd.DataFrame(wob).to_excel( output_folder /f'wob_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)


    # 保存 转速 (rpm) 数据
    pd.DataFrame(rpm).to_excel( output_folder / f'rpm_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 机械钻速 (rop) 数据
    pd.DataFrame(rop).to_excel( output_folder / f'rop_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)

    # 保存 井深 (Depth) 数据
    pd.DataFrame(Depth).to_excel( output_folder / f'Sk_{time}.xlsx', sheet_name='Sheet1', index=False, header=False)
        

    return Depth, wob, ROP, RPM, MSE