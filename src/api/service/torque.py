import numpy as np
from pathlib import Path
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from service import utils
from service.mecha_utils import matlab_ode_wrapper, spline_interp
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import os

def mainfunc(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, js, v, omega):
    data1 = guiji
    data2 = zuanju
    working_condition = wc  # 工况选择：1旋转钻进；2滑动钻进；3起钻；4下钻；5倒划眼

    if working_condition == 1:
        # 输入参数
        miua1 = miua11 / 30  # 套管段摩阻系数
        miua2 = miua22 / 30  # 裸眼段摩阻系数
        miut1 = miua11 * 1.2  # 套管段切向摩阻系数
        miut2 = miua22 * 1.2  # 裸眼段切向摩阻系数
        
        # 固定值
        M0 = abs(T0 * Dw / 3 * 0.5)  # 钻头扭矩
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        sign1 = 1  # 钻柱运动方向：1下入；-1上提
        sign2 = 1  # 钻柱是否旋转：1旋转；0不旋转
    
    elif working_condition == 2:
        # 输入参数
        miua1 = miua11 * 1.165  # 套管段摩阻系数
        miua2 = miua22 * 1.165  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        
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
        miua1 = miua11 * 1.09  # 套管段摩阻系数
        miua2 = miua22 * 1.09  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        
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
        miua1 = miua11 * 1.17  # 套管段摩阻系数
        miua2 = miua22 * 1.17  # 裸眼段摩阻系数
        miut1 = 0  # 套管段切向摩阻系数
        miut2 = 0  # 裸眼段切向摩阻系数
        
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
        miua1 = miua11 / 1.5  # 套管段摩阻系数
        miua2 = miua22 / 1.5  # 裸眼段摩阻系数
        miut1 = miua11 * 1.2  # 套管段切向摩阻系数
        miut2 = miua22 * 1.2  # 裸眼段切向摩阻系数
        
        # 固定值
        T0 = 0  # 钻压，N
        M0 = 0  # 钻头扭矩，N·m
        miu = 0.2  # 钻井液塑性粘度，mPa·s
        taof = 14  # 钻井液屈服值，Pa
        sign1 = -1  # 钻柱运动方向：1下入；-1上提
        sign2 = 1  # 钻柱是否旋转：1旋转；0不旋转
    
    # 基础参数
    rhoo = rhoi  # 钻柱外流体密度
    T0 = -T0
    g = 9.81  # 重力加速度
    E = 2.1e11  # 钻柱弹性模量
    
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
        nntrans[i] = nntrans[i-1] + ltrans[i]
    
    # 计算钻具组合各分段的半径、截面积、线重
    for i in range(Ntrans):
        if i == 0:
            for j in range(int(nntrans[i])):
                Rt[j] = Dtrans[i] / 2
                rt[j] = dtrans[i] / 2
                Aot[j] = np.pi * Rt[j]**2
                Ait[j] = np.pi * rt[j]**2
                qt[j] = mtrans[i]
                qmt[j] = qt[j] - (Aot[j] - Ait[j]) * rhoi * g
                Kft[j] = qmt[j] / qt[j]
                It[j] = np.pi * (Rt[j]**4 - rt[j]**4) / 8
                ht[j] = Rt[j] - rt[j]
        else:
            for j in range(int(nntrans[i-1]), int(nntrans[i])):
                Rt[j] = Dtrans[i] / 2
                rt[j] = dtrans[i] / 2
                Aot[j] = np.pi * Rt[j]**2
                Ait[j] = np.pi * rt[j]**2
                qt[j] = mtrans[i]
                qmt[j] = qt[j] - (Aot[j] - Ait[j]) * rhoi * g
                Kft[j] = qmt[j] / qt[j]
                It[j] = np.pi * (Rt[j]**4 - rt[j]**4) / 8
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
    
    # # 使用scipy的solve_ivp代替MATLAB的ode45
    # def odefun(s, y):
    #     return odefunc(s, y, ks, dks, ddks, kphis, kalphas, taos, sspan, v, omega, taof, miu,
    #                   Rt, Dw, miua, miut, qmt, Ait, Aot, rhoi, rhoo, E, It, g, Mk, mk, Sk,
    #                   alphak, phik, Ttemp, Mtemp, Nbtemp, Nntemp, sign1, sign2)
    
    # # 数值积分求解
    # result = solve_ivp(odefun, [0, len_calc], [T0, M0], method='RK45', t_eval=sspan, rtol=1e-3, atol=1e-6)
    
    # s = result.t
    # y = result.y.T
    
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
        Flj[i] = Flj[i-1] + N[i] * miua[i]
    
    # 输出
    alpha = np.flipud(alpha) * 180 / np.pi
    phi = np.flipud(phi) * 180 / np.pi
    T = T / 1000
    M = np.flipud(M) / 1000
    F = np.flipud(F)
    Flj = np.flipud(Flj) / 1000
    
    if working_condition == 2 or working_condition == 3 or working_condition == 4:
        M[:] = 0
    
    # 垂深计算
    Length, Xs, Ys, Zs = deal_input_data(guiji)
    cs = Xs[0] - Xs
    
    # 垂深插值
    aa = guiji[:, 0]
    Tzz = cs
    aacs = np.arange(1, np.max(aa) + 1)
    Tcs = np.interp(aacs, aa, Tzz)
    Tcs = Tcs[:js]
    
    # 输出各工况结果
    # 旋转钻进
    output_folder = create_output_folder(working_condition)

    # 首先计算井位置信息，供所有工况使用
    Sk = np.arange(len(T))
    N_pos = np.zeros(len(Sk))
    E_pos = np.zeros(len(Sk))
    
    for i in range(1, len(Sk)):
        dSk = Sk[i] - Sk[i-1]
        N_pos[i] = N_pos[i-1] + dSk * np.sin(np.radians(alpha[i])) * np.cos(np.radians(phi[i]))
        E_pos[i] = E_pos[i-1] + dSk * np.sin(np.radians(alpha[i])) * np.sin(np.radians(phi[i]))
    
    if working_condition == 1:
        save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, "旋转钻进")
    elif working_condition == 2:
        save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, "滑动钻进")
    elif working_condition == 3:
        save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, "起钻")
    elif working_condition == 4:
        save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, "下钻")
    elif working_condition == 5:
        save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, "倒划眼")
    
    return N_pos, E_pos, Tcs, T, M, Sk

