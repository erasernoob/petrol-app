import numpy as np
import pandas as pd
import numpy as np
import datetime
from service import utils
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline



def main(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, 
         Dw, A1, C1, A2, C2, A3, C3, Rzz, rzz, Lzz, 
         Rzt, rzt, Lzt, L1, d1, L2, d2, L3, d3, L4, 
         d4, Lp, Li, rzzjt, yxmd, H, yx):


    # 调用 hydro_1 计算
    results = Hydro(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw,
                            A1, C1, A2, C2, A3, C3, Rzz, rzz, Lzz, Rzt, rzt, Lzt,
                            L1, d1, L2, d2, L3, d3, L4, d4, Lp, Li, rzzjt, yxmd, H, yx)

    P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk, dertaPzt = results
    
    print(ECD)

    # ------------------------------
    # 导出数据到 Excel 文件（不包含）
    # ------------------------------
    if yx == 0:
        return Sk, Pgn, Phk, ECD, P, Plg, Pdm, dertaPzt
    else:
        return Sk, Pgnyx, Phkyx, ECDyx, P, Plg, Pdm, dertaPzt




def Hydro(guiji,lbmx,pailiang,fluidden,n,K,miu,taof,Dw,A1,C1,A2,C2,A3,C3,Rzz,rzz,Lzz,Rzt,rzt,Lzt,L1,d1,L2,d2,L3,d3,L4,d4,Lp,Li,rzzjt,yxmd,H,yx):

    # print("Hydro function parameters:")
    # for name, value in locals().items():
    #     print(f"{name}: {value}")


    data = guiji # matrix
    wc = lbmx
    Q = pailiang / 1000 / 60  # 排量，m³/s
    Ql = pailiang / 60        # 排量，L/s
    rhoi = fluidden           # 钻井液密度，kg/m³
    rhoo = fluidden / 1000    # 钻井液密度，kg/L
    g = 9.81

    Rt = Rzz / 2       # 钻柱外径，m
    rt = rzz / 2       # 钻柱内径，m
    Rtzt = Rzt / 2     # 钻铤外径，m
    rtzt = rzt / 2     # 钻铤内径，m

    Dwcm = Dw * 100    # 井眼直径，cm
    Rzzcm = Rzz * 100  # 钻杆外径，cm
    rzzcm = rzz * 100  # 钻杆内径，cm
    Rztcm = Rzt * 100  # 钻铤外径，cm
    rztcm = rzt * 100  # 钻铤内径，cm

    d1 = d1 * 100      # 地面高压管线内径，cm
    d2 = d2 * 100      # 立管内径，cm
    d3 = d3 * 100      # 水龙带内径，cm
    d4 = d4 * 100      # 方钻杆内径，cm

    ntrans = round(data[-1, 0])

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
    fjt = Lp / (Lp + Li) + Li / (Lp + Li) * (rzz / rzzjt) ** 4.8

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

            # 计算新的管内、环空末端压力
    Ppztt = Ppzz[-1] + Ppzt
    Paztt = Pazz[-1] + Pazt

    # 将原数组与末端数据拼接，形成新的压力数组
    Ppp = np.concatenate((Ppzz, Ppztt), axis=0)
    Paa = np.concatenate((Pazz, Paztt), axis=0)

    # 计算最终的管内和环空循环压力
    Pp = fjt * Ppp / 10
    Pa = Paa / 10

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

        P = Pgn[0] + Pdm

        # 立管压力 (Riser pressure)
        Plg = Pgn[0]

        # Initialize additional variables to zero
        Pgnyx = 0
        Phkyx = 0
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

        Payxzz1 = (0.0026068625 * H * Pazz / 10 / fd *
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
        
        Payxzt1 = (0.0026068625 * H * Pazz / 10 / fd *
                  (term1 ** (-1.25)) +
                  (1 + 0.00581695 * H) * Pazz / 10)

        # Payxzz(end) 表示 Payxzz 的最后一个元素，加上 Payxzt 后得到 Payxztt
        Payxztt = Payxzz[-1] + Payxzt

        # MATLAB 中 [Payxzz; Payxztt] 是垂直拼接（按行堆叠）
        # 如果 Payxzz 与 Payxztt 均为 1D 数组，则使用 np.vstack 保证维度一致
        Payx = np.vstack((Payxzz.reshape(-1, 1), Payxztt.reshape(-1, 1))).flatten()
        Payxztt1 = Payxzz[-1] + Payxzt
        Payx1 = np.concatenate((Payxzz1, Payxztt1))

        # 考虑岩屑的环空循环压力
    
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
                    

        ECDyx = ccc * Payx1 * 10 ** 6 / 9.81 / 1000 / Tcs + rhoi / 1000

        P = Pgnyx[0] + Pdm

        # 立管压力 (Riser pressure)
        Plg = Pgnyx[0]

        # Initialize additional variables to zero
        Pgn = 0
        Phk = 0
        ECD = 0

    return P,Plg,Pdm,Pgn,Phk,ECD,Pgnyx,Phkyx,ECDyx,Sk, dertaPzt




