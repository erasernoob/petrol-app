import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import fsolve

def Hydro(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, A1, C1, A2, C2, A3, C3, Rzz, rzz, Lzz, Rzt, rzt, Lzt, L1, d1, L2, d2, L3, d3, L4, d4, Lp, Li, rzzjt, yxmd, H, yx):
    data = guiji
    wc = lbmx
    Q = pailiang / 1000 / 60
    Ql = pailiang / 60
    rhoi = fluidden
    rhoo = fluidden / 1000
    g = 9.81
    Rt = Rzz / 2
    rt = rzz / 2
    Rtzt = Rzt / 2
    rtzt = rzt / 2
    Dwcm = Dw * 100
    Rzzcm = Rzz * 100
    rzzcm = rzz * 100
    Rztcm = Rzt * 100
    rztcm = rzt * 100
    d1 = d1 * 100
    d2 = d2 * 100
    d3 = d3 * 100
    d4 = d4 * 100
    ntrans = round(data[-1, 0])

    Pdm = 5.1655 * rhoo**0.8 * miu**0.2 * (L1 / d1**4.8 + L2 / d2**4.8 + L3 / d3**4.8 + L4 / d4**4.8) * Ql**1.8 / 10

    S1 = C1 * np.pi * (A1 / 2 / 10)**2
    S2 = C2 * np.pi * (A2 / 2 / 10)**2
    S3 = C3 * np.pi * (A3 / 2 / 10)**2
    S = S1 + S2 + S3
    dertaPzt = (0.05 * Ql**2 * rhoi / 1000) / (0.95**2 * S**2)

    ds = 1
    len = ntrans - 1
    nt = len / ds
    sspan = np.arange(0, len + ds, ds)
    SW = sspan.reshape(-1, 1)

    Mk, mk, Sk, alphak, phik = deal_curve_data2(data)
    alpha, phi, ks, dks, ddks, kphis, kalphas, taos = prepare_data(sspan, Mk, mk, Sk, alphak, phik)
    PI1 = np.zeros((ntrans, 1))
    PO1 = np.zeros((ntrans, 1))
    PI2 = np.zeros((ntrans, 1))
    PO2 = np.zeros((ntrans, 1))

    for i in range(ntrans):
        PI1[i] = rhoi * g * np.cos(alpha[ntrans - i])
        PO1[i] = rhoi * g * np.cos(alpha[ntrans - i])

    PI2[0] = PI1[0]
    PO2[0] = PO1[0]
    for i in range(1, ntrans):
        PI2[i] = PI2[i - 1] + PI1[i]
        PO2[i] = PO2[i - 1] + PO1[i]

    PI2 = (PI2 - 9.81 * rhoi) / 10**6
    PO2 = (PO2 - 9.81 * rhoi) / 10**6

    Vp = Q / (np.pi * rt**2)
    Va = 4 * Q / (np.pi * (Dw**2 - 4 * Rt**2))
    Vpzt = Q / (np.pi * rtzt**2)
    Vazt = 4 * Q / (np.pi * (Dw**2 - 4 * Rtzt**2))

    fjt = Lp / (Lp + Li) + Li / (Lp + Li) * (rzz / rzzjt)**4.8

    if wc == 1:
        Repzz = rhoi * rzz * Vp / miu / (1 + taof * rzz / (6 * miu * Vp))
        Reazz = rhoi * (Dw - Rzz) * Va / miu / (1 + taof * (Dw - Rzz) / (8 * miu * Va))
        if Repzz < 2000:
            Ppzz = 40.7437 * miu * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql / rzzcm**4 + taof * np.arange(1, Lzz + 1).reshape(-1, 1) / (187.5 * rzzcm)
        else:
            Ppzz = 5.1655 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql**1.8 / rzzcm**4.8
        if Reazz < 2000:
            Pazz = 61.1155 * miu * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm) + 6 * 10**(-3) * taof * np.arange(1, Lzz + 1).reshape(-1, 1) / (Dwcm - Rzzcm)
        else:
            Pazz = 5.7503 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql**1.8 / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm)**1.8
        Repzt = rhoi * rzt * Vpzt / miu / (1 + taof * rzt / (6 * miu * Vpzt))
        Reazt = rhoi * (Dw - Rzt) * Vazt / miu / (1 + taof * (Dw - Rzt) / (8 * miu * Vazt))
        if Repzt < 2000:
            Ppzt = 40.7437 * miu * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql / rztcm**4 + taof * np.arange(1, Lzt + 1).reshape(-1, 1) / (187.5 * rztcm)
        else:
            Ppzt = 5.1655 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql**1.8 / rztcm**4.8
        if Reazt < 2000:
            Pazt = 61.1155 * miu * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql / (Dwcm - Rztcm)**3 / (Dwcm + Rztcm) + 6 * 10**(-3) * taof * np.arange(1, Lzt + 1).reshape(-1, 1) / (Dwcm - Rztcm)
        else:
            Pazt = 5.7503 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql**1.8 / (Dwcm - Rztcm)**3 / (Dwcm + Rztcm)**1.8
    elif wc == 2:
        Repzz = rhoi * rzz**n * Vp**(2 - n) / 8**(n - 1) / K / ((3 * n + 1) / (4 * n))**n
        Reazz = rhoi * (Dw - Rzz)**n * Va**(2 - n) / 12**(n - 1) / K / ((2 * n + 1) / (3 * n))**n
        if Repzz < 3470 - 1370 * n:
            Ppzz = ((8000 * (3 * n + 1) * Ql) / (np.pi * n * rzzcm**3))**n * np.arange(1, Lzz + 1).reshape(-1, 1) * K / 250 / rzzcm
        else:
            Ppzz = 5.1655 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql**1.8 / rzzcm**4.8
        if Reazz < 3470 - 1370 * n:
            Pazz = ((16000 * (2 * n + 1) * Ql) / (np.pi * n * (Dwcm - Rzzcm)**2 * (Dwcm + Rzzcm)))**n * np.arange(1, Lzz + 1).reshape(-1, 1) * K / 250 / (Dwcm - Rzzcm)
        else:
            Pazz = 5.7503 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzz + 1).reshape(-1, 1) * Ql**1.8 / (Dwcm - Rzzcm)**3 / (Dwcm + Rzzcm)**1.8
        Repzt = rhoi * rzt**n * Vpzt**(2 - n) / 8**(n - 1) / K / ((3 * n + 1) / (4 * n))**n
        Reazt = rhoi * (Dw - Rzt)**n * Vazt**(2 - n) / 12**(n - 1) / K / ((2 * n + 1) / (3 * n))**n
        if Repzt < 3470 - 1370 * n:
            Ppzt = ((8000 * (3 * n + 1) * Ql) / (np.pi * n * rztcm**3))**n * np.arange(1, Lzt + 1).reshape(-1, 1) * K / 250 / rztcm
        else:
            Ppzt = 5.1655 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql**1.8 / rztcm**4.8
        if Reazt < 3470 - 1370 * n:
            Pazt = ((16000 * (2 * n + 1) * Ql) / (np.pi * n * (Dwcm - Rztcm)**2 * (Dwcm + Rztcm)))**n * np.arange(1, Lzt + 1).reshape(-1, 1) * K / 250 / (Dwcm - Rztcm)
        else:
            Pazt = 5.7503 * miu**0.2 * rhoo**0.8 * np.arange(1, Lzt + 1).reshape(-1, 1) * Ql**1.8 / (Dwcm - Rztcm)**3 / (Dwcm + Rztcm)**1.8
    elif wc == 3:
        Repzz = 8**(1 - n) * rhoi * rzz**n * Vp**(2 - n) / K / ((3 * n + 1) / (4 * n))**n / (1 + (3 * n + 1) / (2 * n + 1) * (n / (6 * n + 2))**n * (rzz / Vp)**n * taof / K)
        Reazz = 12**(1 - n) * rhoi * (Dw - Rzz)**n * Va**(2 - n) / K / ((2 * n + 1) / (3 * n))**n / (1 + (2 * n + 1)**(1 - n) / (n + 1) * (n / 4)**n * ((Dw - Rzz) / Va)**n * taof / K)
        Reczz = 3470 - 1370 * n
        taowpzz = taof + K * (8 * Q / np.pi / (rzz / 2)**3)**n
        taowazz = taof + K * (8 * Q / np.pi / ((Dw / 2)**3 - (Rzz / 2)**3))**n
        if Repzz < Reczz:
            fpzz = 16 / Repzz
        else:
            equation = lambda fpzz: 1 / np.sqrt(fpzz) - (2.69 / n - 2.95 + 4.53 / n * np.log10(Repzz * fpzz**(1 - 0.5 * n)) + 4.53 / n * np.log10(1 - taof / taowpzz))
            fp_initial = 0.01
            fpzz = fsolve(equation, fp_initial)[0]
        if Reazz < Reczz:
            fazz = 24 / Reazz
        else:
            equation = lambda fazz: 1 / np.sqrt(fazz) - (2.69 / n - 2.95 + 4.53 / n * np.log10(Reazz * fazz**(1 - 0.5 * n)) + 4.53 / n * np.log10(1 - taof / taowazz))
            fa_initial = 0.01
            fazz = fsolve(equation, fa_initial)[0]
        Ppzz = 2 * fpzz * rhoi * np.arange(1, Lzz + 1).reshape(-1, 1) * Vp**2 / rzz / 10**6 * 10
        Pazz = 2 * fazz * rhoi * np.arange(1, Lzz + 1).reshape(-1, 1) * Va**2 / (Dw - Rzz) / 10**6 * 10
        Repzt = 8**(1 - n) * rhoi * rzt**n * Vpzt**(2 - n) / K / ((3 * n + 1) / (4 * n))**n / (1 + (3 * n + 1) / (2 * n + 1) * (n / (6 * n + 2))**n * (rzt / Vpzt)**n * taof / K)
        Reazt = 12**(1 - n) * rhoi * (Dw - Rzt)**n * Vazt**(2 - n) / K / ((2 * n + 1) / (3 * n))**n / (1 + (2 * n + 1)**(1 - n) / (n + 1) * (n / 4)**n * ((Dw - Rzt) / Vazt)**n * taof / K)
        Reczt = 3470 - 1370 * n
        taowpzt = taof + K * (8 * Q / np.pi / (rzt / 2)**3)**n
        taowazt = taof + K * (8 * Q / np.pi / ((Dw / 2)**3 - (Rzt / 2)**3))**n
        if Repzt < Reczt:
            fpzt = 16 / Repzt
        else:
            equation = lambda fpzt: 1 / np.sqrt(fpzt) - (2.69 / n - 2.95 + 4.53 / n * np.log10(Repzt * fpzt**(1 - 0.5 * n)) + 4.53 / n * np.log10(1 - taof / taowpzt))
            fp_initial = 0.01
            fpzt = fsolve(equation, fp_initial)[0]
        if Reazt < Reczt:
            fazt = 24 / Reazt
        else:
            equation = lambda fazt: 1 / np.sqrt(fazt) - (2.69 / n - 2.95 + 4.53 / n * np.log10(Reazt * fazt**(1 - 0.5 * n)) + 4.53 / n * np.log10(1 - taof / taowazt))
            fa_initial = 0.01
            fazt = fsolve(equation, fa_initial)[0]
        Ppzt = 2 * fpzt * rhoi * np.arange(1, Lzt + 1).reshape(-1, 1) * Vpzt**2 / rzt / 10**6 * 10
        Pazt = 2 * fazt * rhoi * np.arange(1, Lzt + 1).reshape(-1, 1) * Vazt**2 / (Dw - Rzt) / 10**6 * 10

    Ppztt = Ppzz[-1] + Ppzt
    Paztt = Pazz[-1] + Pazt
    Ppp = np.vstack((Ppzz, Ppztt))
    Paa = np.vstack((Pazz, Paztt))
    Pp = fjt * Ppp / 10
    Pa = Paa / 10

    Length, Xs, Ys, Zs = deal_input_data(data)
    cs = Xs[0] - Xs
    aa = data[:, 0]
    T = cs
    aacs = np.arange(1, max(aa) + 1).reshape(-1, 1)
    Tcs = CubicSpline(aa, T, bc_type='natural')(aacs)

    if yx == 0:
        Phk