def get_download_folder():
        """ 获取当前操作系统的下载文件夹路径 """
        if os.name == 'nt':  # Windows
            return Path(os.environ['USERPROFILE']) / 'Downloads'
        elif os.name == 'posix':  # macOS/Linux
            return Path.home() / 'Downloads'
        else:
            raise Exception("Unsupported OS")

def create_output_folder(working_condition):
    condition_names = {
        1: "旋转钻进",
        2: "滑动钻进",
        3: "起钻",
        4: "下钻",
        5: "倒划眼"
    }

    download_folder = utils.get_output_folder("摩阻扭矩")
    
    # 创建输出目录
    folder_name = condition_names.get(working_condition, "未知工况")
    output_folder = download_folder / "" / folder_name

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder
    

def save_results(T, M, Sk, E_pos, N_pos, Tcs, output_folder, prefix):
    time = utils.get_timestamp()
    # 保存数据到CSV文件
    pd.DataFrame(T).to_excel(f"{output_folder}/{prefix}_轴向力_{time}.xlsx", header=False, index=False)
    pd.DataFrame(M).to_excel(f"{output_folder}/{prefix}_扭矩_{time}.xlsx", header=False, index=False)
    

def odefunc(s, y, ks, dks, ddks, kphis, kalphas, taos, sspan, v, omega, taof, miu, Rt, Dw, miua, miut, qmt,
           Ait, Aot, rhoi, rhoo, E, It, g, Mk, mk, Sk, alphak, phik, Ttemp, Mtemp, Nbtemp, Nntemp, sign1, sign2):
    T = y[0]
    M = y[1]
    
    # 计算alpha phi
    alpha, _ = spline_interp(Mk, mk, Sk, alphak, phik, s)
    
    # 利用准备的数据进行插值
    k = np.interp(s, sspan, ks)
    dk = np.interp(s, sspan, dks)
    ddk = np.interp(s, sspan, ddks)
    kphi = np.interp(s, sspan, kphis)
    kalpha = np.interp(s, sspan, kalphas)
    tao = np.interp(s, sspan, taos)
    
    # 输入钻具组合相关数据
    a = int(np.ceil(s)) + 1
    if a >= len(Rt):
        a = len(Rt) - 1
    
    R = Rt[a]
    Ao = Aot[a]
    Ai = Ait[a]
    qm = qmt[a]
    I = It[a]
    at = Rt[a]
    miua_val = miua[a]
    miut_val = miut[a]
    
    flambda = v * (2 * np.pi * at * taof / np.sqrt(v**2 + (at * omega)**2) + 4 * np.pi * at * miu / np.log(Dw / 2 / at))
    
    # 使用fsolve求解非线性方程组
    def solve_func(x, M, T, k, dk, ddk, alpha, tao, kphi, kalpha, R, taof, v, miu, Dw, E, I, miua, miut, omega, flambda, qm, rhoi, rhoo, Ai, Ao, g, sign1, sign2):
        dT, dM, Nn, Nb = x
        
        if abs(k) > 1e-10:
            f = [
                dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb**2 + Nn**2) + sign2 * flambda - qm * np.cos(alpha),
                k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn - ((qm + rhoi * g * Ai - rhoo * g * Ao) * kphi / k * np.sin(alpha) * np.sin(alpha)),
                dM - (miut * R * np.sqrt(Nb**2 + Nn**2) + sign2 * 2 * np.pi * R**3 * omega * (taof / np.sqrt(v**2 + (R * omega)**2) + 2 * miu / (Dw - 2 * R))),
                E * I * ddk - k * T + Nn + miut * Nb - ((qm + rhoi * g * Ai - rhoo * g * Ao) * kalpha / k * np.sin(alpha))
            ]
        else:
            f = [
                dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb**2 + Nn**2) + sign2 * flambda - qm * np.cos(alpha),
                k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn,
                dM - (miut * R * np.sqrt(Nb**2 + Nn**2) + sign2 * 2 * np.pi * R**3 * omega * (taof / np.sqrt(v**2 + (R * omega)**2) + 2 * miu / (Dw - 2 * R))),
                E * I * ddk - k * T + Nn + miut * Nb
            ]
        
        return f
    
    # 初始猜测值
    initial_guess = [Ttemp, Mtemp, Nntemp, Nbtemp]
    
    # 求解非线性方程组
    solution = fsolve(solve_func, initial_guess, args=(M, T, k, dk, ddk, alpha, tao, kphi, kalpha, R, taof, v, miu, Dw, E, I, miua_val, miut_val, omega, flambda, qm, rhoi, rhoo, Ai, Ao, g, sign1, sign2))
    
    # 更新初始条件
    Ttemp = solution[0]
    Mtemp = solution[1]
    Nntemp = solution[2]
    Nbtemp = solution[3]
    
    # 返回导数
    dyds = np.zeros(2)
    dyds[0] = solution[0]
    dyds[1] = solution[1]
    
    return dyds

