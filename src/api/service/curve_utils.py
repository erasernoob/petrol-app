import numpy as np
from scipy.ndimage import gaussian_filter1d
import pandas as pd
from scipy.ndimage import uniform_filter1d
from numpy.linalg import solve
from scipy.interpolate import interp1d, make_interp_spline
from scipy.ndimage import gaussian_filter1d
from service.utils import diff_func, spline_interp

def deal_trank(Sk, alpha, phi):
    """
    根据井眼轨迹数据 Sk, alpha, phi 计算三维坐标 Xs, Ys, Zs 以及长度数据 Length.

    输入：
        Sk    - 1D numpy 数组，采样点的参数（井眼轨迹长度），长度 n
        alpha - 1D numpy 数组，每个采样点的倾角（单位：弧度）
        phi   - 1D numpy 数组，每个采样点的方位角（单位：弧度）

    输出：
        Length - 1D numpy 数组，与 Sk 等长，这里直接赋值为 Sk
        Xs     - 1D numpy 数组，X 坐标
        Ys     - 1D numpy 数组，Y 坐标
        Zs     - 1D numpy 数组，Z 坐标
    """
    n = Sk.size  # 点的个数
    Xs = np.zeros(n)
    Ys = np.zeros(n)
    Zs = np.zeros(n)

    # 直接将 Length 赋值为 Sk（与 MATLAB 中 Length=Sk(:,1) 等效）
    Length = Sk.copy()

    # 从第二个点开始，根据前后两点的 alpha, phi 以及 ds (两点之间的间距) 进行积分计算坐标
    for i in range(1, n):
        alpha1 = alpha[i - 1]
        alpha2 = alpha[i]
        phi1 = phi[i - 1]
        phi2 = phi[i]
        ds = Sk[i] - Sk[i - 1]

        if (alpha1 != alpha2) and (phi1 != phi2):
            dx = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (
                        np.sin(phi2) - np.sin(phi1))
            dy = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (
                        np.cos(phi1) - np.cos(phi2))
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        elif (alpha1 == alpha2) and (phi1 != phi2):
            # 当倾角不变，方位角变化时
            dx = ds * np.sin(alpha2) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            dy = ds * np.sin(alpha2) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
            dz = ds * np.cos(alpha2)
        elif (alpha1 != alpha2) and (phi1 == phi2):
            # 当方位角不变，倾角变化时
            dx = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.cos(phi2)
            dy = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.sin(phi2)
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        else:
            # 当倾角和方位角均不变化时，直接沿当前方向前进
            dx = ds * np.sin(alpha2) * np.cos(phi2)
            dy = ds * np.sin(alpha2) * np.sin(phi2)
            dz = ds * np.cos(alpha2)

        Xs[i] = Xs[i - 1] + dx
        Ys[i] = Ys[i - 1] + dy
        Zs[i] = Zs[i - 1] + dz

    # 以下部分 MATLAB 中的注释代码为数据坐标转换，可根据需要进行调整（此处保持与原代码一致）
    # 例如：
    # Length = Sk[-1] - Length
    # Xs = Xs[::-1]
    # Ys = Ys[::-1]
    # Zs = Zs[-1] - Zs

    return Length, Xs, Ys, Zs


