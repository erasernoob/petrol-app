# Hydro函数，返回一个元组，在调用函数的时候，使用元组解包进行赋值
# 返回值：
# return P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk  # 返回元组


from . import utils

import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline


def Hydro(guiji,lbmx,pailiang,fluidden,n,K,miu,taof,Dw,A1,C1,A2,C2,A3,C3,Rzz,rzz,Lzz,Rzt,rzt,Lzt,L1,d1,L2,d2,L3,d3,L4,d4,Lp,Li,rzzjt,yxmd,H,yx):
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

    ntrans = round(data[-1, 0])  #  data 是 NumPy 数组
    # 地面管汇压耗
    Pdm = 5.1655 * rhoo**0.8 * miu**0.2 * (L1 / d1**4.8 + L2 / d2**4.8 + L3 / d3**4.8 + L4 / d4**4.8) * Ql**1.8 / 10

    # 钻头压降
    S1 = C1 * np.pi * (A1 / 2 / 10)**2
    S2 = C2 * np.pi * (A2 / 2 / 10)**2
    S3 = C3 * np.pi * (A3 / 2 / 10)**2
    S = S1 + S2 + S3

    dertaPzt = (0.05 * Ql**2 * rhoi / 1000) / (0.95**2 * S**2)

    ds = 1 
    length = ntrans - 1
    nt = length / ds
    sspan = np.arange(0, length + ds, ds) # 创建步长为ds的等差数列
    SW = sspan.reshape(-1, 1)  # 转换为列向量（类似 MATLAB 的列向量）


    print(data.shape)
    Mk, mk, Sk, alphak, phik = utils.deal_curve_data2(data)
    alpha, phi, ks, dks, ddks, kphis, kalphas, taos = utils.prepare_data(sspan, Mk, mk, Sk, alphak, phik)

    ntrans = len(sspan)  # 计算 ntrans

    PI1 = np.zeros((ntrans, 1))  # 生成 ntrans×1 的零矩阵
    PO1 = np.zeros((ntrans, 1))
    PI2 = np.zeros((ntrans, 1))
    PO2 = np.zeros((ntrans, 1))

    for i in range(0, ntrans):  # MATLAB 以 1 开始，Python 以 0 开始，需要 +1
        PI1[i] = rhoi * g * np.cos(alpha[ntrans - i - 1])  # i-1 转换为 Python 索引
        PO1[i] = rhoi * g * np.cos(alpha[ntrans - i - 1])  
    
    PI2[0] = PI1[0] 
    PO2[0] = PO1[0] 

    for i in range(1, ntrans):
        PI2[i] = PI2[i - 1] + PI1[i]
        PO2[i] = PO2[i - 1] + PO1[i]
    
    PI2 = (PI2 - 9.81 * rhoi) / 10**6  # 管内静液柱压力
    PO2 = (PO2 - 9.81 * rhoi) / 10**6  # 环空静液柱压力


    # 流速计算
    Vp = Q / (np.pi * rt**2)                # 管内流速
    Va = 4 * Q / (np.pi * (Dw**2 - 4 * Rt**2))  # 环空流速

    # 钻铤井段
    Vpzt = Q / (np.pi * rtzt**2)               # 管内流速
    Vazt = 4 * Q / (np.pi * (Dw**2 - 4 * Rtzt**2))  # 环空流速

    # 钻柱接头影响系数
    fjt = Lp / (Lp + Li) + Li / (Lp + Li) * (rzz / rzzjt)**4.8

    if wc == 1:
    # 钻柱井段
        Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
        Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))
    
        Lzz_vec = np.arange(1, Lzz + 1).reshape(-1, 1)  # 保持列向量
        if Repzz < 2000:
            Ppzz = 40.7437 * miu * Lzz_vec * Ql / rzzcm**4 + taof * Lzz_vec / (187.5 * rzzcm)
        else:
            Ppzz = 5.1655 * miu**0.2 * rhoo**0.8 * Lzz_vec * Ql**1.8 / rzzcm**4.8
    
        if Reazz < 2000:
            Pazz = 61.1155 * miu * Lzz_vec * Ql / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm) + 6 * 10**-3 * taof * Lzz_vec / (Dwcm - Rzzcm)
        else:
            Pazz = 5.7503 * miu**0.2 * rhoo**0.8 * Lzz_vec * Ql**1.8 / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm)**1.8
    elif wc == 2:  # 幂律流体
        # 钻柱井段
        Repzz = rhoi * rzz**n * Vp**(2-n) / 8**(n-1) / K / ((3*n+1) / (4*n))**n
        Reazz = rhoi * (Dw - Rzz)**n * Va**(2-n) / 12**(n-1) / K / ((2*n+1) / (3*n))**n
        
        if Repzz < 3470 - 1370 * n:
            Ppzz = ((8000 * (3*n+1) * Ql) / (np.pi * n * rzzcm**3))**n * Lzz_vec * K / 250 / rzzcm
        else:
            Ppzz = 5.1655 * miu**0.2 * rhoo**0.8 * Lzz_vec * Ql**1.8 / rzzcm**4.8
        
        if Reazz < 3470 - 1370 * n:
            Pazz = ((16000 * (2*n+1) * Ql) / (np.pi * n * (Dwcm - Rzzcm)**2 * (Dwcm + Rzzcm)))**n * Lzz_vec * K / 250 / (Dwcm - Rzzcm)
        else:
            Pazz = 5.7503 * miu**0.2 * rhoo**0.8 * Lzz_vec * Ql**1.8 / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm)**1.8
        # 钻铤井段
        Repzt = rhoi * rzt**n * Vpzt**(2-n) / 8**(n-1) / K / ((3*n+1) / (4*n))**n
        Reazt = rhoi * (Dw - Rzt)**n * Vazt**(2-n) / 12**(n-1) / K / ((2*n+1) / (3*n))**n

        Lzt_vec = np.arange(1, Lzt + 1).reshape(-1, 1)  # 保持列向量

        if Repzt < 3470 - 1370 * n:
            Ppzt = ((8000 * (3*n+1) * Ql) / (np.pi * n * rztcm**3))**n * Lzt_vec * K / 250 / rztcm
        else:
            Ppzt = 5.1655 * miu**0.2 * rhoo**0.8 * Lzt_vec * Ql**1.8 / rztcm**4.8

        if Reazt < 3470 - 1370 * n:
            Pazt = ((16000 * (2*n+1) * Ql) / (np.pi * n * (Dwcm - Rztcm)**2 * (Dwcm + Rztcm)))**n * Lzt_vec * K / 250 / (Dwcm - Rztcm)
        else:
            Pazt = 5.7503 * miu**0.2 * rhoo**0.8 * Lzt_vec * Ql**1.8 / (Dwcm - Rztcm)**3 / (Dwcm + Rztcm)**1.8
    elif wc == 3: # 赫巴流体
        # 管内雷诺数
        Repzz = (8**(1-n) * rhoi * rzz**n * Vp**(2-n) / K / ((3*n+1)/(4*n))**n / 
                (1 + (3*n+1) / (2*n+1) * (n/(6*n+2))**n * (rzz/Vp)**n * taof / K))

        # 环空雷诺数
        Reazz = (12**(1-n) * rhoi * (Dw-Rzz)**n * Va**(2-n) / K / ((2*n+1)/(3*n))**n / 
                (1 + (2*n+1)**(1-n) / (n+1) * (n/4)**n * ((Dw-Rzz)/Va)**n * taof / K))

        # 临界雷诺数
        Reczz = 3470 - 1370 * n

        # 管内壁面剪切力
        taowpzz = taof + K * (8 * Q / np.pi / (rzz/2)**3)**n

        # 环空壁面剪切力
        taowazz = taof + K * (8 * Q / np.pi / ((Dw/2)**3 - (Rzz/2)**3))**n

        # 计算管内摩擦系数
        if Repzz < Reczz:
            fpzz = 16 / Repzz
        else:
            equation = lambda fpzz: (1 / np.sqrt(fpzz) - 
                                        (2.69/n - 2.95 + 4.53/n * np.log10(Repzz * fpzz**(1-0.5*n)) + 
                                        4.53/n * np.log10(1 - taof/taowpzz)))
            fpzz = fsolve(equation, 0.01)[0]

        # 计算环空摩擦系数
        if Reazz < Reczz:
            fazz = 24 / Reazz
        else:
            equation_fazz = lambda fazz: (1 / np.sqrt(fazz) - 
                                        (2.69/n - 2.95 + 4.53/n * np.log10(Reazz * fazz**(1-0.5*n)) + 
                                        4.53/n * np.log10(1 - taof/taowazz)))
            fazz = fsolve(equation_fazz, 0.01)[0]

        # 生成列向量
        Lzz_vec = np.arange(1, Lzz + 1).reshape(-1, 1)

        # 管内压降
        Ppzz = 2 * fpzz * rhoi * Lzz_vec * Vp**2 / rzz / 10**6 * 10

        # 环空压降
        Pazz = 2 * fazz * rhoi * Lzz_vec * Va**2 / (Dw - Rzz) / 10**6 * 10

        # 钻铤井段
        # 管内雷诺数
        Repzt = (8**(1 - n) * rhoi * rzt**n * Vpzt**(2 - n) /
                (K * ((3 * n + 1) / (4 * n))**n *
                (1 + (3 * n + 1) / (2 * n + 1) * (n / (6 * n + 2))**n *
                    (rzt / Vpzt)**n * taof / K)))

        # 环空雷诺数
        Reazt = (12**(1 - n) * rhoi * (Dw - Rzt)**n * Vazt**(2 - n) /
                (K * ((2 * n + 1) / (3 * n))**n *
                (1 + (2 * n + 1)**(1 - n) / (n + 1) * (n / 4)**n *
                    ((Dw - Rzt) / Vazt)**n * taof / K)))

        # 临界雷诺数
        Reczt = 3470 - 1370 * n

        # 管内壁面剪切力
        # taowpzt = taof + K * (8 * Vpzt / rzt)**n
        taowpzt = taof + K * (8 * Q / np.pi / (rzt / 2)**3)**n

        # 环空壁面剪切力
        # taowazt = taof + K * (6 * Vazt / (Dw - Rzt))**n
        taowazt = taof + K * (8 * Q / np.pi / ((Dw / 2)**3 - (Rzt / 2)**3))**n

        # 管内摩擦系数
        if Repzt < Reczt:
            fpzt = 16 / Repzt
        else:
            equation_fpzt = lambda fpzt: (1 / np.sqrt(fpzt) -
                                        (2.69 / n - 2.95 + 4.53 / n * np.log10(Repzt * fpzt**(1 - 0.5 * n)) +
                                        4.53 / n * np.log10(1 - taof / taowpzt)))
            fpzt = fsolve(equation_fpzt, 0.01)[0]

        # 环空摩擦系数
        if Reazt < Reczt:
            fazt = 24 / Reazt
        else:
            equation_fazt = lambda fazt: (1 / np.sqrt(fazt) -
                                        (2.69 / n - 2.95 + 4.53 / n * np.log10(Reazt * fazt**(1 - 0.5 * n)) +
                                        4.53 / n * np.log10(1 - taof / taowazt)))
            fazt = fsolve(equation_fazt, 0.01)[0]

        # 管内压降
        Ppzt = 2 * fpzt * rhoi * np.arange(1, Lzt + 1).reshape(-1, 1) * Vpzt**2 / rzt / 10**6 * 10

        # 环空压降
        Pazt = 2 * fazt * rhoi * np.arange(1, Lzt + 1).reshape(-1, 1) * Vazt**2 / (Dw - Rzt) / 10**6 * 10

    # 计算总压降
    Ppztt = Ppzz[-1] + Ppzt
    Paztt = Pazz[-1] + Pazt
    # TODO: 存在列向量问题
    # Ppp = np.concatenate((Ppzz, Ppztt))
    # Paa = np.concatenate((Pazz, Paztt))

    Ppp = np.vstack((Ppzz, Ppztt))
    Paa = np.vstack((Pazz, Paztt))

    Pp = fjt * Ppp / 10
    Pa = Paa / 10

    # 垂深插值
    Length, Xs, Ys, Zs = utils.deal_input_data(data)
    cs = Xs[0] - Xs
    aa = data[:, 0]
    T = cs
    aacs = np.arange(1, np.max(aa) + 1).reshape(-1, 1)
    Tcs = CubicSpline(aa, T, bc_type='natural')(aacs)

    # 一维数组转换为二维数组
    Tcs = Tcs.reshape(-1, 1)

    
    if yx == 0:
    # 环空循环压力
        Phk = PO2 + Pa
        
        # 管内循环压力
        nn = ntrans
        Pgn = np.zeros((nn, 1))
        Pgn[-1] = Phk[-1] + dertaPzt
        
        for i in range(nn - 1):
            PI2yx = PI2[-(i + 1)] - PI2[-(i + 2)]
            Ppyx = Pp[-(i + 1)] - Pp[-(i + 2)]
            Pgn[-(i + 2)] = Pgn[-(i + 1)] - PI2yx + Ppyx  # 反向填充 Pgn

        # ECD 计算
        ECD = Pa * 1e6 / 9.81 / 1000 / Tcs + rhoi / 1000

        # 总循环压耗
        P = Pgn[0] + Pdm

        # 立管压力
        Plg = Pgn[0]

        # 赋值 0
        Pgnyx = 0
        Phkyx = 0
        ECDyx = 0

    elif yx == 1:
        # 考虑岩屑的环空压耗
        S = yxmd / rhoi

        # 钻柱井段
        if wc == 1:
            if Reazz < 2000:
                fd = 64 / Reazz
            else:
                fd = 0.316 / Reazz ** 0.25
        elif wc == 2 or wc == 3:
            if Reazz < 3470 - 1370 * n:
                fd = 64 / Reazz
            else:
                fd = 0.316 / Reazz ** 0.25

        # 计算 Payxzz，确保矩阵维度一致
        Payxzz = (0.0026068625 * H * Pazz / 10 / fd * 
                (Va ** 2 / g / (Dw - Rzz) / (S - 1)) ** (-1.25) + 
                (1 + 0.00581695 * H) * Pazz / 10)
    
        # 钻铤井段
        if wc == 1:
            if Reazt < 2000:
                fdzt = 64 / Reazt
            else:
                fdzt = 0.316 / Reazt ** 0.25
        elif wc == 2 or wc == 3:
            if Reazt < 3470 - 1370 * n:
                fdzt = 64 / Reazt
            else:
                fdzt = 0.316 / Reazt ** 0.25

        # 计算 Payxzt
        Payxzt = (0.0026068625 * H * Pazt / 10 / fdzt * (Vazt ** 2 / g / (Dw - Rzt) / (S - 1)) ** (-1.25) + (1 + 0.00581695 * H) * Pazt / 10)

        # 计算 Payxztt
        Payxztt = Payxzz[-1] + Payxzt
        Payx = np.vstack((Payxzz, Payxztt))  # 保持与 MATLAB 计算结果的结构一致

        # 考虑岩屑的环空循环压力
        Phkyx = PO2 + Payx

        # 考虑岩屑的管内循环压力
        nn = ntrans
        Pgnyx = np.zeros((nn, 1))
        Pgnyx[-1] = Phkyx[-1] + dertaPzt

        for i in range(nn - 1):
            PI2yx = PI2[-(i + 1)] - PI2[-(i + 2)]
            Ppyx = Pp[-(i + 1)] - Pp[-(i + 2)]
            Pgnyx[-(i + 2)] = Pgnyx[-(i + 1)] - PI2yx + Ppyx


        print(f"Pa:{Pa}")
        print(f"Tcs:{Tcs}")
        print(f"rhoi:{rhoi}")
        
        # 考虑岩屑的 ECD
        ECDyx = Payx * 10 ** 6 / 9.81 / 1000 / Tcs + rhoi / 1000

        # 考虑岩屑的总循环压耗
        P = Pgnyx[0] + Pdm

        # 立管压力
        Plg = Pgnyx[0]

        # 置零不使用的变量
        Pgn = 0
        Phk = 0
        ECD = 0

    return P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk  # 返回元组
    