def data_recovery(sall, yall, ks, dks, ddks, kphis, kalphas, taos, sspan, v, omega, taof, miu, Rt, Dw, amiu, tmiu, qmt,
                 Ait, Aot, rhoi, rhoo, E, It, g, Mk, mk, Sk, alphak, phik, Ttemp, Mtemp, Nbtemp, Nntemp, sign1, sign2):
    N = np.zeros(len(sall))
    Nb = np.zeros(len(sall))
    Nn = np.zeros(len(sall))
    
    for i in range(len(sall)):
        s = sall[i]
        y = yall[i, :]
        T = y[0]
        M = y[1]
        
        # 计算alpha phi
        alpha, _ = spline_interp(Mk, mk, Sk, alphak, phik, s)
        
        # 利用准备的数据进行插值
        k = np.interp(s, sspan, ks)
        dk = np.interp(s, sspan, dks)
        ddk = np.interp(s, sspan, ddks)
        kphi = np.interp(s, sspan, kphis)
        kalpha = np.interp(s, sspan, kalphas)
        tao = np.interp(s, sspan, taos)
        
        # 输入钻具组合相关数据
        a = int(np.ceil(s)) + 1
        if a >= len(Rt):
            a = len(Rt) - 1
            
        R = Rt[a]
        Ao = Aot[a]
        Ai = Ait[a]
        qm = qmt[a]
        I = It[a]
        at = Rt[a]
        miua_val = amiu[a]
        miut_val = tmiu[a]
        
        flambda = v * (2 * np.pi * at * taof / np.sqrt(v**2 + (at * omega)**2) + 4 * np.pi * at * miu / np.log(Dw / 2 / at))
        
        # 求解非线性方程组
        def solve_func(x, M, T, k, dk, ddk, alpha, tao, kphi, kalpha, R, taof, v, miu, Dw, E, I, miua, miut, omega, flambda, qm, rhoi, rhoo, Ai, Ao, g, sign1, sign2):
            dT, dM, Nn, Nb = x
            
            if abs(k) > 1e-10:
                f = [
                    dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb**2 + Nn**2) + sign2 * flambda - qm * np.cos(alpha),
                    k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn - ((qm + rhoi * g * Ai - rhoo * g * Ao) * kphi / k * np.sin(alpha) * np.sin(alpha)),
                    dM - (miut * R * np.sqrt(Nb**2 + Nn**2) + sign2 * 2 * np.pi * R**3 * omega * (taof / np.sqrt(v**2 + (R * omega)**2) + 2 * miu / (Dw - 2 * R))),
                    E * I * ddk - k * T + Nn + miut * Nb - ((qm + rhoi * g * Ai - rhoo * g * Ao) * kalpha / k * np.sin(alpha))
                ]
            else:
                f = [
                    dT + k * E * I * dk + sign1 * miua * np.sqrt(Nb**2 + Nn**2) + sign2 * flambda - qm * np.cos(alpha),
                    k * dM + M * dk - tao * E * I * dk - Nb + miut * Nn,
                    dM - (miut * R * np.sqrt(Nb**2 + Nn**2) + sign2 * 2 * np.pi * R**3 * omega * (taof / np.sqrt(v**2 + (R * omega)**2) + 2 * miu / (Dw - 2 * R))),
                    E * I * ddk - k * T + Nn + miut * Nb
                ]
            
            return f
        
        # 初始猜测值
        initial_guess = [Ttemp, Mtemp, Nntemp, Nbtemp]
        
        # 求解非线性方程组
        solution = fsolve(solve_func, initial_guess, args=(M, T, k, dk, ddk, alpha, tao, kphi, kalpha, R, taof, v, miu, Dw, E, I, miua_val, miut_val, omega, flambda, qm, rhoi, rhoo, Ai, Ao, g, sign1, sign2))
        
        Nn[i] = solution[2]
        Nb[i] = solution[3]
        N[i] = np.sqrt(solution[2]**2 + solution[3]**2)
        
        Ttemp = solution[0]
        Mtemp = solution[1]
        Nntemp = solution[2]
        Nbtemp = solution[3]
    
    return N, Nn, Nb

