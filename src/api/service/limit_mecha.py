import numpy as np
from pathlib import Path
from scipy.optimize import fsolve, least_squares
from scipy.interpolate import interp1d
from functools import partial
import pandas as pd
from entity.DTO import LimitMechanismDTO
from scipy.interpolate import interp1d
from service import utils
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

from service.torque import data_recovery, odefunc,  deal_curve_data, spline_interp


def mainfunc(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, qfqd, jsjg, v, omega):
    data1 = guiji
    data2 = zuanju
    working_condition = wc

    if working_condition == 1:
        # 输入参数
        T0 = T0  # 钻压，N
        rhoi = rhoi  # 钻井液密度，kg/m3
        Dw = Dw  # 井眼直径，m
        tgxs = tgxs  # 套管下深，m
        miua1 = miua11 / 30  # 套管段摩阻系数
        miua2 = miua22 / 30  # 裸眼段摩阻系数
        miut1 = miua11 * 1.2  # 套管段切向摩阻系数
        miut2 = miua22 * 1.2  # 裸眼段切向摩阻系数
        qfqd = qfqd  # 钻柱屈服强度，MPa
        jsjg = jsjg  # 计算井深间隔，m

        # 固定值
        M0 = abs(T0 * Dw / 3 * 0.5)  # 钻头扭矩
        v = v  # 钻进速度，m/s
        omega = omega  # 转速，rad/s
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        sign1 = 1  # 钻柱运动方向：1下入；-1上提
        sign2 = 1  # 钻柱是否旋转：1旋转；0不旋转

    elif working_condition == 2:
        # 输入参数
        T0 = T0  # 钻压，N
        rhoi = rhoi  # 钻井液密度，kg/m3
        Dw = Dw  # 井眼直径，m
        tgxs = tgxs  # 套管下深，m
        miua1 = miua11 * 1.165  # 套管段摩阻系数
        miua2 = miua22 * 1.165  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        qfqd = qfqd  # 钻柱屈服强度，MPa
        jsjg = jsjg  # 计算井深间隔，m

        # 固定值
        M0 = 0  # 钻头扭矩
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        v = 1  # 钻进速度，m/s
        omega = 0  # 转速，rad/s
        sign1 = 1  # 钻柱运动方向：1下入；-1上提
        sign2 = 0  # 钻柱是否旋转：1旋转；0不旋转

    elif working_condition == 3:
        # 输入参数
        rhoi = rhoi  # 钻井液密度，kg/m3
        Dw = Dw  # 井眼直径，m
        tgxs = tgxs  # 套管下深，m
        miua1 = miua11 * 1.09  # 套管段摩阻系数
        miua2 = miua22 * 1.09  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        qfqd = qfqd  # 钻柱屈服强度，MPa
        jsjg = jsjg  # 计算井深间隔，m

        # 固定值
        T0 = 0  # 钻压，N
        M0 = 0  # 钻头扭矩
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        v = 1  # 上提速度，m/s
        omega = 0  # 转速，rad/s
        sign1 = -1  # 钻柱运动方向：1下入；-1上提
        sign2 = 0  # 钻柱是否旋转：1旋转；0不旋转

    elif working_condition == 4:
        # 输入参数
        rhoi = rhoi  # 钻井液密度，kg/m3
        Dw = Dw  # 井眼直径，m
        tgxs = tgxs  # 套管下深，m
        miua1 = miua11 * 1.17  # 套管段摩阻系数
        miua2 = miua22 * 1.17  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        qfqd = qfqd  # 钻柱屈服强度，MPa
        jsjg = jsjg  # 计算井深间隔，m

        # 固定值
        T0 = 0  # 钻压，N
        M0 = 0  # 钻头扭矩
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        v = 1  # 下放速度，m/s
        omega = 0  # 转速，rad/s
        sign1 = 1  # 钻柱运动方向：1下入；-1上提
        sign2 = 0  # 钻柱是否旋转：1旋转；0不旋转

    elif working_condition == 5:
        # 输入参数
        rhoi = rhoi  # 钻井液密度，kg/m3
        Dw = Dw  # 井眼直径，m
        tgxs = tgxs  # 套管下深，m
        miua1 = miua11 / 1.5  # 套管段摩阻系数
        miua2 = miua22 / 1.5  # 裸眼段摩阻系数
        miut1 = miua11 * 1.2  # 套管段切向摩阻系数
        miut2 = miua22 * 1.2  # 裸眼段切向摩阻系数
        qfqd = qfqd  # 钻柱屈服强度，MPa
        jsjg = jsjg  # 计算井深间隔，m

        # 固定值
        T0 = 0  # 钻压，N
        M0 = 0  # 钻头扭矩，N·m
        v = v  # 上提速度，m/s
        omega = omega  # 转速，rad/s
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        sign1 = -1  # 钻柱运动方向：1下入；-1上提
        sign2 = 1  # 钻柱是否旋转：1旋转；0不旋转

        # 基础参数
    rhoo = rhoi  # 钻柱外流体密度
    T0 = -T0  # 反转钻压
    g = 9.81  # 重力加速度
    E = 2.1e11  # 钻柱弹性模量

    jd = guiji[:, 0]
    yssd = jd[-1]  # 取数组最后一个元素的值

    # 计算迭代次数
    num_iterations = int(np.ceil(yssd / jsjg))

    # 创建结果数组
    T_result = np.zeros((num_iterations * jsjg, num_iterations))
    M_result = np.zeros((num_iterations * jsjg, num_iterations))
    aq_result = np.zeros((num_iterations * jsjg, num_iterations))

    # 进行迭代
    for nn in range(1, num_iterations + 1):
        if nn == num_iterations:
            # 最后一次迭代时使用 guiji 最后的值
            js = yssd
        else:
            # 否则按正常的间隔计算
            js = nn * jsjg

        # 钻具长度确定
        row_data = zuanju[3, :-1]
        row_sum = np.sum(row_data)
        zuanju[3, -1] = js - row_sum

        # 钻具组合参数
        Dtrans = zuanju[0, :]  # 钻柱外径，m
        dtrans = zuanju[1, :]  # 钻柱内径，m
        mtrans = 9.81 * zuanju[2, :]  # 钻柱组合线重，N/m
        ltrans = zuanju[3, :]

        # 钻具组合参数
        Ntrans = len(Dtrans)  # 所加载的钻具组合数量
        nntrans = np.zeros(Ntrans)  # 即nntrans的前n项累加
        ntrans = np.sum(ltrans)  # 所加载的钻具组合总分段数（计算步长）
        ntrans = int(ntrans)

        Rt = np.zeros(ntrans)  # 各段钻具组合外半径/m
        rt = np.zeros(ntrans)  # 各段钻具组合内半径/m
        Aot = np.zeros(ntrans)  # 各段钻具组合外截面积/m^2
        Ait = np.zeros(ntrans)  # 各段钻具组合内截面积/m^2
        qt = np.zeros(ntrans)  # 各段钻具组合线重/N.m^-1
        qmt = np.zeros(ntrans)  # 各段钻具组合浮重/N.m^-1
        Kft = np.zeros(ntrans)  # 浮力系数
        It = np.zeros(ntrans)  # 惯性矩
        ht = np.zeros(ntrans)  # 壁厚

        # 计算nntrans，便于后续计算
        nntrans[0] = ltrans[0]
        for i in range(1, Ntrans):
            nntrans[i] = nntrans[i - 1] + ltrans[i]

        # 计算钻具组合各分段的半径、截面积、线重
        for i in range(Ntrans):
            if i == 0:
                for j in range(int(nntrans[i])):
                    Rt[j] = Dtrans[i] / 2
                    rt[j] = dtrans[i] / 2
                    Aot[j] = np.pi * Rt[j] ** 2
                    Ait[j] = np.pi * rt[j] ** 2
                    qt[j] = mtrans[i]
                    qmt[j] = qt[j] - (Aot[j] - Ait[j]) * rhoi * g
                    Kft[j] = qmt[j] / qt[j]
                    It[j] = np.pi * (Rt[j] ** 4 - rt[j] ** 4) / 8
                    ht[j] = Rt[j] - rt[j]
            else:
                for j in range(int(nntrans[i - 1]), int(nntrans[i])):
                    Rt[j] = Dtrans[i] / 2
                    rt[j] = dtrans[i] / 2
                    Aot[j] = np.pi * Rt[j] ** 2
                    Ait[j] = np.pi * rt[j] ** 2
                    qt[j] = mtrans[i]
                    qmt[j] = qt[j] - (Aot[j] - Ait[j]) * rhoi * g
                    Kft[j] = qmt[j] / qt[j]
                    It[j] = np.pi * (Rt[j] ** 4 - rt[j] ** 4) / 8
                    ht[j] = Rt[j] - rt[j]

        # 计算参数
        ds = 1  # 步长
        len_calc = ntrans - 1  # 计算长度
        sspan = np.arange(0, len_calc + 1, ds)
        miua = np.zeros(ntrans)
        miut = np.zeros(ntrans)

        for i in range(ntrans):
            if i >= ntrans - tgxs:
                miua[i] = miua1
                miut[i] = miut1
            else:
                miua[i] = miua2
                miut[i] = miut2

        # 处理井眼轨迹函数
        Mk, mk, Sk, alphak, phik = deal_curve_data(guiji, js)

        # 初始化k和tao等参数
        alpha, phi, ks, dks, ddks, kphis, kalphas, taos = prepare_data(sspan, Mk, mk, Sk, alphak, phik)

        # 开始计算
        Ttemp = T0
        Mtemp = M0
        Nbtemp = 0
        Nntemp = 0

         # 调用封装函数
        s, y = matlab_ode_wrapper(
            len_calc=len_calc,  # 计算长度（必须与sspan[-1]一致）
            ds=ds,  # 计算间隔
            T0=T0,  # 初始扭矩
            M0=M0,  # 初始弯矩
            ks=ks,  # 曲率数组
            dks=dks,  # 曲率一阶导数数组
            ddks=ddks,  # 曲率二阶导数数组
            kphis=kphis,  # 曲率-phi系数数组
            kalphas=kalphas,  # 曲率-alpha系数数组
            taos=taos,  # 扭矩系数数组
            Rt=Rt,  # 钻具半径数组
            Dw=Dw,  # 井径
            miua=miua,  # 轴向摩擦系数数组
            miut=miut,  # 周向摩擦系数数组
            qmt=qmt,  # 单位长度重量数组
            Ait=Ait,  # 内截面积数组
            Aot=Aot,  # 外截面积数组
            rhoi=rhoi,  # 内流体密度
            rhoo=rhoo,  # 外流体密度
            E=E,  # 弹性模量
            It=It,  # 惯性矩数组
            g=g,  # 重力加速度
            Mk=Mk,  # 样条alpha二阶导数数组
            mk=mk,  # 样条phi二阶导数数组
            Sk=Sk,  # 样条节点位置数组
            alphak=alphak,  # 样条alpha节点值
            phik=phik,  # 样条phi节点值
            v=v,  # 钻速
            omega=omega,  # 转速
            taof=taof,  # 流体剪切应力
            miu=miu,  # 流体摩擦系数
            sign1=sign1,  # 方向标志1
            sign2=sign2  # 方向标志2
        )

        T = y[:, 0]
        M = y[:, 1]
        T = np.flipud(T)

        # 数据恢复
        Nbtemp = 0
        Nntemp = 0
        Ttemp = T0
        Mtemp = M0

        N, Nn, Nb = data_recovery(s, y, ks, dks, ddks, kphis, kalphas, taos, sspan, v, omega, taof,
                                  miu, Rt, Dw, miua, miut, qmt, Ait, Aot, rhoi, rhoo, E, It, g, Mk,
                                  mk, Sk, alphak, phik, Ttemp, Mtemp, Nbtemp, Nntemp, sign1, sign2)

        # 表达摩阻
        for i in range(ntrans):
            if i < 28:
                N[i] = N[i] * 0.3157407408

        F = np.zeros(len(N))
        for i in range(ntrans):
            F[i] = N[i] * miua[i]

        # 原累计摩阻
        Flj = np.zeros(len(N))
        Flj[0] = N[0] * miua[0]
        for i in range(1, ntrans):
            Flj[i] = Flj[i - 1] + N[i] * miua[i]

        # 输出
        alpha = np.flipud(alpha) * 180 / np.pi
        phi = np.flipud(phi) * 180 / np.pi
        T = T / 1000
        M = np.flipud(M) / 1000
        F = np.flipud(F)
        Flj = np.flipud(Flj) / 1000

        if working_condition == 2 or working_condition == 3 or working_condition == 4:
            M[:] = 0

        aq = qfqd / ((T[0] * 1000 / (np.pi * (((Dtrans[-1] / 2) ** 2) - ((dtrans[-1] / 2) ** 2))) / 1000000))

        T_result[:T.shape[0], nn - 1] = T.reshape(-1)
        M_result[:M.shape[0], nn - 1] = M.reshape(-1)
        aq_result[:np.size(aq), nn - 1] = np.array(aq).reshape(-1)

    Tjk = T_result[0, :].reshape(-1, 1)
    Mjk = M_result[0, :].reshape(-1, 1)
    aqjk = aq_result[0, :].reshape(-1, 1)

    condition_prefix = {
        1: "旋转钻进",
        2: "滑动钻进",
        3: "起钻",
        4: "下钻",
        5: "倒划眼"
    }
    prefix = condition_prefix.get(working_condition, "未知工况")

    timestamp = utils.get_timestamp()

    # 针对不同的结果数据，调用封装函数进行绘图和导出
    x_coords =  plot_and_export(T_result[0, :], '井口轴向力（kN）', f"{prefix}_井口轴向力_{timestamp}.xlsx", jsjg, yssd)
    plot_and_export(M_result[0, :], '井口扭矩（kN·m）', f"{prefix}_井口扭矩_{timestamp}.xlsx", jsjg, yssd)
    plot_and_export(aq_result[0, :], '安全系数', f"{prefix}_安全系数_{timestamp}.xlsx", jsjg, yssd)

    return Tjk, Mjk, aqjk, x_coords

