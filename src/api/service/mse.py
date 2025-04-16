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
    
    wob = WOB

    # 计算变量
    u = 0.5
    # 单位转换（保持与MATLAB完全相同的操作，即使存在潜在错误）
    wob = wob.astype(np.float64) * 1000 / 4.448222   # 注意：此处疑似单位转换方向错误
    Db = Db.astype(np.float64) / 25.4
    Ab = np.pi * (Db ** 2) / 4
    T = (1 / 36) * u * wob * Db
    rop = ROP.astype(np.float64) / 0.3048

    # 直接计算MSE（允许除零产生Inf/NaN）
    MSE = (wob / Ab) + (120 * np.pi * RPM * T) / (Ab * rop)
    MSE *= 0.0068947  # 单位转换
    
    wob_res, rpm_res, rop_res  = "", "", ""
    UCS = []
    
    if canshu.shape[1] == 6:
        UCS = canshu[:, 5]
        wob_res, rpm_res, rop_res = extra_optimized(UCS, MSE, Depth, WOB, ROP, RPM)
    return Depth, WOB, ROP, RPM, MSE, UCS, wob_res, rpm_res, rop_res


def extra_optimized(UCS, MSE, Depth, wob, rop, rpm):
    UCS_max = np.max(UCS)
    
    wob_res, rpm_res, rop_res  = "", "", ""

    # 找出所有大于最大岩石抗压强度的 MSE
    idx = np.where(MSE > UCS_max)[0]

    if len(idx) == 0:
        wob_res = '建议增大钻压'
        rpm_res = '建议增大转速'
        rop_res = '建议减小机械钻速'
    else:
        # 找出大于最大岩石抗压强度的最小 MSE 值及对应的参数值
        MSE_selected = MSE[idx]
        n_selected = len(MSE_selected)
        
        if n_selected >= 50:
            n_top = int(np.ceil(0.05 * n_selected))
            sort_idx = np.argsort(MSE_selected)
            top_idx = idx[sort_idx[:n_top]]
        else:
            top_idx = idx
            n_top = n_selected

        # 提取相关参数
        bot_MSE = MSE[top_idx]
        bot_Depth = Depth[top_idx]
        bot_WOB = wob[top_idx]
        bot_RPM = rpm[top_idx]
        bot_ROP = rop[top_idx]

        # 找出大于最大岩石抗压强度的最大机械钻速值及对应的参数值
        ROP_selected = rop[idx]
        m_selected = len(ROP_selected)
        
        if m_selected >= 50:
            n_top = int(np.ceil(0.05 * m_selected))
            sort_idx = np.argsort(ROP_selected)[::-1]
            top_idx = idx[sort_idx[:n_top]]
        else:
            top_idx = idx
            n_top = m_selected

        # 提取对应的参数值
        top_ROP = rop[top_idx]
        top_Depth = Depth[top_idx]
        top_WOB = wob[top_idx]
        top_RPM = rpm[top_idx]
        top_MSE = MSE[top_idx]

        # 找出最小 MSE 和最大机械钻速中的重复 MSE 值
        common_MSE_values = np.intersect1d(np.unique(bot_MSE), np.unique(top_MSE))

        # 初始化容器
        all_bot_MSE = []
        all_bot_WOB = []
        all_bot_RPM = []
        all_bot_ROP = []
        all_top_MSE = []
        all_top_WOB = []
        all_top_RPM = []
        all_top_ROP = []

        if len(common_MSE_values) > 0:
            for val in common_MSE_values:
                idx_bot = np.where(np.abs(bot_MSE - val) < 1e-6)[0]
                all_bot_MSE.extend(bot_MSE[idx_bot])
                all_bot_WOB.extend(bot_WOB[idx_bot])
                all_bot_RPM.extend(bot_RPM[idx_bot])
                all_bot_ROP.extend(bot_ROP[idx_bot])
                
                idx_top = np.where(np.abs(top_MSE - val) < 1e-6)[0]
                all_top_MSE.extend(top_MSE[idx_top])
                all_top_WOB.extend(top_WOB[idx_top])
                all_top_RPM.extend(top_RPM[idx_top])
                all_top_ROP.extend(top_ROP[idx_top])
        else:
            all_bot_MSE = bot_MSE
            all_bot_WOB = bot_WOB
            all_bot_RPM = bot_RPM
            all_bot_ROP = bot_ROP
            all_top_MSE = bot_MSE
            all_top_WOB = bot_WOB
            all_top_RPM = bot_RPM
            all_top_ROP = bot_ROP

        # 最优钻压
        merged_WOB = np.concatenate([all_bot_WOB, all_top_WOB])
        min_WOB = np.min(merged_WOB)
        max_WOB = np.max(merged_WOB)
        if np.abs(min_WOB - max_WOB) < 1e-6:
            optimal_WOB = f'{min_WOB:.2f} kN'
        else:
            optimal_WOB = f'{min_WOB:.2f} ~ {max_WOB:.2f} kN'

        # 最优转速
        merged_RPM = np.concatenate([all_bot_RPM, all_top_RPM])
        min_RPM = np.min(merged_RPM)
        max_RPM = np.max(merged_RPM)
        if np.abs(min_RPM - max_RPM) < 1e-6:
            optimal_RPM = f'{min_RPM:.1f} RPM'
        else:
            optimal_RPM = f'{min_RPM:.1f} ~ {max_RPM:.1f} RPM'

        # 最优机械钻速
        merged_ROP = np.concatenate([all_bot_ROP, all_top_ROP])
        min_ROP = np.min(merged_ROP)
        max_ROP = np.max(merged_ROP)
        if np.abs(min_ROP - max_ROP) < 1e-6:
            optimal_ROP = f'{min_ROP:.2f} m/h'
        else:
            optimal_ROP = f'{min_ROP:.2f} ~ {max_ROP:.2f} m/h'


        wob_res = f'{optimal_WOB}'
        rpm_res = f'{optimal_RPM}'
        rop_res = f'{optimal_ROP}'
        print(wob_res)
        print(rpm_res)
        print(rop_res)

        return wob_res, rpm_res, rop_res