def diff_func(vars_data, span):
    diff_var = np.zeros_like(vars_data)
    
    for i in range(len(vars_data)):
        if i == 0:
            diff_var[i] = (vars_data[i+1] - vars_data[i]) / (span[i+1] - span[i])
        elif i == len(vars_data) - 1:
            diff_var[i] = (vars_data[-1] - vars_data[-2]) / (span[-1] - span[-2])
        else:
            diff_var[i] = (vars_data[i+1] - vars_data[i-1]) / (span[i+1] - span[i-1])
    
    # # 对导数进行光滑处理
    # window_length = min(101, len(diff_var))
    # if window_length % 2 == 0:
    #     window_length -= 1
    
    # if window_length >= 3:
        # diff_var = savgol_filter(diff_var, window_length, 3)
    
    return diff_var

def deal_input_data(data):
    n = data.shape[0]
    Xs = np.zeros(n)
    Ys = np.zeros(n)
    Zs = np.zeros(n)
    Length = np.zeros(n)
    Length = data[:, 0].copy()
    
    for i in range(1, n):
        alpha1 = data[i-1, 1] / 180 * np.pi
        alpha2 = data[i, 1] / 180 * np.pi
        phi1 = data[i-1, 2] / 180 * np.pi
        phi2 = data[i, 2] / 180 * np.pi
        
        ppp = abs(phi1 - phi2)
        if ppp > np.pi and phi1 < np.pi:
            phi1 = phi1 + 2 * np.pi
        elif ppp > np.pi and phi1 > np.pi:
            phi1 = phi1 - 2 * np.pi
        
        ds = data[i, 0] - data[i-1, 0]
        
        if alpha1 != alpha2 and phi1 != phi2:
            dx = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            dy = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
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
        
        Xs[i] = Xs[i-1] + dx
        Ys[i] = Ys[i-1] + dy
        Zs[i] = Zs[i-1] + dz
    
    # 从井底到井口的数据
    Length = data[-1, 0] - Length
    Xs0 = Xs[-1] - Xs
    Ys0 = Ys[-1] - Ys
    Zs0 = Zs[-1] - Zs
    
    # 保持坐标系定义一致
    Xs = Zs0
    Ys = Xs0
    Zs = Ys0
    
    return Length, Xs, Ys, Zs

