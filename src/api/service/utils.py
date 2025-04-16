import numpy as np
import datetime
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline
from numpy.linalg import solve
from pathlib import Path
import os
import pandas as pd
from service import utils
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, splrep, splev, UnivariateSpline, CubicSpline
from scipy.signal import savgol_filter

def get_output_folder(prefix):
    if os.name == 'nt':  # Windows
        download_folder =  Path(os.environ['USERPROFILE']) / 'Downloads'
        output_folder = download_folder / prefix
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        return output_folder
    elif os.name == 'posix':  # macOS/Linux
        return Path.home() / 'Downloads'
    else:
        raise Exception("Unsupported OS")

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    




def hydro_limit_eye(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, yx, yxmd, H):
    """Main hydraulic calculation function"""
    data = guiji
    wc = lbmx
    Q = pailiang / 1000 / 60  # Flow rate, m³/s
    Ql = pailiang / 60  # Flow rate, L/s
    rhoi = fluidden  # Drilling fluid density, kg/m³
    rhoo = fluidden / 1000  # Drilling fluid density, kg/L
    g = 9.81

    # Drill pipe and drill collar dimensions
    Rt = Rzz / 2  # Drill pipe outer radius, m
    rt = rzz / 2  # Drill pipe inner radius, m
    Rtzt = Rzt / 2  # Drill collar outer radius, m
    rtzt = rzt / 2  # Drill collar inner radius, m

    # Convert to cm for some equations
    Dwcm = Dw * 100  # Wellbore diameter, cm
    Rzzcm = Rzz * 100  # Drill pipe outer diameter, cm
    rzzcm = rzz * 100  # Drill pipe inner diameter, cm
    Rztcm = Rzt * 100  # Drill collar outer diameter, cm
    rztcm = rzt * 100  # Drill collar inner diameter, cm

    ntrans = round(data[-1, 0])

    # Static hydrostatic pressure calculation
    ds = 1
    length = ntrans - 1
    nt = length / ds
    sspan = np.arange(0, length + 1, ds)
    SW = sspan.reshape(-1, 1)

    Mk, mk, Sk, alphak, phik = utils.deal_curve_data2(data)
    Mk = Mk.reshape(-1, 1)
    mk = mk.reshape(-1, 1)
    Sk = Sk.reshape(-1, 1)
    alphak = alphak.reshape(-1, 1)
    phik = phik.reshape(-1, 1)

    alpha, phi, ks, dks, ddks, kphis, kalphas, taos = utils.prepare_data(sspan, Mk, mk, Sk, alphak, phik)

    # 假设 ntrans 是一个整数，alpha 是一维数组，rhoi、g、Q、rt、Dw、Rt、rtzt、Rtzt 均为标量
    PI1 = np.zeros((ntrans, 1))
    PO1 = np.zeros((ntrans, 1))
    PI2 = np.zeros((ntrans, 1))
    PO2 = np.zeros((ntrans, 1))

    for i in range(ntrans):
        # MATLAB 中 alpha(ntrans-i+1) 对应 Python 的 alpha[ntrans-i-1]
        PI1[i, 0] = rhoi * g * np.cos(alpha[ntrans - i - 1])
        PO1[i, 0] = rhoi * g * np.cos(alpha[ntrans - i - 1])

    PI2[0, 0] = PI1[0, 0]
    PO2[0, 0] = PO1[0, 0]
    for i in range(1, ntrans):
        PI2[i, 0] = PI2[i - 1, 0] + PI1[i, 0]
        PO2[i, 0] = PO2[i - 1, 0] + PO1[i, 0]

    # 管内静液柱压力和环空静液柱压力
    PI2 = (PI2 - 9.81 * rhoi) / (10 ** 6)
    PO2 = (PO2 - 9.81 * rhoi) / (10 ** 6)

    # 流速计算
    # 钻柱井段
    Vp = Q / (np.pi * rt ** 2)  # 管内流速
    Va = 4 * Q / (np.pi * (Dw ** 2 - 4 * Rt ** 2))  # 环空流速

    # 钻铤井段
    Vpzt = Q / (np.pi * rtzt ** 2)  # 管内流速
    Vazt = 4 * Q / (np.pi * (Dw ** 2 - 4 * Rtzt ** 2))  # 环空流速

    if wc == 1:  # 宾汉流体
        # 钻柱井段
        # 管内雷诺数
        Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
        # 环空雷诺数
        Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))
        # 管内压降
        if Repzz < 2000:
            Ppzz = 40.7437 * miu * np.arange(1, Lzz + 1) * Ql / rzzcm ** 4 + taof * np.arange(1, Lzz + 1) / (
                    187.5 * rzzcm)
        else:
            Ppzz = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzz + 1) * Ql ** 1.8 / rzzcm ** 4.8
        # 环空压降
        if Reazz < 2000:
            Pazz = (61.1155 * miu * np.arange(1, Lzz + 1) * Ql / ((Dwcm - Rzzcm) ** 3 * (Dwcm + Rzzcm)) +
                    6e-3 * taof * np.arange(1, Lzz + 1) / (Dwcm - Rzzcm))
        else:
            Pazz = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzz + 1) * Ql ** 1.8 / (
                    (Dwcm - Rzzcm) ** 3 * (Dwcm + Rzzcm) ** 1.8)

        # 钻铤井段
        # 管内雷诺数
        Repzt = rhoi * rzt * Vpzt / miu / (1 + taof * rzt / (6 * miu * Vpzt))
        # 环空雷诺数
        Reazt = rhoi * (Dw - Rzt) * Vazt / miu / (1 + taof * (Dw - Rzt) / (8 * miu * Vazt))
        # 管内压降
        if Repzt < 2000:
            Ppzt = 40.7437 * miu * np.arange(1, Lzt + 1) * Ql / rztcm ** 4 + taof * np.arange(1, Lzt + 1) / (
                    187.5 * rztcm)
        else:
            Ppzt = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / rztcm ** 4.8
        # 环空压降
        if Reazt < 2000:
            Pazt = (61.1155 * miu * np.arange(1, Lzt + 1) * Ql / ((Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm)) +
                    6e-3 * taof * np.arange(1, Lzt + 1) / (Dwcm - Rztcm))
        else:
            Pazt = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / (
                    (Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm) ** 1.8)

    elif wc == 2:  # 幂律流体
        # 钻柱井段
        # 管内雷诺数
        Repzz = rhoi * rzz ** n * Vp ** (2 - n) / (8 ** (n - 1)) / K / (((3 * n + 1) / (4 * n)) ** n)
        # 环空雷诺数
        Reazz = rhoi * (Dw - Rzz) ** n * Va ** (2 - n) / (12 ** (n - 1)) / K / (((2 * n + 1) / (3 * n)) ** n)
        # 管内压降
        if Repzz < 2000:
            Ppzz = (((8000 * (3 * n + 1) * Ql) / (np.pi * n * rzzcm ** 3)) ** n) * np.arange(1,
                                                                                             Lzz + 1) * K / 250 / rzzcm
        else:
            Ppzz = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzz + 1) * Ql ** 1.8 / rzzcm ** 4.8
        # 环空压降
        if Reazz < 2000:
            Pazz = (((16000 * (2 * n + 1) * Ql) / (np.pi * n * (Dwcm - Rzzcm) ** 2 * (Dwcm + Rzzcm))) ** n) * np.arange(
                1, Lzz + 1) * K / 250 / (Dwcm - Rzzcm)
        else:
            Pazz = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzz + 1) * Ql ** 1.8 / (
                    (Dwcm - Rzzcm) ** 3 * (Dwcm + Rzzcm) ** 1.8)

        # 钻铤井段
        # 管内雷诺数
        Repzt = rhoi * rzt ** n * Vpzt ** (2 - n) / (8 ** (n - 1)) / K / (((3 * n + 1) / (4 * n)) ** n)
        # 环空雷诺数
        Reazt = rhoi * (Dw - Rzt) ** n * Vazt ** (2 - n) / (12 ** (n - 1)) / K / (((2 * n + 1) / (3 * n)) ** n)
        # 管内压降
        if Repzt < 2000:
            Ppzt = (((8000 * (3 * n + 1) * Ql) / (np.pi * n * rztcm ** 3)) ** n) * np.arange(1,
                                                                                             Lzt + 1) * K / 250 / rztcm
        else:
            Ppzt = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / rztcm ** 4.8
        # 环空压降
        if Reazt < 2000:
            Pazt = (((16000 * (2 * n + 1) * Ql) / (np.pi * n * (Dwcm - Rztcm) ** 2 * (Dwcm + Rztcm))) ** n) * np.arange(
                1, Lzt + 1) * K / 250 / (Dwcm - Rztcm)
        else:
            Pazt = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / (
                    (Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm) ** 1.8)

    elif wc == 3:  # 赫巴流体
        gammaaa = 8 * Va / (Dw - Rzz)
        miueffa = K * (8 * Va / (Dw - Rzz)) ** (n - 1) + taof / gammaaa
        Reazz = rhoi * Va * (Dw - Rzz) / miueffa
        gammaazt = 8 * Vazt / (Dw - Rzt)
        miueffazt = K * (8 * Vazt / (Dw - Rzt)) ** (n - 1) + taof / gammaazt
        Reazt = rhoi * Vazt * (Dw - Rzt) / miueffazt

        # 环空——单位转换
        Qhb = Q * 15850.32
        dp = Rzz * 39.3701
        dpzt = Rzt * 39.3701
        dh = Dw * 39.3701
        Khb = K * 2.0885
        taofhb = taof * 2.0885
        rhoihb = rhoi * 0.008345

        # 钻柱井段——环空
        Vahb = 24.51 * Qhb / (dh ** 2 - dp ** 2)
        Baa = 1.5 * (2 * n + 1) / (3 * n)
        Gfa = Baa
        gammaa = 1.6 * Gfa * Vahb / (dh - dp)
        taova = (3 / 2) ** n * taofhb + Khb * gammaa ** n
        taowa = 1.067 * taova
        NReGa = rhoihb * Vahb ** 2 / (19.36 * taowa)
        NcRe = 3470 - 1370 * n
        flama = 16 / NReGa
        ftransa = 16 * NReGa / (NcRe ** 2)
        a_val = (np.log10(n) + 3.93) / 50
        b_val = (1.75 - np.log10(n)) / 7
        fturba = a_val / (NReGa ** b_val)
        finta = (ftransa ** (-8) + fturba ** (-8)) ** (-1 / 8)
        fa = (finta ** 12 + flama ** 12) ** (1 / 12)
        Pazz = 1.076 * rhoihb * Vahb ** 2 * fa * np.arange(1, Lzz + 1) / (10 ** 5 * (dh - dp))
        Pazz = Pazz * 6.894757 / 1000 * 10

        # 钻铤井段——环空
        Vahbzt = 24.51 * Qhb / (dh ** 2 - dpzt ** 2)
        Baazt = 1.5 * (2 * n + 1) / (3 * n)
        Gfazt = Baazt
        gammaazt = 1.6 * Gfazt * Vahbzt / (dh - dpzt)
        taovazt = (3 / 2) ** n * taofhb + Khb * gammaazt ** n
        taowazt = 1.067 * taovazt
        NReGazt = rhoihb * Vahb ** 2 / (19.36 * taowazt)  # 注意这里使用 Vahb**2，与原代码一致
        NcRezt = 3470 - 1370 * n
        flamazt = 16 / NReGazt
        ftransazt = 16 * NReGazt / (NcRezt ** 2)
        a_val = (np.log10(n) + 3.93) / 50  # 重新计算 a_val, b_val（若需要可复用前面结果）
        b_val = (1.75 - np.log10(n)) / 7
        fturbazt = a_val / (NReGazt ** b_val)
        fintazt = (ftransazt ** (-8) + fturbazt ** (-8)) ** (-1 / 8)
        fazt = (fintazt ** 12 + flamazt ** 12) ** (1 / 12)
        Pazt = 1.076 * rhoihb * Vahbzt ** 2 * fazt * np.arange(1, Lzt + 1) / (10 ** 5 * (dh - dpzt))
        Pazt = Pazt * 6.894757 / 1000 * 10

        # 管内计算
        # 钻柱井段——管内
        gammap = 8 * Vp / rzz
        miueffp = K * (8 * Vp / rzz) ** (n - 1) + taof / gammap
        Repzz = rhoi * Vp * rzz / miueffp
        if Repzz < 2000:
            Ppzz = (2 * taof * np.arange(1, Lzz + 1) / rzz +
                    2 * n * np.arange(1, Lzz + 1) * K * Q ** n / (n + 1) / (np.pi * rt ** 2) ** n) / 10 ** 5
        else:
            Ppzz = (0.316 / Repzz ** 0.25 * np.arange(1, Lzz + 1) * rhoi * Vp ** 2 / rzz / 2) / 10 ** 5

        # 钻铤井段——管内
        gammapzt = 8 * Vpzt / rzt
        miueffpzt = K * (8 * Vpzt / rzt) ** (n - 1) + taof / gammapzt
        Repzt = rhoi * Vpzt * rzt / miueffpzt
        if Repzt < 2000:
            Ppzt = (2 * taof * np.arange(1, Lzt + 1) / rzt +
                    2 * n * np.arange(1, Lzt + 1) * K * Q ** n / (n + 1) / (np.pi * rtzt ** 2) ** n) / 10 ** 5
        else:
            Ppzt = (0.316 / Repzt ** 0.25 * np.arange(1, Lzt + 1) * rhoi * Vpzt ** 2 / rzt / 2) / 10 ** 5

    # Combine drill collar pressure with drill pipe pressure
    Paztt = Pazz[-1] + Pazt  # 利用广播机制，将 Pazz[-1]（标量）加到 Pazt 的每个元素上
    Paa = np.concatenate((Pazz, Paztt), axis=0)  # 垂直拼接两个数组
    Pa = Paa / 10.0  # 除以 10

    # Interpolate vertical depth
    Length, Xs, Ys, Zs = utils.deal_input_data(data)

    # 计算 cs = Xs[0] - Xs
    cs = Xs[0] - Xs

    # 提取 aa（data 的第一列）
    aa = data[:, 0]

    # T 等于 cs
    T = cs.copy()  # 使用副本以确保数据不变

    # 生成 aacs，从 1 到 max(aa) 的整数数组
    max_aa = int(np.round(np.max(aa)))  # 确保 max_aa 为整数
    aacs = np.arange(1, max_aa + 1)

    # 检查 aa 是否单调递增，MATLAB 中 interutils 要求输入数据单调递增
    if not np.all(np.diff(aa) >= 0):
        # 需要排序并保持对应关系
        sort_idx = np.argsort(aa)
        aa_sorted = aa[sort_idx]
        T_sorted = T[sort_idx]
    else:
        aa_sorted = aa
        T_sorted = T

    # 使用 CubicSpline 进行三次样条插值
    cubic_spline = CubicSpline(aa_sorted, T_sorted)

    # 计算插值结果
    Tcs = cubic_spline(aacs)

    if yx == 0:
        # 当 yx == 0 时，直接计算 ECD 与 ECDyx

        if Dw <= 0.3:
            if wc == 1:
                ccc = 0.885
            elif wc == 2:
                ccc = 1.045
            elif wc == 3:
                ccc = 1.382
        elif Dw > 0.3:
            if wc == 1:
                ccc = 0.88
            elif wc == 2:
                ccc = 1.01
            elif wc == 3:
                ccc = 1.1


        ECD = ccc * Pa * 10 ** 6 / 9.81 / 1000 / Tcs + rhoi / 1000
        ECDyx = 0
    elif yx == 1:
        # 考虑岩屑的环空压耗
        S = yxmd / rhoi

        # 钻柱井段
        if Reazz < 2000:
            fd = 64 / Reazz
        else:
            fd = 0.316 / (Reazz ** 0.25)
        # 注意：MATLAB 中的 ".*" 表示逐元素乘法，这里假设 H 和 Pazz 均为 NumPy 数组
        term1 = (Va ** 2) / g / (Dw - Rzz) / (S - 1)
        Payxzz = (0.026068625 * H * Pazz / 10 / fd *
                  (term1 ** (-1.25)) +
                  (1 + 0.00581695 * H) * Pazz / 10)

        # 钻铤井段
        if Reazt < 2000:
            fdzt = 64 / Reazt
        else:
            fdzt = 0.316 / (Reazt ** 0.25)
        term2 = (Vazt ** 2) / g / (Dw - Rzt) / (S - 1)
        Payxzt = (0.026068625 * H * Pazt / 10 / fdzt *
                  (term2 ** (-1.25)) +
                  (1 + 0.00581695 * H) * Pazt / 10)

        # Payxzz(end) 表示 Payxzz 的最后一个元素，加上 Payxzt 后得到 Payxztt
        Payxztt = Payxzz[-1] + Payxzt

        # MATLAB 中 [Payxzz; Payxztt] 是垂直拼接（按行堆叠）
        # 如果 Payxzz 与 Payxztt 均为 1D 数组，则使用 np.vstack 保证维度一致
        # TODO注意这里是
        Payx = np.vstack((Payxzz.reshape(-1, 1), Payxztt.reshape(-1, 1))).flatten()

        
        if Dw <= 0.3:
            if wc == 1:
                ccc = 0.885
            elif wc == 2:
                ccc = 1.045
            elif wc == 3:
                ccc = 1.382
        elif Dw > 0.3:
            if wc == 1:
                ccc = 0.88
            elif wc == 2:
                ccc = 1.01
            elif wc == 3:
                ccc = 1.1

        # 考虑岩屑的 ECD（同样保证逐元素运算）
        ECDyx = ccc * Payx * 10 ** 6 / 9.81 / 1000 / Tcs + rhoi / 1000
        ECD = 0

    return ECD, ECDyx, aacs