def prepare_data(sspan, Mk, mk, Sk, alphak, phik):
    """
    输入：
        sspan   - 采样点的自变量数组（1D numpy 数组）
        Mk, mk, Sk, alphak, phik - 与曲线相关的各项数据（均为 numpy 数组）
    输出：
        alphas, phis   - 通过样条插值得到的 alpha 和 phi 数组
        ks             - 曲率值数组（根据 kalphas, kphis 和 alphas 计算得到）
        dks, ddks      - ks 的一阶和二阶导数（由 diff_func 计算）
        kphis, kalphas - phis 和 alphas 对应的导数（由 diff_func 计算）
        taos           - 通过后处理计算得到的角变化率数组
    """
    n_span = sspan.size  # 采样点个数

    # 初始化 alphas, phis, taos 数组（均为列向量形式）
    alphas = np.zeros(n_span)
    phis   = np.zeros(n_span)
    taos   = np.zeros(n_span)

    # --- 1. 对每个 sspan 点，通过样条插值函数获得 alpha 和 phi ---
    for i in range(n_span):
        # 调用 spline_interp 进行插值，假设返回一个元组 (alpha, phi)
        alphas[i], phis[i] = spline_interp(Mk, mk, Sk, alphak, phik, sspan[i])

    # --- 2. 求导计算 ---
    # kphis: phis 关于 sspan 的一阶导数
    kphis   = diff_func(phis, sspan)
    # kalphas: alphas 关于 sspan 的一阶导数
    kalphas = diff_func(alphas, sspan)
    # 计算曲率 ks，注意 MATLAB 中公式：ks = sqrt(kalphas.^2 + kphis.^2.*sin(alphas).*sin(alphas))
    ks = np.sqrt(kalphas**2 + (kphis**2) * (np.sin(alphas)**2))
    # ks 的一阶与二阶导数
    dks  = diff_func(ks, sspan)
    ddks = diff_func(dks, sspan)

    # --- 3. 计算 taos (角变化率) ---
    # 对每个采样点，根据其相邻点信息计算
    for i in range(n_span):
        if i == 0:
            # MATLAB 中 i==1 对应 Python 索引 0
            alpha1 = alphas[0]
            alpha2 = alphas[1]
            phi1   = phis[0]
            phi2   = phis[1]
            ds     = sspan[1] - sspan[0]
        elif i == n_span - 1:
            # MATLAB 中 i==numel(sspan) 对应 Python 索引 n_span-1
            alpha1 = alphas[-2]
            alpha2 = alphas[-1]
            phi1   = phis[-2]
            phi2   = phis[-1]
            ds     = 2 * (sspan[1] - sspan[0])
        else:
            # 中间点
            alpha1 = alphas[i - 1]
            alpha2 = alphas[i + 1]
            phi1   = phis[i]
            phi2   = phis[i + 1]
            ds     = sspan[1] - sspan[0]

        # 调整 phi1 当 phi1 与 phi2 差值过大时（跨越 180° 的情况）
        ppp = abs(phi1 - phi2)
        if ppp > np.pi:
            if phi1 < np.pi:
                phi1 = phi1 + 2 * np.pi
            elif phi1 > np.pi:
                phi1 = phi1 - 2 * np.pi

        # 计算 dp, da, ac
        dp = (phi2 - phi1) / 2
        da = (alpha2 - alpha1) / 2
        ac = (alpha1 + alpha2) / 2
        # 计算 edl，注意 MATLAB 中 da^2 表示 da**2，在 Python 中使用 ** 表示乘方
        edl = np.sqrt(da**2 + dp**2 * (np.sin(ac)**2))

        # 计算 theta，根据给定公式
        # theta = acos( da^2/edl^2*cos(dp) - da*dp/edl^2*( sin(alpha2)*cos(alpha2)- sin(alpha1)*cos(alpha1) )* sin(dp)
        #               + dp^2/edl^2*sin(alpha1)*sin(alpha2)*( sin(alpha1)*sin(alpha2)+ cos(alpha1)*cos(alpha2)*cos(dp) ) )
        argument = (da**2 / edl**2) * np.cos(dp) \
                   - (da * dp / edl**2) * (np.sin(alpha2) * np.cos(alpha2) - np.sin(alpha1) * np.cos(alpha1)) * np.sin(dp) \
                   + (dp**2 / edl**2) * np.sin(alpha1) * np.sin(alpha2) * (np.sin(alpha1) * np.sin(alpha2) + np.cos(alpha1) * np.cos(alpha2) * np.cos(dp))
        # 防止由于数值误差导致 argument 超出 acos 定义域，进行夹紧处理
        argument = np.clip(argument, -1.0, 1.0)
        theta = np.arccos(argument)
        theta = np.real(theta)  # 保证 theta 为实数
        taos[i] = theta / ds

    # --- 4. 对 taos 中可能出现的 NaN 值进行处理，将 NaN 替换为 0 ---
    taos[np.isnan(taos)] = 0

    return alphas, phis, ks, dks, ddks, kphis, kalphas, taos