def deal_curve_data(data, js):
    S = data[:, 0]
    alphaa = data[:, 1]
    phia = data[:, 2]
    n = int(js)
    
    alphas = np.zeros(n)
    phis = np.zeros(n)
    
    # 创建插值函数
    alpha_interp = interp1d(S, alphaa, kind='cubic', bounds_error=False, fill_value="extrapolate")
    phi_interp = interp1d(S, phia, kind='cubic', bounds_error=False, fill_value="extrapolate")
    
    # 在整数深度插值
    S_interp = np.arange(1, n+1)
    
    for i in range(n):
        alphas[i] = abs(alpha_interp(i+1))
        phis[i] = abs(phi_interp(i+1))
    
    # 应用模
    for i in range(n):
        alphas[i] = alphas[i] % 360
        phis[i] = phis[i] % 360
    
    S = S_interp
    alpha = alphas
    phi = phis
    
    np_len = len(S)
    A = np.zeros((np_len, np_len))
    D1 = np.zeros(np_len)
    D2 = np.zeros(np_len)
    Ls = S[1:] - S[:-1]
    
    # 转换为弧度并翻转数组
    alpha = np.flip(alpha) * np.pi / 180
    phi = np.flip(phi) * np.pi / 180
    
    for i in range(1, np_len-1):
        Lk0 = Ls[i-1]
        Lk1 = Ls[i]
        alphak1 = alpha[i+1]
        alphak0 = alpha[i]
        alphak00 = alpha[i-1]
        phik1 = phi[i+1]
        phik0 = phi[i]
        phik00 = phi[i-1]
        
        D1[i] = 6 / (Lk0 + Lk1) * ((alphak1 - alphak0) / Lk1 - (alphak0 - alphak00) / Lk0)
        D2[i] = 6 / (Lk0 + Lk1) * ((phik1 - phik0) / Lk1 - (phik0 - phik00) / Lk0)
        lamk = Lk1 / (Lk0 + Lk1)
        miuk = 1 - lamk
        A[i, i-1:i+2] = [miuk, 2, lamk]
    
    # 求解三对角矩阵系统
    Mk = np.zeros(np_len)
    mk = np.zeros(np_len)
    
    # 先处理边界条件
    A_sub = A[1:-1, 1:-1]
    Mk[1:-1] = np.linalg.solve(A_sub, D1[1:-1])
    mk[1:-1] = np.linalg.solve(A_sub, D2[1:-1])
    
    Sk = S
    alphak = alpha
    phik = phi
    
    return Mk, mk, Sk, alphak, phik