def smooth(x, window_len):
    """Apply smoothing filter to data"""
    if len(x) < window_len:
        return x
    return savgol_filter(x, min(window_len, len(x) - (1 if len(x) % 2 == 0 else 0)), 3)


def diff_func(vars_data, span):
    """Calculate derivatives with smoothing"""
    diff_var1 = np.zeros_like(vars_data)
    n = len(vars_data)

    for i in range(n):
        if i == 0:
            diff_var1[i] = (vars_data[i + 1] - vars_data[i]) / (span[i + 1] - span[i])
        elif i == n - 1:
            diff_var1[i] = (vars_data[-1] - vars_data[-2]) / (span[-1] - span[-2])
        else:
            diff_var1[i] = (vars_data[i + 1] - vars_data[i - 1]) / (span[i + 1] - span[i - 1])

    # Smooth the derivatives
    window_len = min(100, n // 2)
    if window_len % 2 == 0:
        window_len += 1  # Ensure window length is odd
    if window_len > 2:
        diff_var = smooth(diff_var1, window_len)
    else:
        diff_var = diff_var1

    return diff_var


def spline_interp(Mk, mk, Sk, alphak, phik, S0):
    """Spline interpolation for well trajectory"""
    np_points = len(Mk)

    if S0 >= Sk[-1]:
        iter_point = np_points - 2
    else:
        iter_point = 0
        for i in range(np_points - 1):
            if S0 >= Sk[i] and S0 < Sk[i + 1]:
                iter_point = i
                break

    if S0 < min(Sk):
        iter_point = 0

    M0 = Mk[iter_point]
    M1 = Mk[iter_point + 1]
    m0 = mk[iter_point]
    m1 = mk[iter_point + 1]
    alpha0 = alphak[iter_point]
    alpha1 = alphak[iter_point + 1]
    phi0 = phik[iter_point]
    phi1 = phik[iter_point + 1]
    Sr = Sk[iter_point + 1]
    Sl = Sk[iter_point]
    Lk = Sk[iter_point + 1] - Sk[iter_point]

    C1 = alpha1 / Lk - M1 * Lk / 6
    C0 = alpha0 / Lk - M0 * Lk / 6
    c1 = phi1 / Lk - m1 * Lk / 6
    c0 = phi0 / Lk - m0 * Lk / 6

    alphacal = M0 * (Sr - S0) ** 3 / (6 * Lk) + M1 * (S0 - Sl) ** 3 / (6 * Lk) + C1 * (S0 - Sl) + C0 * (Sr - S0)
    phical = m0 * (Sr - S0) ** 3 / (6 * Lk) + m1 * (S0 - Sl) ** 3 / (6 * Lk) + c1 * (S0 - Sl) + c0 * (Sr - S0)

    return alphacal, phical


def deal_curve_data2(data1, js=""):
    # ------------------------------
    # 1. 去除井眼轨迹中的重复值，并按第一列升序排序
    # MATLAB:
    #   sortedData = sortrows(round(data1), 1);
    #   [~, uniqueIndices] = unique(sortedData(:, 1), 'stable');
    #   data = sortedData(uniqueIndices, :);
    #
    # Python实现：
    rounded_data = np.round(data1)  # 对整个数组进行四舍五入
    sorted_indices = np.argsort(rounded_data[:, 0])
    sorted_data = rounded_data[sorted_indices]

    # 获取第一列唯一值的索引（保持顺序稳定）
    _, unique_indices = np.unique(sorted_data[:, 0], return_index=True)
    # 为确保顺序与 MATLAB 保持一致，排序 unique_indices
    unique_indices_sorted = np.sort(unique_indices)
    data = sorted_data[unique_indices_sorted, :]

    # ------------------------------
    # 2. 读取数据并初始化
    # MATLAB:
    #   S = round(data(:,1));
    #   alphaa = data(:,2);
    #   phia = data(:,3);
    #   n = round(S(end));
    #   alphas = zeros(n,1);
    #   phis = zeros(n,1);
    #
    S = np.round(data[:, 0])
    alphaa = data[:, 1]
    phia = data[:, 2]
    if js != "":
        n = int(js)
    else:
        n = int(np.round(S[-1]))  # MATLAB S(end)为最后一个元素

    # 初始化插值结果（1D数组，共 n 个点）
    alphas = np.zeros(n)
    phis = np.zeros(n)

    # ------------------------------
    # 3. 使用三次样条对 alphaa 和 phia 进行插值
    # MATLAB中 for i=1:n, alphas(i)=abs(interp1(S, alphaa, i, 'spline'));
    x_eval = np.arange(1, n + 1)  # 生成1到n的整数点

    # 构建三次样条插值器
    spline_alpha = make_interp_spline(S, alphaa, k=3)
    spline_phi = make_interp_spline(S, phia, k=3)

    alphas = np.abs(spline_alpha(x_eval))
    phis = np.abs(spline_phi(x_eval))

    # 对结果取模360
    alphas = np.mod(alphas, 360)
    phis = np.mod(phis, 360)

    # ------------------------------
    # 4. 重构 S、alpha、phi，并进行后续计算
    # MATLAB:
    #   S = (1:1:n)';  alpha = alphas; phi = phis;
    #   np = numel(S);
    #
    S = np.arange(1, n + 1)
    alpha = alphas.copy()
    phi = phis.copy()
    np_pts = S.size  # 点数目

    # 初始化 A, D1, D2
    A = np.zeros((np_pts, np_pts))
    D1 = np.zeros(np_pts)
    D2 = np.zeros(np_pts)

    # 计算相邻点之间的距离（Ls）
    Ls = S[1:] - S[:-1]  # 长度 np_pts-1 的向量

    # 翻转 alpha 和 phi，并转换为弧度
    alpha = np.flipud(alpha) * np.pi / 180
    phi = np.flipud(phi) * np.pi / 180

    # ------------------------------
    # 5. 循环计算 A 矩阵和 D1、D2
    # MATLAB的 for i = 2:np-1 对应 Python 的 i 从 1 到 np_pts-2（0-indexed）
    for i in range(1, np_pts - 1):
        Lk0 = Ls[i - 1]
        Lk1 = Ls[i]

        alphak1 = alpha[i + 1]
        alphak0 = alpha[i]
        alphak00 = alpha[i - 1]
        phik1 = phi[i + 1]
        phik0 = phi[i]
        phik00 = phi[i - 1]

        D1[i] = 6 / (Lk0 + Lk1) * (((alphak1 - alphak0) / Lk1) - ((alphak0 - alphak00) / Lk0))
        D2[i] = 6 / (Lk0 + Lk1) * (((phik1 - phik0) / Lk1) - ((phik0 - phik00) / Lk0))

        lamk = Lk1 / (Lk0 + Lk1)
        miuk = 1 - lamk
        # 设置 A[i, i-1:i+2] 对应 [miuk, 2, lamk]
        A[i, i - 1:i + 2] = [miuk, 2, lamk]

    # ------------------------------
    # 6. 求解 Mk 和 mk
    # MATLAB:
    #   Mk = zeros(np,1);
    #   mk = zeros(np,1);
    #   Mk(2:end-1) = A(2:end-1,2:end-1) \ D1(2:end-1);
    #   mk(2:end-1) = A(2:end-1,2:end-1) \ D2(2:end-1);
    #
    Mk = np.zeros(np_pts)
    mk = np.zeros(np_pts)

    if np_pts > 2:  # 保证有内部点可供求解
        # Python中 A[1:-1,1:-1] 对应 MATLAB 的 A(2:end-1,2:end-1)
        Mk[1:-1] = solve(A[1:-1, 1:-1], D1[1:-1])
        mk[1:-1] = solve(A[1:-1, 1:-1], D2[1:-1])

    # ------------------------------
    # 7. 设置输出
    Sk = S.copy()  # 轨迹的横坐标
    alphak = alpha.copy()  # 角度（已转换为弧度并翻转）
    phik = phi.copy()

    return Mk, mk, Sk, alphak, phik


def prepare_data(sspan, Mk, mk, Sk, alphak, phik):
    """Prepare well trajectory data for hydraulic calculations"""
    alphas = np.zeros(len(sspan))
    phis = np.zeros(len(sspan))
    taos = np.zeros(len(sspan)).reshape(-1, 1)

    # Interpolate values along the trajectory
    for i in range(len(sspan)):
        alphas[i], phis[i] = spline_interp(Mk, mk, Sk, alphak, phik, sspan[i])

    # Calculate curvature parameters
    kphis = diff_func(phis, sspan).reshape(-1, 1)
    kalphas = diff_func(alphas, sspan).reshape(-1, 1)

    # 将数组展平成 1D 向量
    kphis_flat = kphis.flatten()
    kalphas_flat = kalphas.flatten()
    alphas_flat = alphas.flatten()

    # 计算 ks，注意确保所有数组都是一维的
    ks = np.sqrt(kalphas_flat ** 2 + kphis_flat ** 2 * np.sin(alphas_flat) ** 2)
    # 将 ks 转换为 (4200,1) 列向量
    # ks = ks.reshape(-1, 1)

    dks = diff_func(ks, sspan)
    ddks = diff_func(dks, sspan)

    # Calculate curvature along the wellbore
    for i in range(len(sspan)):
        if i == 0:
            alpha1 = alphas[0]
            alpha2 = alphas[1]
            phi1 = phis[0]
            phi2 = phis[1]
            ds = sspan[1] - sspan[0]
        elif i == len(sspan) - 1:
            alpha1 = alphas[-2]
            alpha2 = alphas[-1]
            phi1 = phis[-2]
            phi2 = phis[-1]
            ds = 2 * (sspan[1] - sspan[0])
        else:
            alpha1 = alphas[i - 1]
            alpha2 = alphas[i + 1]
            phi1 = phis[i - 1]
            phi2 = phis[i + 1]
            ds = sspan[1] - sspan[0]

        dp = (phi2 - phi1) / 2
        da = (alpha2 - alpha1) / 2
        ac = (alpha1 + alpha2) / 2
        edl = np.sqrt(da ** 2 + dp ** 2 * (np.sin(ac)) ** 2)

        # Avoid division by zero
        if edl > 0:
            theta_cos = (da ** 2 / edl ** 2 * np.cos(dp) -
                         da * dp / edl ** 2 * (
                                     np.sin(alpha2) * np.cos(alpha2) - np.sin(alpha1) * np.cos(alpha1)) * np.sin(dp) +
                         dp ** 2 / edl ** 2 * np.sin(alpha1) * np.sin(alpha2) *
                         (np.sin(alpha1) * np.sin(alpha2) + np.cos(alpha1) * np.cos(alpha2) * np.cos(dp)))

            # Ensure cos value is within valid range for arccos
            theta_cos = max(min(theta_cos, 1.0), -1.0)
            theta = np.arccos(theta_cos)
            taos[i] = theta / ds
        else:
            taos[i] = 0

    # Clean up any NaN values
    taos = np.nan_to_num(taos)

    return alphas, phis, ks, dks, ddks, kphis, kalphas, taos


def deal_input_data(data):
    """Process well trajectory data to calculate coordinates"""
    Xs = np.zeros(data.shape[0])
    Ys = np.zeros(data.shape[0])
    Zs = np.zeros(data.shape[0])
    Length = data[:, 0].copy()

    for i in range(1, len(Xs)):
        alpha1 = data[i - 1, 1] / 180 * np.pi
        alpha2 = data[i, 1] / 180 * np.pi
        phi1 = data[i - 1, 2] / 180 * np.pi
        phi2 = data[i, 2] / 180 * np.pi

        # Handle angle wrapping
        ppp = abs(phi1 - phi2)
        if ppp > np.pi and phi1 < np.pi:
            phi1 = phi1 + 2 * np.pi
        elif ppp > np.pi and phi1 > np.pi:
            phi1 = phi1 - 2 * np.pi

        ds = data[i, 0] - data[i - 1, 0]

        # Calculate incremental coordinate changes
        if alpha1 != alpha2 and phi1 != phi2:
            dx = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (
                        np.sin(phi2) - np.sin(phi1))
            dy = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (
                        np.cos(phi1) - np.cos(phi2))
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        elif alpha1 == alpha2 and phi1 != phi2:
            dx = ds * np.sin(alpha1) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            dy = ds * np.sin(alpha1) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
            dz = ds * np.cos(alpha1)
        elif alpha1 != alpha2 and phi1 == phi2:
            dx = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.cos(phi1)
            dy = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.sin(phi1)
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        else:
            dx = ds * np.sin(alpha1) * np.cos(phi1)
            dy = ds * np.sin(alpha1) * np.sin(phi1)
            dz = ds * np.cos(alpha1)

        Xs[i] = Xs[i - 1] + dx
        Ys[i] = Ys[i - 1] + dy
        Zs[i] = Zs[i - 1] + dz

    # Convert to coordinates from bottom to top
    Length = data[-1, 0] - Length
    Xs0 = Xs[-1] - Xs
    Ys0 = Ys[-1] - Ys
    Zs0 = Zs[-1] - Zs

    # Rearrange coordinate system to match previous definition
    Xs = Zs0
    Ys = Xs0
    Zs = Ys0

    return Length, Xs, Ys, Zs


# 这是LIMIT水力延伸极限
def hydro_limit_hydro(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, A1, C1, A2, C2, A3, C3,
          Rzz, rzz, Lzz, Rzt, rzt, Lzt, L1, d1, L2, d2, L3, d3, L4, d4, Lp, Li, rzzjt,
          yxmd, H, jsjg, y):

    data = guiji
    wc = lbmx
    Q = pailiang / 1000 / 60  # Flow rate, m³/s
    Ql = pailiang / 60  # Flow rate, L/s
    rhoi = fluidden  # Drilling fluid density, kg/m³
    rhoo = fluidden / 1000  # Drilling fluid density, kg/L
    g = 9.81

    # Drill pipe and drill collar dimensions
    Rt = Rzz / 2  # Drill pipe outer radius, m
    rt = rzz / 2  # Drill pipe inner radius, m
    Rtzt = Rzt / 2  # Drill collar outer radius, m
    rtzt = rzt / 2  # Drill collar inner radius, m

    # Convert to cm for some equations
    Dwcm = Dw * 100  # Wellbore diameter, cm
    Rzzcm = Rzz * 100  # Drill pipe outer diameter, cm
    rzzcm = rzz * 100  # Drill pipe inner diameter, cm
    Rztcm = Rzt * 100  # Drill collar outer diameter, cm
    rztcm = rzt * 100  # Drill collar inner diameter, cm
    # 单位转换：将各内径从原单位转换为 cm
    d1 = d1 * 100  # 地面高压管线内径，cm
    d2 = d2 * 100  # 立管内径，cm
    d3 = d3 * 100  # 水龙带内径，cm
    d4 = d4 * 100  # 方钻杆内径，cm

    # 取 guiji 第一列数据（MATLAB 的 guiji(:,1) 对应 Python 的 guiji[:,0]）
    jd = guiji[:, 0]
    yssd = jd[-1]

    # 计算迭代次数：向上取整
    num_iterations = int(np.ceil(yssd / jsjg))

    # 初始化 Plg 数组，形状为 (num_iterations * jsjg, num_iterations)
    Plg = np.zeros((num_iterations * jsjg, num_iterations))

    # 循环遍历每一次迭代（MATLAB 的 for nnn=1:num_iterations 对应 Python 的 range(1, num_iterations+1)）
    for nnn in range(1, num_iterations + 1):
        if nnn == num_iterations:
            # 最后一次迭代时使用 guiji 的最后一个值
            js = yssd
        else:
            # 否则按照正常的间隔计算
            js = nnn * jsjg

        # 四舍五入，得到 ntrans
        ntrans = round(js)

        # 地面管汇压耗计算
        # 注意：^ 在 MATLAB 中为乘方运算，在 Python 中需用 ** 表示
        Pdm = (5.1655 * (rhoo ** 0.8) * (miu ** 0.2) *
               (L1 / (d1 ** 4.8) + L2 / (d2 ** 4.8) + L3 / (d3 ** 4.8) + L4 / (d4 ** 4.8)) *
               (Ql ** 1.8) / 10)

        # 钻头压降计算
        S1 = C1 * np.pi * ((A1 / 2 / 10) ** 2)
        S2 = C2 * np.pi * ((A2 / 2 / 10) ** 2)
        S3 = C3 * np.pi * ((A3 / 2 / 10) ** 2)
        S = S1 + S2 + S3
        dertaPzt = (0.05 * (Ql ** 2) * rhoi / 1000) / ((0.95 ** 2) * (S ** 2))


        # Static hydrostatic pressure calculation
        ds = 1
        length = ntrans - 1
        nt = length / ds
        sspan = np.arange(0, length + 1, ds)
        SW = sspan.reshape(-1, 1)

        Mk, mk, Sk, alphak, phik = deal_curve_data2(data, js)
        Mk = Mk.reshape(-1, 1)
        mk = mk.reshape(-1, 1)
        Sk = Sk.reshape(-1, 1)
        alphak = alphak.reshape(-1, 1)
        phik = phik.reshape(-1, 1)

        alpha, phi, ks, dks, ddks, kphis, kalphas, taos = prepare_data(sspan, Mk, mk, Sk, alphak, phik)

        # 假设 ntrans 是一个整数，alpha 是一维数组，rhoi、g、Q、rt、Dw、Rt、rtzt、Rtzt 均为标量
        PI1 = np.zeros((ntrans, 1))
        PO1 = np.zeros((ntrans, 1))
        PI2 = np.zeros((ntrans, 1))

        PO2 = np.zeros((ntrans, 1))

        for i in range(ntrans):
            # MATLAB 中 alpha(ntrans-i+1) 对应 Python 的 alpha[ntrans-i-1]
            PI1[i, 0] = rhoi * g * np.cos(alpha[ntrans - i - 1])
            PO1[i, 0] = rhoi * g * np.cos(alpha[ntrans - i - 1])

        PI2[0, 0] = PI1[0, 0]
        PO2[0, 0] = PO1[0, 0]
        for i in range(1, ntrans):
            PI2[i, 0] = PI2[i - 1, 0] + PI1[i, 0]
            PO2[i, 0] = PO2[i - 1, 0] + PO1[i, 0]

        # 管内静液柱压力和环空静液柱压力
        PI2 = (PI2 - 9.81 * rhoi) / (10 ** 6)
        PO2 = (PO2 - 9.81 * rhoi) / (10 ** 6)

        # 流速计算
        # 钻柱井段
        Vp = Q / (np.pi * rt ** 2)  # 管内流速
        Va = 4 * Q / (np.pi * (Dw ** 2 - 4 * Rt ** 2))  # 环空流速

        # 钻铤井段
        Vpzt = Q / (np.pi * rtzt ** 2)  # 管内流速
        Vazt = 4 * Q / (np.pi * (Dw ** 2 - 4 * Rtzt ** 2))  # 环空流速
        fjt = Lp / (Lp + Li) + Li / (Lp + Li) * (rzz / rzzjt) ** 4.8

        if wc == 1:  # 宾汉流体
            # 钻柱井段
            # 管内雷诺数
            Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
            # 环空雷诺数
            Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))

            # 管内压降
            if Repzz < 2000:
                Ppzz = 40.7437 * miu * np.arange(1, js - Lzt + 1) * Ql / rzzcm ** 4 + taof * np.arange(1, js - Lzt + 1) / (
                            187.5 * rzzcm)
            else:
                Ppzz = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, js - Lzt + 1) * Ql ** 1.8 / rzzcm ** 4.8

            # 环空压降
            if Reazz < 2000:
                Pazz = 61.1155 * miu * np.arange(1, js - Lzt + 1) * Ql / (Dwcm - Rzzcm) ** 3 / (Dwcm + Rzzcm) + 6 * 10 ** (
                    -3) * taof * np.arange(1, js - Lzt + 1) / (Dwcm - Rzzcm)
            else:
                Pazz = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, js - Lzt + 1) * Ql ** 1.8 / (Dwcm - Rzzcm) ** 3 / (
                            Dwcm + Rzzcm) ** 1.8

            # 钻铤井段
            # 管内雷诺数
            Repzt = rhoi * rzt * Vpzt / miu / (1 + taof * rzt / (6 * miu * Vpzt))
            # 环空雷诺数
            Reazt = rhoi * (Dw - Rzt) * Vazt / miu / (1 + taof * (Dw - Rzt) / (8 * miu * Vazt))
            # 管内压降
            if Repzt < 2000:
                Ppzt = 40.7437 * miu * np.arange(1, Lzt + 1) * Ql / rztcm ** 4 + taof * np.arange(1, Lzt + 1) / (
                        187.5 * rztcm)
            else:
                Ppzt = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / rztcm ** 4.8
            # 环空压降
            if Reazt < 2000:
                Pazt = (61.1155 * miu * np.arange(1, Lzt + 1) * Ql / ((Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm)) +
                        6e-3 * taof * np.arange(1, Lzt + 1) / (Dwcm - Rztcm))
            else:
                Pazt = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / (
                        (Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm) ** 1.8)


        elif wc == 2:  # 幂律流体
            # 钻柱井段
            # 管内雷诺数
            Repzz = rhoi * (rzz ** n) * (Vp ** (2 - n)) / (8 ** (n - 1)) / K / (((3 * n + 1) / (4 * n)) ** n)

            # 环空雷诺数
            Reazz = rhoi * ((Dw - Rzz) ** n) * (Va ** (2 - n)) / (12 ** (n - 1)) / K / (((2 * n + 1) / (3 * n)) ** n)

            # 构造索引数组，对应 MATLAB 中 (1:(js-Lzt))'
            indices = np.arange(1, js - Lzt + 1)  # 从 1 到 js-Lzt

            # 管内压降
            if Repzz < 2000:
                Ppzz = (((8000 * (3 * n + 1) * Ql) / (np.pi * n * (rzzcm ** 3))) ** n) * indices * K / 250 / rzzcm
            else:
                Ppzz = 5.1655 * (miu ** 0.2) * (rhoo ** 0.8) * indices * (Ql ** 1.8) / (rzzcm ** 4.8)

            # 环空压降
            if Reazz < 2000:
                Pazz = (((16000 * (2 * n + 1) * Ql) / (
                            np.pi * n * ((Dwcm - Rzzcm) ** 2 * (Dwcm + Rzzcm)))) ** n) * indices * K / 250 / (Dwcm - Rzzcm)
            else:
                Pazz = 5.7503 * (miu ** 0.2) * (rhoo ** 0.8) * indices * (Ql ** 1.8) / (
                            ((Dwcm - Rzzcm) ** 3) * ((Dwcm + Rzzcm) ** 1.8))
            # 钻铤井段
            # 管内雷诺数
            Repzt = rhoi * rzt ** n * Vpzt ** (2 - n) / (8 ** (n - 1)) / K / (((3 * n + 1) / (4 * n)) ** n)
            # 环空雷诺数
            Reazt = rhoi * (Dw - Rzt) ** n * Vazt ** (2 - n) / (12 ** (n - 1)) / K / (((2 * n + 1) / (3 * n)) ** n)
            # 管内压降
            if Repzt < 2000:
                Ppzt = (((8000 * (3 * n + 1) * Ql) / (np.pi * n * rztcm ** 3)) ** n) * np.arange(1,
                                                                                                 Lzt + 1) * K / 250 / rztcm
            else:
                Ppzt = 5.1655 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / rztcm ** 4.8
            # 环空压降
            if Reazt < 2000:
                Pazt = (((16000 * (2 * n + 1) * Ql) / (
                            np.pi * n * (Dwcm - Rztcm) ** 2 * (Dwcm + Rztcm))) ** n) * np.arange(
                    1, Lzt + 1) * K / 250 / (Dwcm - Rztcm)
            else:
                Pazt = 5.7503 * miu ** 0.2 * rhoo ** 0.8 * np.arange(1, Lzt + 1) * Ql ** 1.8 / (
                        (Dwcm - Rztcm) ** 3 * (Dwcm + Rztcm) ** 1.8)
        elif wc == 3:  # 赫巴流体
            gammaaa = 8 * Va / (Dw - Rzz)
            miueffa = K * (8 * Va / (Dw - Rzz)) ** (n - 1) + taof / gammaaa
            Reazz = rhoi * Va * (Dw - Rzz) / miueffa
            gammaazt = 8 * Vazt / (Dw - Rzt)
            miueffazt = K * (8 * Vazt / (Dw - Rzt)) ** (n - 1) + taof / gammaazt
            Reazt = rhoi * Vazt * (Dw - Rzt) / miueffazt

            # 环空——单位转换
            Qhb = Q * 15850.32
            dp = Rzz * 39.3701
            dpzt = Rzt * 39.3701
            dh = Dw * 39.3701
            Khb = K * 2.0885
            taofhb = taof * 2.0885
            rhoihb = rhoi * 0.008345

            # 钻柱井段——环空
            Vahb = 24.51 * Qhb / (dh ** 2 - dp ** 2)
            Baa = 1.5 * (2 * n + 1) / (3 * n)
            Gfa = Baa
            gammaa = 1.6 * Gfa * Vahb / (dh - dp)
            taova = (3 / 2) ** n * taofhb + Khb * gammaa ** n
            taowa = 1.067 * taova
            NReGa = rhoihb * Vahb ** 2 / (19.36 * taowa)
            NcRe = 3470 - 1370 * n
            flama = 16 / NReGa
            ftransa = 16 * NReGa / (NcRe ** 2)
            a_val = (np.log10(n) + 3.93) / 50
            b_val = (1.75 - np.log10(n)) / 7
            fturba = a_val / (NReGa ** b_val)
            finta = (ftransa ** (-8) + fturba ** (-8)) ** (-1 / 8)
            fa = (finta ** 12 + flama ** 12) ** (1 / 12)
            Pazz = 1.076 * rhoihb * Vahb ** 2 * fa * np.arange(1, js - Lzt + 1) / 10 ** 5 / (dh - dp)
            Pazz = Pazz * 6.894757 / 1000 * 10

            # 钻铤井段——环空
            Vahbzt = 24.51 * Qhb / (dh ** 2 - dpzt ** 2)
            Baazt = 1.5 * (2 * n + 1) / (3 * n)
            Gfazt = Baazt
            gammaazt = 1.6 * Gfazt * Vahbzt / (dh - dpzt)
            taovazt = (3 / 2) ** n * taofhb + Khb * gammaazt ** n
            taowazt = 1.067 * taovazt
            NReGazt = rhoihb * Vahb ** 2 / (19.36 * taowazt)  # 注意这里使用 Vahb**2，与原代码一致
            NcRezt = 3470 - 1370 * n
            flamazt = 16 / NReGazt
            ftransazt = 16 * NReGazt / (NcRezt ** 2)
            a_val = (np.log10(n) + 3.93) / 50  # 重新计算 a_val, b_val（若需要可复用前面结果）
            b_val = (1.75 - np.log10(n)) / 7
            fturbazt = a_val / (NReGazt ** b_val)
            fintazt = (ftransazt ** (-8) + fturbazt ** (-8)) ** (-1 / 8)
            fazt = (fintazt ** 12 + flamazt ** 12) ** (1 / 12)
            Pazt = 1.076 * rhoihb * Vahbzt ** 2 * fazt * np.arange(1, Lzt + 1) / (10 ** 5 * (dh - dpzt))
            Pazt = Pazt * 6.894757 / 1000 * 10

            # 管内计算
            # 钻柱井段——管内
            gammap = 8 * Vp / rzz
            miueffp = K * (8 * Vp / rzz) ** (n - 1) + taof / gammap
            Repzz = rhoi * Vp * rzz / miueffp

            if Repzz < 2000:
                Ppzz = (2 * taof * np.arange(1, js - Lzt + 1) / rzz +
                        2 * n * np.arange(1, js - Lzt + 1) * K * Q ** n / (n + 1) / (np.pi * rt ** 2) ** n) / 10 ** 5
            else:
                Ppzz = (0.316 / Repzz ** 0.25 * np.arange(1, js - Lzt + 1) * rhoi * Vp ** 2 / rzz / 2) / 10 ** 5

            # 钻铤井段——管内
            gammapzt = 8 * Vpzt / rzt
            miueffpzt = K * (8 * Vpzt / rzt) ** (n - 1) + taof / gammapzt
            Repzt = rhoi * Vpzt * rzt / miueffpzt
            if Repzt < 2000:
                Ppzt = (2 * taof * np.arange(1, Lzt + 1) / rzt +
                        2 * n * np.arange(1, Lzt + 1) * K * Q ** n / (n + 1) / (np.pi * rtzt ** 2) ** n) / 10 ** 5
            else:
                Ppzt = (0.316 / Repzt ** 0.25 * np.arange(1, Lzt + 1) * rhoi * Vpzt ** 2 / rzt / 2) / 10 ** 5

        # 计算新的管内、环空末端压力
        Ppztt = Ppzz[-1] + Ppzt
        Paztt = Pazz[-1] + Pazt

        # 将原数组与末端数据拼接，形成新的压力数组
        Ppp = np.concatenate((Ppzz, Ppztt), axis=0)
        Paa = np.concatenate((Pazz, Paztt), axis=0)

        # 计算最终的管内和环空循环压力
        Pp = fjt * Ppp / 10
        Pa = Paa / 10

        if y == 0:
            # 环空循环压力
        
            if Dw <= 0.3:
                if wc == 1:
                    aaa = 0.885
                elif wc == 2:
                    aaa = 1.045
                elif wc == 3:
                    aaa = 1.382
            elif Dw > 0.3:
                if wc == 1:
                    aaa = 0.88
                elif wc == 2:
                    aaa = 1.01
                elif wc == 3:
                    aaa = 1.1


            # Phk = PO2.flatten() + Pa * aaa

            mm = ntrans
            Phk = np.zeros(mm)
            Phk[0] = 0
            PO2 = PO2.flatten()

            for i in range(1, mm):
                PO2yx = PO2[i] - PO2[i-1]
                Payx = Pa[i] - Pa[i-1]
                Phk[i] = Phk[i-1] + PO2yx + aaa * Payx

            # 管内循环压力
            if Dw <= 0.3:
                if wc == 1:
                    nnnn = 1.69
                elif wc == 2:
                    nnnn = 1.435
                elif wc == 3:
                    nnnn = 0.78
            elif Dw > 0.3:
                if wc == 1:
                    nnnn = 1.44
                elif wc == 2:
                    nnnn = 1.087
                elif wc == 3:
                    nnnn = 0.69



            nn = ntrans  # ntrans 应该是一个正整数
            # 创建一个长度为 nn 的一维数组（与 MATLAB 的 zeros(nn,1) 等价）
            Pgn = np.zeros(nn)

            # MATLAB 中 Pgn(end)=Phk(end)+dertaPzt 对应 Python 的 Pgn[-1] = Phk[-1] + dertaPzt
            Pgn[-1] = Phk[-1] + dertaPzt

            # 循环计算管内循环压力，其 MATLAB 代码为：
            # for i=1:nn-1
            #     PI2yx=PI2(end+1-i)-PI2(end-i);
            #     Ppyx=Pp(end+1-i)-Pp(end-i);
            #     Pgn(end-i)=Pgn(end+1-i)-PI2yx+nnnn*Ppyx;
            # end
            for i in range(1, nn):
                # 对应 MATLAB 中 PI2(end+1-i) 为 Python 的 PI2[-i]，而 PI2(end-i) 为 PI2[-(i+1)]
                PI2yx = PI2[-i] - PI2[-(i+1)]
                Ppyx = Pp[-i] - Pp[-(i+1)]
                Pgn[-(i+1)] = Pgn[-i] - PI2yx + nnnn * Ppyx

            # 立管压力：MATLAB 中 Plg(1:length(Pgn), nnn) = Pgn
            # 注意：如果 MATLAB 中 nnn 为列索引（从 1 开始），在 Python 中请确保 nnn 已做相应调整（从 0 开始）
            Plg[:len(Pgn), nnn - 1] = Pgn

            # 总循环压耗：MATLAB 中 P=Plg(1,:)+Pdm，对应 Python 中取 Plg 第一行（索引 0）
            P = Plg[0, :] + Pdm

            # 设定 Pyx 为 0
            Pyx = 0
        elif y == 1:
            # 考虑岩屑的环空压耗
            S = yxmd / rhoi

            # 钻柱井段
            if Reazz < 2000:
                fd = 64 / Reazz
            else:
                fd = 0.316 / (Reazz ** 0.25)
            # 注意：MATLAB 中的 ".*" 表示逐元素乘法，这里假设 H 和 Pazz 均为 NumPy 数组
            term1 = (Va ** 2) / g / (Dw - Rzz) / (S - 1)
            Payxzz = (0.026068625 * H * Pazz / 10 / fd *
                      (term1 ** (-1.25)) +
                      (1 + 0.00581695 * H) * Pazz / 10)

            # 钻铤井段
            if Reazt < 2000:
                fdzt = 64 / Reazt
            else:
                fdzt = 0.316 / (Reazt ** 0.25)
            term2 = (Vazt ** 2) / g / (Dw - Rzt) / (S - 1)
            Payxzt = (0.026068625 * H * Pazt / 10 / fdzt *
                      (term2 ** (-1.25)) +
                      (1 + 0.00581695 * H) * Pazt / 10)

            # Payxzz(end) 表示 Payxzz 的最后一个元素，加上 Payxzt 后得到 Payxztt
            Payxztt = Payxzz[-1] + Payxzt

            # MATLAB 中 [Payxzz; Payxztt] 是垂直拼接（按行堆叠）
            # 如果 Payxzz 与 Payxztt 均为 1D 数组，则使用 np.vstack 保证维度一致
            # TODO注意这里是
            Payx = np.vstack((Payxzz.reshape(-1, 1), Payxztt.reshape(-1, 1))).flatten()

            if Dw <= 0.3:
                if wc == 1:
                    aaa = 0.885
                elif wc == 2:
                    aaa = 1.045
                elif wc == 3:
                    aaa = 1.382
            elif Dw > 0.3:
                if wc == 1:
                    aaa = 0.88
                elif wc == 2:
                    aaa = 1.01
                elif wc == 3:
                    aaa = 1.1

            # Phkyx = PO2.flatten() + Payx * aaa
            mm = ntrans
            Phkyx = np.zeros(mm)
            Phkyx[0] = 0
            PO2 = PO2.flatten()

            for i in range(1, mm):
                PO2yx = PO2[i] - PO2[i-1]
                Payxx = Payx[i] - Payx[i-1]
                Phkyx[i] = Phkyx[i-1] + PO2yx + aaa * Payxx

            # 考虑岩屑的管内循环压力
            if Dw <= 0.3:
                if wc == 1:
                    nnnn = 1.69
                elif wc == 2:
                    nnnn = 1.435
                elif wc == 3:
                    nnnn = 0.78
            elif Dw > 0.3:
                if wc == 1:
                    nnnn = 1.44
                elif wc == 2:
                    nnnn = 1.087
                elif wc == 3:
                    nnnn = 0.69

            nn = ntrans  # ntrans 是正整数
            # 创建一个长度为 nn 的一维数组（与 MATLAB 中的 zeros(nn,1) 等价）
            Pgnyx = np.zeros(nn)

            # MATLAB 中 Pgnyx(end)=Phkyx(end)+dertaPzt 对应 Python 的 Pgnyx[-1] = Phkyx[-1] + dertaPzt
            Pgnyx[-1] = Phkyx[-1] + dertaPzt

            # 循环计算岩屑的管内循环压力
            for i in range(1, nn):
                # 对应 MATLAB 中 PI2(end+1-i) 为 Python 的 PI2[-i]，PI2(end-i) 为 PI2[-(i+1)]
                PI2yx = PI2[-i] - PI2[-(i + 1)]
                Ppyx = Pp[-i] - Pp[-(i + 1)]
                Pgnyx[-(i + 1)] = Pgnyx[-i] - PI2yx + nnnn * Ppyx

            # 立管压力：MATLAB 中 Plg(1:length(Pgnyx), nnn) = Pgnyx
            Plg[:len(Pgnyx), nnn - 1] = Pgnyx

            # 考虑岩屑的总循环压耗：MATLAB 中 P=Plg(1,:)+Pdm
            Pyx = Plg[0, :] + Pdm

            P = 0
    return P, Pyx, Plg, yssd















