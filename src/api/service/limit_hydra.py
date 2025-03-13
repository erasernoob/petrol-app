import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from entity.DTO import LimitHydroDTO

from service import utils

def main(dto: LimitHydroDTO):
    # 读取井眼轨迹
    guiji = pd.read_excel(dto.file_path, header=None).values

    # 输出参数（调试用）
    print("参数初始化完成，准备进行计算...")

    P, Pyx, Plg, yssd = utils.hydro_limit_hydro(
    guiji, dto.lbmx, dto.pailiang, dto.fluidden, dto.n, dto.K, dto.miu, dto.taof,
    dto.Dw, dto.A1, dto.C1, dto.A2, dto.C2, dto.A3, dto.C3,
    dto.Rzz, dto.rzz, dto.Lzz, dto.Rzt, dto.rzt, dto.Lzt,
    dto.L1, dto.d1, dto.L2, dto.d2, dto.L3, dto.d3, dto.L4, dto.d4,
    dto.Lp, dto.Li, dto.rzzjt,
    dto.yxmd, dto.H, dto.jsjg, dto.y  # 这里按照 hydro_limit_hydro 的顺序排列
)


    output = utils.get_output_folder("水力延伸极限")
    time = utils.get_timestamp()

    if dto.y == 0:
        # # 输出立管压力图
        x_coords = np.append(dto.jsjg * np.arange(1, Plg.shape[1]), yssd)
        # 导出立管压力数据

        dataToExport = np.column_stack([x_coords, Plg[0, :]])
        df = pd.DataFrame(dataToExport, columns=['深度（m）', '立管压力（MPa）'])
        df.to_excel( output / f'立管压力_{time}.xlsx', index=False, sheet_name='Sheet1')


        # 导出总循环压耗数据
        dataToExport = np.column_stack([x_coords, P])
        df = pd.DataFrame(dataToExport, columns=['深度（m）', '总循环压耗（MPa）'])
        df.to_excel( output / f'总循环压耗_{time}.xlsx', index=False, sheet_name='Sheet1')

        return x_coords.flatten(), P.flatten(), Plg.flatten()
    elif dto.y == 1:
        # # 输出立管压力图
        # plt.figure()
        x_coords = np.append(dto.jsjg * np.arange(1, Plg.shape[1]), yssd)

        dataToExport = np.column_stack([x_coords, Plg[0, :]])
        df = pd.DataFrame(dataToExport, columns=['深度（m）', '立管压力（MPa）'])
        df.to_excel( output / f'立管压力_{time}.xlsx', index=False, sheet_name='Sheet1')


        # 导出总循环压耗数据
        dataToExport = np.column_stack([x_coords, Pyx])
        df = pd.DataFrame(dataToExport, columns=['深度（m）', '总循环压耗（MPa）'])
        df.to_excel( output / f'总循环压耗_{time}.xlsx', index=False, sheet_name='Sheet1')

        return x_coords.flatten(), Pyx.flatten(), Plg.flatten()