def diff_func(vars, span):
    diff_var = np.zeros_like(vars)

    # Compute the difference
    for i in range(len(vars)):
        if i == 0:
            diff_var[i] = (vars[i + 1] - vars[i]) / (span[i + 1] - span[i])
        elif i == len(vars) - 1:
            diff_var[i] = (vars[-1] - vars[-2]) / (span[-1] - span[-2])
        else:
            diff_var[i] = (vars[i + 1] - vars[i - 1]) / (span[i + 1] - span[i - 1])

    # Smooth the derivative (similar to MATLAB's smooth function)
    # diff_var = savgol_filter(diff_var, window_length=201, polyorder=2)  # Adjust the window size as needed

    return diff_var

def prepare_data(sspan, Mk, mk, Sk, alphak, phik):
    alphas = np.zeros(len(sspan))
    phis = np.zeros(len(sspan))
    taos = np.zeros(len(sspan))

    for i in range(len(sspan)):
        alphas[i], phis[i] = spline_interp(Mk, mk, Sk, alphak, phik, sspan[i])

    kphis = diff_func(phis, sspan)
    kalphas = diff_func(alphas, sspan)

    ks = np.sqrt(kalphas ** 2 + kphis ** 2 * np.sin(alphas) ** 2)
    dks = diff_func(ks, sspan)
    ddks = diff_func(dks, sspan)

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

        # Calculate theta using the provided formula
        term1 = (da ** 2 / edl ** 2) * np.cos(dp)
        term2 = (da * dp / edl ** 2) * (np.sin(alpha2) * np.cos(alpha2) - np.sin(alpha1) * np.cos(alpha1)) * np.sin(dp)
        term3 = (dp ** 2 / edl ** 2) * np.sin(alpha1) * np.sin(alpha2) * (
                    np.sin(alpha1) * np.sin(alpha2) + np.cos(alpha1) * np.cos(alpha2) * np.cos(dp))
        theta = np.arccos(term1 - term2 + term3)

        # Force theta to be real (in case of small imaginary parts due to numerical error)
        theta = np.real(theta)

        # Compute taos at the current index
        taos[i] = theta / ds

    # Replace any NaN values in taos with 0
    taos = np.where(np.isnan(taos), 0, taos)
    return alphas, phis, ks, dks, ddks, kphis, kalphas, taos