def prepare_data(sspan, Mk, mk, Sk, alphak, phik):
    alphas = np.zeros(len(sspan))
    phis = np.zeros(len(sspan))
    taos = np.zeros(len(sspan))
    
    for i in range(len(sspan)):
        alphas[i], phis[i] = spline_interp(Mk, mk, Sk, alphak, phik, sspan[i])
    
    kphis = diff_func(phis, sspan)
    kalphas = diff_func(alphas, sspan)
    
    ks = np.sqrt(kalphas**2 + kphis**2 * np.sin(alphas)**2)
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
            alpha1 = alphas[i-1]
            alpha2 = alphas[i+1]
            phi1 = phis[i-1]
            phi2 = phis[i+1]
            ds = sspan[1] - sspan[0]
        
        dp = (phi2 - phi1) / 2
        da = (alpha2 - alpha1) / 2
        ac = (alpha1 + alpha2) / 2
        edl = np.sqrt(da**2 + dp**2 * (np.sin(ac))**2)
        
        if edl > 1e-10:
            try:
                trig_val = (da**2 / edl**2 * np.cos(dp) 
                           - da * dp / edl**2 * (np.sin(alpha2) * np.cos(alpha2) - np.sin(alpha1) * np.cos(alpha1)) * np.sin(dp)
                           + dp**2 / edl**2 * np.sin(alpha1) * np.sin(alpha2) * (np.sin(alpha1) * np.sin(alpha2) + np.cos(alpha1) * np.cos(alpha2) * np.cos(dp)))
                trig_val = max(-1.0, min(1.0, trig_val))  # 限制在 [-1, 1] 范围内
                theta = np.arccos(trig_val)
            except:
                theta = 0
        else:
            theta = 0
        
        theta = np.real(theta)
        taos[i] = theta / ds
    
    # 处理NaN值
    taos = np.nan_to_num(taos)
    
    return alphas, phis, ks, dks, ddks, kphis, kalphas, taos

def main():
    # 读取数据
    # guiji = np.loadtxt('KL16-1-A25井眼轨迹.xlsx', delimiter=',')
    # zuanju = np.loadtxt('钻具组合.xlsx', delimiter=',')

    guiji = pd.read_excel('KL16-1-A25井眼轨迹.xlsx', header=None)
    zuanju = pd.read_excel('钻具组合.xlsx', header=None)

    # Convert to NumPy arrays if necessary
    guiji = guiji.to_numpy()
    zuanju = zuanju.to_numpy()

    
    # 基本参数
    wc = 1  # 工况选择：1旋转钻进
    v = 0.00714  # 钻进速度，m/s
    omega = 5 * np.pi / 3  # 转速，rad/s
    T0 = 58900  # 钻压，N
    rhoi = 1170  # 钻井液密度，kg/m3
    Dw = 0.2159  # 井眼直径，m
    tgxs = 3500  # 套管下深，m
    miua11 = 0.15  # 套管段摩阻系数
    miua22 = 0.20  # 裸眼段摩阻系数
    js = 4200  # 计算井深，m
    
    # 调用主函数
    T, M = mainfunc(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, js, v, omega)
    
    return T, M
