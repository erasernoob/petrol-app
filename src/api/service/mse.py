import numpy as np
import pandas as pd
from service import utils

# 导入参数
def calcu_mse(file_path):
    canshu = pd.read_excel(file_path).values
    print(canshu)
    # Assign columns to variables
    Depth = canshu[:, 0]       # 井深
    WOB = canshu[:, 1]         # 钻压
    Db = canshu[:, 2]          # 直径
    RPM = canshu[:, 3]         # 转速
    ROP = canshu[:, 4]         # 机械钻速

    # Initialize variables
    wob = WOB
    rpm = RPM
    rop = ROP
    u = 0.5

    # Convert units
    WOB = WOB * 1000 / 4.448222      # 钻压单位转换
    Db = Db / 25.4                   # 直径单位转换
    Ab = np.pi * (Db ** 2) / 4       # 面积
    T = (1 / 36) * u * WOB * Db      # 扭矩
    ROP = ROP / 0.3048               # 机械钻速单位转换

    # Calculate MSE (Mechanical Specific Energy)
    MSE = (WOB / Ab) + (120 * np.pi * RPM * T / (Ab * ROP))
    MSE = MSE * 0.0068947            # 单位转换为 MPa



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