def plot_and_export(data, ylabel, filename, jsjg, yssd):
    """
    绘制图像并导出 Excel 文件。

    参数:
        data: 1D NumPy 数组，表示井口数据（例如轴向力、扭矩或安全系数）。
        ylabel: y 轴标签，例如 '井口轴向力（kN）'。
        filename: 导出的 Excel 文件名。
        jsjg: 井深间隔（标量），用于计算横坐标。
        yssd: 最终深度（标量），作为横坐标的最后一个点。
    """
    # data 的长度应与 x 坐标长度一致
    n = data.shape[0]
    # 计算横坐标：前 n-1 个点为 jsjg * (1, 2, ..., n-1)，最后一个点为 yssd
    x_coords = np.concatenate((jsjg * np.arange(1, n), [yssd]))

    output = utils.get_output_folder("机械延伸极限")


    # 合并数据并导出到 Excel（无索引和表头）
    export_data = np.column_stack((x_coords, data))
    pd.DataFrame(export_data).to_excel( output / filename, index=False, header=False)
    return x_coords


def spline_interp(Mk, mk, Sk, alphak, phik, S0):
    """与MATLAB完全一致的三次样条插值实现"""
    Sk = np.asarray(Sk)
    idx = np.searchsorted(Sk, S0, side='right') - 1
    idx = np.clip(idx, 0, len(Sk) - 2)

    M0, M1 = Mk[idx], Mk[idx + 1]
    m0, m1 = mk[idx], mk[idx + 1]
    alpha0, alpha1 = alphak[idx], alphak[idx + 1]
    phi0, phi1 = phik[idx], phik[idx + 1]
    Sl, Sr = Sk[idx], Sk[idx + 1]
    Lk = Sr - Sl

    C1 = alpha1 / Lk - M1 * Lk / 6
    C0 = alpha0 / Lk - M0 * Lk / 6
    c1 = phi1 / Lk - M1 * Lk / 6
    c0 = phi0 / Lk - M0 * Lk / 6

    alphacal = (M0 * (Sr - S0) ** 3) / (6 * Lk) + (M1 * (S0 - Sl) ** 3) / (6 * Lk) + C1 * (S0 - Sl) + C0 * (Sr - S0)
    phical = (m0 * (Sr - S0) ** 3) / (6 * Lk) + (m1 * (S0 - Sl) ** 3) / (6 * Lk) + c1 * (S0 - Sl) + c0 * (Sr - S0)

    return alphacal, phical