def deal_curve_data2(data1, js):
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


    window = 20
    sigma = window / 6.0  # MATLAB 的平滑窗长 20 对应的 sigma 估计值
    truncate_val = (window - 1) / (2.0 * sigma)  # 保证滤波器长度约为 window

    alphas = gaussian_filter1d(alphas, sigma=sigma, truncate=truncate_val)
    phis = gaussian_filter1d(phis, sigma=sigma, truncate=truncate_val)

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




def abcfunc4(guiji, Holedia, ml, zuanju, js):
    """
    参数：
      guiji: 井眼轨迹数据（二维 NumPy 数组）
      Holedia: 井筒直径（m）
      ml: 钻柱弹性模量（MPa）
      zuanju: 钻具组合数据（二维 NumPy 数组）
      js: 计算井深（m）

    返回：
      FH: 螺旋屈曲临界载荷（N）的数组
      FS: 正弦屈曲临界载荷（N）的数组
    """
    # 井眼轨迹数据
    data = guiji  # MATLAB 中的 data=guiji
    Dw = Holedia  # 井筒直径
    miut = 0.17
    miua = miut
    E = ml * 1000000  # 弹性模量，单位：Pa

    # 钻具长度确定：取 zuanju 第4行（Python索引为 3），除最后一列外的数据
    row_data = zuanju[3, :-1]
    row_sum = np.sum(row_data)
    # 更新 zuanju 第4行最后一个元素
    zuanju[3, -1] = js - row_sum

    # 钻柱参数（MATLAB 中的 Dtrans、dtrans、mtrans、ltrans）
    Dtrans = zuanju[0, :]  # 钻柱外径，m
    dtrans = zuanju[1, :]  # 钻柱内径，m
    mtrans = 9.81 * 2.5 * zuanju[2, :]  # 钻柱组合线重，N/m
    ltrans = zuanju[3, :]  # 钻柱长度

    # 计算第一个钻柱的极惯性矩
    I = np.pi * (Dtrans[0] ** 4 - dtrans[0] ** 4) / 64
    g = 9.81  # 重力加速度

    # 钻具组合参数
    Ntrans = Dtrans.size  # 钻具组合数量
    nntrans = np.zeros(Ntrans)
    # 总钻具长度（假设 ltrans 中的各段长度均为整数或可转换为整数）
    ntrans = int(np.sum(ltrans))

    # 初始化各段参数，长度均为 ntrans
    Rt = np.zeros(ntrans)  # 各段钻具组合外半径，m
    rt = np.zeros(ntrans)  # 各段钻具组合内半径，m
    Aot = np.zeros(ntrans)  # 各段钻具组合外截面积，m^2
    Ait = np.zeros(ntrans)  # 各段钻具组合内截面积，m^2
    qt = np.zeros(ntrans)  # 各段钻具组合线重，N/m
    It = np.zeros(ntrans)  # 惯性矩
    ht = np.zeros(ntrans)  # 壁厚
    Pi = np.zeros(ntrans)  # 环空流体压力，MPa
    PI1 = Pi.copy()
    PI2 = Pi.copy()
    Tc = PI1.copy()
    Po = np.zeros(ntrans)  # 管内流体压力，MPa
    PO1 = Po.copy()
    PO2 = Pi.copy()
    FH = np.zeros(ntrans)  # 螺旋屈曲临界载荷，N
    FS = np.zeros(ntrans)  # 正弦屈曲临界载荷，N

    # 计算 nntrans：各钻柱段长度的累加
    nntrans[0] = ltrans[0]
    for i in range(1, Ntrans):
        nntrans[i] = nntrans[i - 1] + ltrans[i]

    # 计算钻具组合各分段的半径、截面积、线重
    for i in range(Ntrans):
        if i == 0:
            # MATLAB: for j = 1:nntrans(1)
            for j in range(int(nntrans[0])):  # Python 索引 0 到 nntrans[0]-1
                Rt[j] = Dtrans[0] / 2.0
                rt[j] = dtrans[0] / 2.0
                Aot[j] = np.pi * Rt[j] ** 2
                Ait[j] = np.pi * rt[j] ** 2
                qt[j] = mtrans[0]
                # qmt 与 Kft 的计算在原代码中被注释
                It[j] = np.pi * (Rt[j] ** 4 - rt[j] ** 4) / 4.0
                ht[j] = Rt[j] - rt[j]
        else:
            # MATLAB: for j = nntrans(i-1)+1 : nntrans(i)
            # 对应 Python 中 j 从 nntrans[i-1] 到 nntrans[i]-1
            for j in range(int(nntrans[i - 1]), int(nntrans[i])):
                Rt[j] = Dtrans[i] / 2.0
                rt[j] = dtrans[i] / 2.0
                Aot[j] = np.pi * Rt[j] ** 2
                Ait[j] = np.pi * rt[j] ** 2
                qt[j] = mtrans[i]
                # qmt 与 Kft 同上，保持注释
                It[j] = np.pi * (Rt[j] ** 4 - rt[j] ** 4) / 4.0
                ht[j] = Rt[j] - rt[j]


    # 初始化其他变量
    sign1 = 1
    T0 = 0
    M0 = 0
    sign2 = 0

    # T0 取负
    T0 = -T0

    # 计算参数
    Dw = Dw + 0.001
    ds = 1  # 步长
    L = ntrans - 1  # 计算长度（避免使用内置变量 len）
    nt = L / ds
    sspan = np.arange(0, L + ds, ds)  # 包含 L 的数组
    SW = sspan.reshape(-1, 1)  # 转换为列向量

    # 调用处理井眼轨迹的函数
    Mk, mk, Sk, alphak, phik = deal_curve_data2(data, js)

    # 初始化 k、tao 等参数
    alpha, phi, ks, dks, ddks, kphis, kalphas, taos = prepare_data(sspan, Mk, mk, Sk, alphak, phik)

    # 初始化 DAL 数组（此处用 1D 数组，如果需要列向量可以 reshape(-1, 1)）
    DAL = np.zeros(ntrans)
    # 翻转后的 alpha 值，转换为角度（单位：°）
    # ALpha = (alpha * 180 / np.pi)[::-1]
    # ALpha = np.flip(alpha * 180 / np.pi)
    ALpha = np.flipud(alpha * 180 / np.pi)

    # 计算 DAL 数组：对每相邻两个点计算角度差的绝对值，并乘以 30 再乘以 10
    for i in range(ntrans - 1):
        DAL[i] = abs((ALpha[i + 1] - ALpha[i]) * 30) * 10

    # 调用 deal_trank 函数，输出自然长度以及各点坐标
    Length, Ys, Zs, Xs = deal_trank(Sk, alpha, phi)  # Ys, Zs, Xs 均为形状为 (ntrans, ?) 的 numpy 数组

    # 构建 mmm 数组（用于存放井眼坐标差值），形状为 (ntrans, 3)
    mmm = np.zeros((ntrans, 3))
    # MATLAB 中 iiii=numel(mmm(:,3))，由于 mmm[:,2] 长度为 ntrans，所以 iiii = ntrans
    iiiii = ntrans

    # 注意 MATLAB 为 1-indexed，Python 为 0-indexed，因此取最后一行使用索引 iiii-1
    # 这里假设 Xs, Ys, Zs 至少有一列，且取第一列数据
    mmm[:, 2] = Xs[iiiii - 1] - Xs[0]  # 第三列：X 坐标差值
    mmm[:, 0] = Ys[iiiii - 1] - Ys[0]  # 第一列：北坐标差值（Y 坐标）
    mmm[:, 1] = Zs[iiiii - 1] - Zs[0]  # 第二列：东坐标差值（Z 坐标）

    # ---------------------------
     # 计算 B、B1、Z（注意数组索引：Python 中前500个元素为 smalpha[:500]，
    # MATLAB 中 smalpha(1:500) 对应 Python 的 smalpha[0:500]）

    # 假设 alpha 是一个 NumPy 数组
    window = 201
    smalpha = uniform_filter1d(alpha, size=window)


    B = np.mean(smalpha[:500])
    B1 = np.mean(smalpha[:300])
    # MATLAB 中 smalpha(end-300:end) 对应 Python 的 smalpha[-301:]
    Z = np.mean(smalpha[-301:])

    # 初始化 Ls, Lc, Lh
    Ls = 0
    Lc = 0
    Lh = 0

    if B < 0.44:
        Ls = ntrans
    else:
        # 初始化用于存储 ca 值（可选）
        ca = []
        # MATLAB for i=1:ntrans-1，对应 Python 的 range(1, ntrans)
        for i in range(1, ntrans):
            # 对应 MATLAB 中 smalpha(end-i+1) 转换为 Python 的 smalpha[-i]
            ca_val = abs(smalpha[-i] - Z)
            ca.append(ca_val)
            Ls = i + 1  # 垂直井段：MATLAB 中 Ls=i+1
            if ca_val > 0.11 and smalpha[-i] > 0.25:
                break

    # 识别水平井段
    # 判断25°到70°定向井的情况
    if B1 > 0.44 and B < 1.23:
        ba = []  # 用于存储 ba 值（可选）
        for i in range(1, ntrans):
            # 若垂直井段已占满，则退出循环
            if Ls == ntrans:
                break
            else:
                # MATLAB 中 for i=1:ntrans-1，索引转换为 Python 的 smalpha[i-1]
                ba_val = abs(smalpha[i - 1] - B1)
                ba.append(ba_val)
                Lh = i  # 水平井段：MATLAB 中 Lh=i
                if ba_val > 0.11 and smalpha[i - 1] < 0.44:
                    break
    else:
        # 其它情况
        ba = []  # 用于存储 ba 值（可选）
        for i in range(1, ntrans):
            if Ls == ntrans:
                break
            else:
                ba_val = abs(smalpha[i - 1] - B)
                ba.append(ba_val)
                Lh = i
                if ba_val > 0.11 and smalpha[i - 1] < 1.35:
                    break

    # 计算斜段长度（造斜段）
    Lc = ntrans - Lh - Ls

    # 计算 R 和 RR 数组
    R = 1.0 / ks  # MATLAB 中 R=1./ks
    RR = R ** 2  # MATLAB 中 RR=R.^2

    # 预分配 FH 和 FS 数组
    FH = np.zeros(ntrans)
    FS = np.zeros(ntrans)

    # 遍历每个截面，计算各段的力
    for i in range(ntrans):
        if i < Lh:  # MATLAB 中条件 if i < Lh+1，对应 Python 0 ~ Lh-1
            FH[i] = -2 * (2 * (2 ** 0.5) - 1) * np.sqrt(E * It[i] * qt[i] * np.sin(alpha[i]) / (0.5 * Dw - Rt[i]))
            FS[i] = -2 * np.sqrt(E * It[i] * qt[i] * np.sin(alpha[i]) / (0.5 * Dw - Rt[i]))
        elif i < Lh + Lc:  # MATLAB 中条件 elseif i < Lh+1+Lc，对应 Python Lh ~ Lh+Lc-1
            FH[i] = -7.56 * E * It[i] / (Rt[i] * (0.5 * Dw - Rt[i])) / 1000
            FS[i] = -4 * E * It[i] / (Rt[i] * (0.5 * Dw - Rt[i])) / 1000
        else:  # 其余部分，即垂直部分
            FH[i] = -5.55 * (E * It[i] * (qt[i] ** 2)) ** (1 / 3)
            FS[i] = -2.55 * (E * It[i] * (qt[i] ** 2)) ** (1 / 3)

    # 翻转数组顺序，并缩放1/1000
    fh = np.flipud(FH) / 1000
    fs = np.flipud(FS) / 1000
    return fh, fs






