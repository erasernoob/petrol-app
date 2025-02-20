import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from Hydro import Hydro

matplotlib.rcParams['font.sans-serif'] = ['Ubuntu Sans']  # 适用于大多数系统
matplotlib.rcParams['axes.unicode_minus'] = False  # 避免负号显示问题


# 输入参数————————————————————————————————————————————

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(script_dir, 'KL16-1-A25井眼轨迹.xlsx')
guiji = pd.read_excel(excel_path).values  # 与 xlsread 类似

# 基本参数————————————————————————————————————————————
pailiang = 1500      # 排量，L/min
Dw = 0.2159          # 井眼直径，m
Rzz = 0.127          # 钻柱外径，m
rzz = 0.1086         # 钻柱内径，m
Lzz = 4190           # 钻柱长度，m
Rzt = 0.15875        # 钻铤外径，m
rzt = 0.07144        # 钻铤内径，m
Lzt = 10             # 钻铤长度，m

# 钻井液————————————————————————————————————————————
lbmx = 3             # 流变模式：1宾汉流体；2幂律流体；3赫巴流体
fluidden = 1170      # 钻井液密度，kg/m3
n = 0.48             # 流性指数
K = 1.09             # 稠度系数，pa·s^n
miu = 0.021          # 塑性粘度，Pa·s
taof = 14            # 屈服值，Pa

# 钻头压降————————————————————————————————————————————
A1 = 16              # 喷嘴1尺寸，mm
C1 = 7               # 喷嘴1个数
A2 = 0               # 喷嘴2尺寸，mm
C2 = 0               # 喷嘴2个数
A3 = 0               # 喷嘴3尺寸，mm
C3 = 0               # 喷嘴3个数

# 钻杆接头系数————————————————————————————————————————
Lp = 10              # 单根钻杆长度，m
Li = 0.3             # 接头长度，m
rzzjt = 0.0953       # 接头内径，m

# 地面管汇压耗————————————————————————————————————————
L1 = 30              # 地面高压管线长度，m
d1 = 0.1086          # 地面高压管线内径，m
L2 = 30              # 立管长度，m
d2 = 0.1086          # 立管内径，m
L3 = 30              # 水龙带长度，m
d3 = 0.1086          # 水龙带内径，m
L4 = 11.4            # 方钻杆长度，m
d4 = 0.0826          # 方钻杆内径，m

# 岩屑床——————————————————————————————————————————————
yx = 1               # 是否考虑岩屑：0不考虑，1考虑
yxmd = 2500          # 岩屑密度，kg/m3
H = 10               # 岩屑床高度，%




# 假设 Hydro 函数已定义并返回：
# P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk
# 请确保 Hydro 函数已正确实现，并在当前作用域内可调用

P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk = Hydro(
    guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw,
    A1, C1, A2, C2, A3, C3, Rzz, rzz, Lzz, Rzt, rzt, Lzt,
    L1, d1, L2, d2, L3, d3, L4, d4, Lp, Li, rzzjt, yxmd, H, yx)

if yx == 0:
    # 作循环压力图—————————————————————————————————————————————————————————
    # plt.figure()
    # plt.plot(Pgn, Sk, 'b-', label='钻柱')
    # plt.plot(Phk, Sk, 'r-', label='环空')
    # plt.xlabel('循环压力（MPa）')  # X轴标签
    # plt.ylabel('井深（m）')         # Y轴标签
    # plt.gca().invert_yaxis()        # Y轴反转，使井深从下到上变化
    # plt.legend(loc='lower left')    # 图例位置设置
    # plt.savefig('output1.png')
    # plt.show()

    # 导出钻柱循环压力数据——————————————————————————————————————————————————————
    pd.DataFrame(Pgn).to_excel('钻柱循环压力.xlsx', sheet_name='Sheet1', index=False)
    # 导出环空循环压力数据——————————————————————————————————————————————————————
    pd.DataFrame(Phk).to_excel('环空循环压力.xlsx', sheet_name='Sheet1', index=False)

    # 作ECD图————————————————————————————————————————————
    # plt.figure()
    # plt.plot(ECD, Sk)
    # plt.xlabel('ECD（g/cm3）')
    # plt.ylabel('井深（m）')
    # plt.gca().invert_yaxis()        # Y轴反转，使井深从下到上变化
    # # plt.show()

    # 导出ECD数据——————————————————————————————————————————————————————
    print(f"ECD:{ECD}")
    pd.DataFrame(ECD).to_excel('ECD.xlsx', sheet_name='Sheet1', index=False)

elif yx == 1:
    # 作循环压力图—————————————————————————————————————————————————————————
    # plt.figure()
    # plt.plot(Pgnyx, Sk, 'b-', label='钻柱')
    # plt.plot(Phkyx, Sk, 'r-', label='环空')
    # plt.xlabel('循环压力（MPa）')  # X轴标签
    # plt.ylabel('井深（m）')         # Y轴标签
    # plt.gca().invert_yaxis()        # Y轴反转，使井深从下到上变化
    # plt.legend(loc='lower left')    # 图例位置设置
    # plt.show()

    # 导出钻柱循环压力数据——————————————————————————————————————————————————————
    pd.DataFrame(Pgnyx).to_excel('钻柱循环压力.xlsx', sheet_name='Sheet1', index=False)
    # 导出环空循环压力数据——————————————————————————————————————————————————————
    pd.DataFrame(Phkyx).to_excel('环空循环压力.xlsx', sheet_name='Sheet1', index=False)

    # 作ECD图————————————————————————————————————————————
    # plt.figure()
    # plt.plot(ECDyx, Sk)
    # plt.xlabel('ECD（g/cm3）')
    # plt.ylabel('井深（m）')
    # plt.gca().invert_yaxis()        # Y轴反转，使井深从下到上变化
    # # plt.show()

    print(f"ECDyx:{ECDyx}")
    # 导出ECD数据——————————————————————————————————————————————————————
    pd.DataFrame(ECDyx).to_excel('ECD.xlsx', sheet_name='Sheet1', index=False)