def solve_func(x, M, T, k, dk, ddk, alpha, tao, kphi, kalpha, R, taof, v, miu, Dw, E, I, miua, miut, omega, flambda, qm,
               rhoi, rhoo, Ai, Ao, g, sign1, sign2):
    """与MATLAB完全一致的隐式方程定义"""
    dT, dM, Nn, Nb = x
    if abs(k) > 1e-12:
        return [
            dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb ** 2 + Nn ** 2) + sign2 * flambda - qm * np.cos(alpha),
            k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn - (
                        (qm + rhoi * g * Ai - rhoo * g * Ao) * kphi / k * np.sin(alpha) ** 2),
            dM - (miut * R * np.sqrt(Nb ** 2 + Nn ** 2) + sign2 * 2 * np.pi * R ** 3 * omega * (
                        taof / np.sqrt(v ** 2 + (R * omega) ** 2) + 2 * miu / (Dw - 2 * R))),
            E * I * ddk - k * T + Nn + miut * Nb - ((qm + rhoi * g * Ai - rhoo * g * Ao) * kalpha / k * np.sin(alpha))
        ]
    else:
        return [
            dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb ** 2 + Nn ** 2) + sign2 * flambda - qm * np.cos(alpha),
            k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn,
            dM - (miut * R * np.sqrt(Nb ** 2 + Nn ** 2) + sign2 * 2 * np.pi * R ** 3 * omega * (
                        taof / np.sqrt(v ** 2 + (R * omega) ** 2) + 2 * miu / (Dw - 2 * R))),
            E * I * ddk - k * T + Nn + miut * Nb
        ]


