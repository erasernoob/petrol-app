import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from service.torque import mainfunc
from service.curve_utils import abcfunc4
from entity.DTO import LimitMechanismDTO

# 假设必要的变量已经定义，如：
# guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, max_depth, jsjg, v, omega
def limit_mecha_curve(dto: LimitMechanismDTO):
    guiji = pd.read_excel(dto.file_path1, header=None).values
    zuanju = pd.read_excel(dto.file_path2, header=None).values
    print("屈曲载荷 参数初始化完成，准备进行计算...")
    return mainfunc(guiji, zuanju, dto.wc, dto.T0, dto.rhoi, dto.Dw, dto.tgxs, dto.miua11, dto.miua22, dto.qfqd, dto.jsjg, dto.v, dto.omega, dto.ml)

def mainfunc(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, max_depth, jsjg, v, omega, ml):
        T_all = np.nan * np.ones((10, 0))  # 初始化 T_all，包含 NaN
        # 最终深度
        max_depth = int(guiji[-1, 0])
        depth = jsjg

        # 主循环
        while True:
            # 如果深度超过最大深度，将深度设置为最大深度
            if depth > max_depth:
                depth = max_depth

            _, _, _, T, M, _= mainfunc(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, depth, v, omega)

            # 确保 T_all 足够大以容纳新数据
            max_len = max(T_all.shape[0], len(T))
            if T_all.shape[0] < max_len:
                T_all = np.vstack([T_all, np.nan * np.ones((max_len - T_all.shape[0], T_all.shape[1]))])

            # 将 T 补齐 NaN 值，使其与 max_len 相同
            T = np.append(T, np.nan * np.ones(max_len - len(T)))
            T_all = np.column_stack([T_all, T])

            # 如果达到最大井深，则退出循环
            if depth == max_depth:
                break

            # 否则继续增加井深
            depth += jsjg

        # 屈曲临界载荷（计算）
        Holedia = Dw  # 井眼直径，单位：米
        js = max_depth  # 井深，单位：米
        fh, fs = abcfunc4(guiji, Holedia, ml, zuanju, js)

        # 合并数据
        T_selected = T_all[:, 1:]

        # 确保 fs 和 fh 是列向量
        fs = np.reshape(fs, (-1, 1)) if fs.ndim == 1 else fs
        fh = np.reshape(fh, (-1, 1)) if fh.ndim == 1 else fh

        # 确保长度一致
        n_rows = T_selected.shape[0]
        if len(fs) < n_rows:
            fs = np.vstack([fs, np.nan * np.ones((n_rows - len(fs), 1))])
        elif len(fs) > n_rows:
            fs = fs[:n_rows]

        if len(fh) < n_rows:
            fh = np.vstack([fh, np.nan * np.ones((n_rows - len(fh), 1))])
        elif len(fh) > n_rows:
            fh = fh[:n_rows]

        T_out = np.hstack([T_selected, fs, fh])

        # 作图
        z_axis = np.linspace(0, max_depth, n_rows)
        return T_out, z_axis

        # plt.figure()
        # for i in range(T_out.shape[1]):
        #     y = T_out[:, i]
        #     if not np.all(np.isnan(y)):
        #         plt.plot(z_axis, y)

        # plt.xlabel('井深（m）')
        # plt.ylabel('轴向力（kN）')

        # # 设置横轴使用普通数字格式
        # plt.gca().tick_params(axis='x', labelsize=12)
        # plt.xticks(np.arange(0, max_depth+1, step=100))  # 根据需要自定义

        # plt.show()
