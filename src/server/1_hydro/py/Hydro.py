# Hydro函数，返回一个元组，在调用函数的时候，使用元组解包进行赋值
# 返回值：
# return P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk  # 返回元组

import numpy as np
import utils

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
    len = ntrans - 1
    nt = len / ds
    sspan = np.arange(0, len + ds, ds) # 创建步长为ds的等差数列
    SW = sspan.reshape(-1, 1)  # 转换为列向量（类似 MATLAB 的列向量）


    Mk, mk, Sk, alphak, phik = utils.deal_curve_data2(data)
    alpha, phi, ks, dks, ddks, kphis, kalphas, taos = utils.prepare_data(sspan, Mk, mk, Sk, alphak, phik)

    ntrans = len(sspan)  # 计算 ntrans

    PI1 = np.zeros((ntrans, 1))  # 生成 ntrans×1 的零矩阵
    PO1 = np.zeros((ntrans, 1))
    PI2 = np.zeros((ntrans, 1))
    PO2 = np.zeros((ntrans, 1))

    for i in range(0, ntrans):  # MATLAB 以 1 开始，Python 以 0 开始，需要 +1
        PI1[i] = rhoi * g * np.cos(alpha[ntrans - i + 1])  # i-1 转换为 Python 索引
        PO1[i] = rhoi * g * np.cos(alpha[ntrans - i + 1])  
    
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

    # Ppzz , Pazz = 0
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
        
    




    




    
    
    


    return P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk  # 返回元组
    