def matlab_ode_wrapper(len_calc, ds, T0, M0,
                       ks, dks, ddks, kphis, kalphas, taos,
                       Rt, Dw, miua, miut, qmt,
                       Ait, Aot, rhoi, rhoo, E, It, g,
                       Mk, mk, Sk, alphak, phik,
                       v, omega, taof, miu,
                       sign1, sign2):
    """与MATLAB算法完全等价的Python封装函数"""
    # 生成计算点数组 (与MATLAB的0:ds:len_calc完全一致)
    sspan = np.arange(0, len_calc + ds, ds)
    sspan[-1] = min(sspan[-1], len_calc)  # 确保不超出总长

    # 预创建插值器 (使用MATLAB默认的spline方法)
    interps = {
        'k': interp1d(sspan, ks, 'cubic', fill_value='extrapolate'),
        'dk': interp1d(sspan, dks, 'cubic', fill_value='extrapolate'),
        'ddk': interp1d(sspan, ddks, 'cubic', fill_value='extrapolate'),
        'kphi': interp1d(sspan, kphis, 'cubic', fill_value='extrapolate'),
        'kalpha': interp1d(sspan, kalphas, 'cubic', fill_value='extrapolate'),
        'tao': interp1d(sspan, taos, 'cubic', fill_value='extrapolate')
    }

    # 状态容器 (模拟MATLAB的持久变量)
    class State:
        def __init__(self):
            self.history = []
            self.Ttemp = T0
            self.Mtemp = M0
            self.Nntemp = 0.0
            self.Nbtemp = 0.0

        def update(self, x):
            self.history.append(x)
            if len(self.history) > 5:
                self.history.pop(0)
            self.Ttemp, self.Mtemp, self.Nntemp, self.Nbtemp = np.mean(self.history, axis=0)
    state = State()

    # ODE函数定义
    def odefunc(s, y):
        nonlocal state
        T, M = y[0], y[1]

        # 参数插值
        k = interps['k'](s)
        dk = interps['dk'](s)
        ddk = interps['ddk'](s)
        kphi = interps['kphi'](s)
        kalpha = interps['kalpha'](s)
        tao = interps['tao'](s)

        # 样条插值alpha
        alpha, _ = spline_interp(Mk, mk, Sk, alphak, phik, s)

        # 修正索引计算，避免浮点误差
        a = min(int(np.ceil(s + 1e-9)) + 1, len(Rt) - 1)
        R = Rt[a]
        Ai = Ait[a]
        Ao = Aot[a]
        qm = qmt[a]
        I = It[a]
        miua_val = miua[a]
        miut_val = miut[a]

        # 流体阻力计算 (完全复现MATLAB公式)
        flambda = v * (
                2 * np.pi * R * taof / np.sqrt(v ** 2 + (R * omega) ** 2) +
                4 * np.pi * R * miu / np.log(Dw / (2 * R))
        )

        # 隐式方程求解 (初始猜测来自前一步状态)
        result = least_squares(
            lambda x: solve_func(x, M, T, k, dk, ddk, alpha, tao, kphi, kalpha,
                                 R, taof, v, miu, Dw, E, I, miua_val, miut_val,
                                 omega, flambda, qm, rhoi, rhoo, Ai, Ao, g,
                                 sign1, sign2),
            x0=[state.Ttemp, state.Mtemp, state.Nntemp, state.Nbtemp],
            method='lm',
            # xtol=1e-8,
            ftol=1e-10,
            max_nfev=200
        )

        x = result.x

        # 监控残差
        if not result.success:
            print(f"求解失败于 s={s:.2f}, 残差={np.linalg.norm(result.fun):.2e}")
        # 在odefunc中添加调试代码
        if abs(s - 4000) < 1e-6:
            print("===== 4000m处调试信息 =====")
            print(f"初始猜测: Ttemp={state.Ttemp:.2e}, Mtemp={state.Mtemp:.2e}")
            print(f"参数解: x={result.x}")
            print(f"残差范数: {result.cost:.2e}")
            print(f"终止原因: {result.message}")

        state.update(x)
        return [x[0], x[1]]

    # 执行数值积分 (严格匹配MATLAB的ode45默认设置)
    result = solve_ivp(
        fun=odefunc,
        t_span=[0, len_calc],
        y0=[T0, M0],
        t_eval=sspan,
        method='RK45',
        rtol=1e-8,  # 对应MATLAB默认相对容差
        atol=1e-10  # 对应MATLAB默认绝对容差
    )

    return result.t, result.y.T




def main(dto: LimitMechanismDTO ):
    # 读取井眼轨迹数据，并转换为 NumPy 数组
    guiji = pd.read_excel(dto.file_path1, header=None).values
    zuanju = pd.read_excel(dto.file_path2, header=None).values

    # 输出参数（调试用）
    print("参数初始化完成，准备进行计算...")

    return mainfunc(guiji, zuanju, dto.wc, dto.T0, dto.rhoi, dto.Dw, dto.tgxs, dto.miua11, dto.miua22, dto.qfqd, dto.jsjg, dto.v, dto.omega)










