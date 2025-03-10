import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline

from scipy.interpolate import interp1d
from scipy.linalg import solve

def deal_curve_data2(data1):
    # 去除重复值并按升序排序
    data1_rounded = np.round(data1).astype(int)
    sorted_indices = np.argsort(data1_rounded[:, 0])
    sorted_data = data1_rounded[sorted_indices]
    # 获取唯一行（保持顺序）
    _, unique_indices = np.unique(sorted_data[:, 0], return_index=True)
    unique_indices = np.sort(unique_indices)  # 保持原始顺序
    data = sorted_data[unique_indices]
    
    # 提取并处理数据
    S = data[:, 0].astype(int)
    alphaa = data[:, 1]
    phia = data[:, 2]  # 注意：原MATLAB代码中是第三列，索引为2（Python从0开始）
    
    n = int(np.round(S[-1]))
    alphas = np.zeros(n)
    phis = np.zeros(n)
    
    # 创建插值函数（使用三次样条）
    if len(S) > 3:
        interp_kind = 'cubic'
    else:
        interp_kind = 'linear'  # 数据点少于3时使用线性插值
        
    alpha_interp = interp1d(S, alphaa, kind=interp_kind, fill_value='extrapolate')
    phi_interp = interp1d(S, phia, kind=interp_kind, fill_value='extrapolate')
    
    for i in range(n):
        alphas[i] = np.abs(alpha_interp(i+1))  # MATLAB的S从1开始
        phis[i] = np.abs(phi_interp(i+1))
    
    # 取模360度
    alphas = np.mod(alphas, 360)
    phis = np.mod(phis, 360)
    
    # 转换为弧度并翻转
    S = np.arange(1, n+1)
    alpha = np.flipud(alphas) * np.pi / 180
    phi = np.flipud(phis) * np.pi / 180
    np_ = len(S)
    
    # 初始化矩阵和向量
    A = np.zeros((np_, np_))
    D1 = np.zeros(np_)
    D2 = np.zeros(np_)
    Ls = np.diff(S)
    
    # 构建三对角矩阵
    for i in range(1, np_-1):
        Lk0 = Ls[i-1]
        Lk1 = Ls[i]
        
        alphak1 = alpha[i+1]
        alphak0 = alpha[i]
        alphak00 = alpha[i-1]
        
        phik1 = phi[i+1]
        phik0 = phi[i]
        phik00 = phi[i-1]
        
        # 计算D向量
        D1[i] = 6 / (Lk0 + Lk1) * ((alphak1 - alphak0)/Lk1 - (alphak0 - alphak00)/Lk0)
        D2[i] = 6 / (Lk0 + Lk1) * ((phik1 - phik0)/Lk1 - (phik0 - phik00)/Lk0)
        
        # 填充矩阵A
        lamk = Lk1 / (Lk0 + Lk1)
        miuk = 1 - lamk
        A[i, i-1] = miuk
        A[i, i] = 2
        A[i, i+1] = lamk
    
    # 求解方程组
    Mk = np.zeros(np_)
    mk = np.zeros(np_)
    if np_ > 2:
        # 提取中间方程组
        A_sub = A[1:-1, 1:-1]
        D1_sub = D1[1:-1]
        D2_sub = D2[1:-1]
        
        Mk[1:-1] = solve(A_sub, D1_sub)
        mk[1:-1] = solve(A_sub, D2_sub)
    
    return Mk, mk, S, alpha, phi



def deal_input_data(data):
    Xs = np.zeros((data.shape[0], 1))
    Ys = np.zeros((data.shape[0], 1))
    Zs = np.zeros((data.shape[0], 1))
    Length = np.zeros((data.shape[0], 1))
    Length = data[:, 0].reshape(-1, 1)

    for i in range(1, len(Xs)):
        alpha1 = data[i - 1, 1] / 180 * np.pi
        alpha2 = data[i, 1] / 180 * np.pi
        phi1 = data[i - 1, 2] / 180 * np.pi
        phi2 = data[i, 2] / 180 * np.pi
        ppp = abs(phi1 - phi2)
        if ppp > np.pi and phi1 < np.pi:
            phi1 = phi1 + 2 * np.pi
        elif ppp > np.pi and phi1 > np.pi:
            phi1 = phi1 - 2 * np.pi

        ds = data[i, 0] - data[i - 1, 0]
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

        Xs[i] = Xs[i - 1] + dx
        Ys[i] = Ys[i - 1] + dy
        Zs[i] = Zs[i - 1] + dz

    # 变换成从井底到井口的数据
    Length = data[-1, 0] - Length
    Xs0 = Xs[-1] - Xs
    Ys0 = Ys[-1] - Ys
    Zs0 = Zs[-1] - Zs

    # 同前期 xyz 坐标系定义保持一致
    Xs = Zs0
    Ys = Xs0
    Zs = Ys0

    return Length, Xs, Ys, Zs


def diff_func(vars, span):
    # TODO: 这里需要确保是1D数组吗
    vars = np.asarray(vars).flatten()  # 确保 vars 是 1D 数组
    span = np.asarray(span).flatten()

    diff_var1 = np.zeros_like(vars)

    # 计算数值导数
    for i in range(len(vars)):
        if i == 0:  # 前向差分
            diff_var1[i] = (vars[i + 1] - vars[i]) / (span[i + 1] - span[i])
        elif i == len(vars) - 1:  # 后向差分
            diff_var1[i] = (vars[-1] - vars[-2]) / (span[-1] - span[-2])
        else:  # 中心差分
            diff_var1[i] = (vars[i + 1] - vars[i - 1]) / (span[i + 1] - span[i - 1])

    # 平滑处理（等价于 MATLAB 的 smooth）
    diff_var = savgol_filter(diff_var1, window_length=101, polyorder=3, mode='nearest')  # 101 是窗口大小，可调整

    return diff_var

# gpt
def spline_interp(Mk,mk,Sk,alphak,phik,S0):
    np_val = len(Mk)
    
    if S0 >= Sk[-1]:
        iter = np_val - 1
    else:
        for i in range(np_val - 1):
            if Sk[i] <= S0 < Sk[i + 1]:
                iter = i
                break
    
    if S0 < min(Sk):
        iter = 0
    
    M0 = Mk[iter]
    M1 = Mk[iter + 1]
    m0 = mk[iter]
    m1 = mk[iter + 1]
    alpha0 = alphak[iter]
    alpha1 = alphak[iter + 1]
    phi0 = phik[iter]
    phi1 = phik[iter + 1]
    Sr = Sk[iter + 1]
    Sl = Sk[iter]
    Lk = Sk[iter + 1] - Sk[iter]
    
    C1 = alpha1 / Lk - M1 * Lk / 6
    C0 = alpha0 / Lk - M0 * Lk / 6
    c1 = phi1 / Lk - M1 * Lk / 6
    c0 = phi0 / Lk - M0 * Lk / 6
    
    alphacal = M0 * (Sr - S0)**3 / (6 * Lk) + M1 * (S0 - Sl)**3 / (6 * Lk) + C1 * (S0 - Sl) + C0 * (Sr - S0)
    phical = m0 * (Sr - S0)**3 / (6 * Lk) + m1 * (S0 - Sl)**3 / (6 * Lk) + c1 * (S0 - Sl) + c0 * (Sr - S0)
    
    return alphacal, phical


# gpt
def prepare_data(sspan,Mk,mk,Sk,alphak,phik):
    # 初始化输出变量
    alphas = np.zeros(len(sspan))
    phis = np.zeros(len(sspan))
    taos = np.zeros(len(sspan))

    # 插值计算 alphas 和 phis
    for i in range(len(sspan)):
        alphas[i], phis[i] = spline_interp(Mk, mk, Sk, alphak, phik, sspan[i])

    # 调用求导函数计算 kphis 和 kalphas
    kphis = diff_func(phis, sspan)
    kalphas = diff_func(alphas, sspan)

    # 计算 ks, dks, ddks
    ks = np.sqrt(kalphas**2 + kphis**2 * np.sin(alphas)**2)
    dks = diff_func(ks, sspan)
    ddks = diff_func(dks, sspan)

    # 计算 taos
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
        edl = np.sqrt(da**2 + dp**2 * np.sin(ac)**2)

        theta = np.arccos(
            da**2 / edl**2 * np.cos(dp) -
            da * dp / edl**2 * (np.sin(alpha2) * np.cos(alpha2) - np.sin(alpha1) * np.cos(alpha1)) * np.sin(dp) +
            dp**2 / edl**2 * np.sin(alpha1) * np.sin(alpha2) * (np.sin(alpha1) * np.sin(alpha2) + np.cos(alpha1) * np.cos(alpha2) * np.cos(dp))
        )
        theta = np.real(theta)
        taos[i] = theta / ds

    # 处理 taos 中的 NaN 值
    for i in range(len(sspan)):
        if np.isnan(taos[i]):
            taos[i] = 0

    return alphas, phis, ks, dks, ddks, kphis, kalphas, taos

def deal_trank(Sk, alpha, phi):
    #     data=xlsread(filename);
    n = len(Sk)  # n=numel(Sk);
    Xs = np.zeros(n)  # Xs=zeros(n,1);
    Ys = np.zeros(n)  # Ys=zeros(n,1);
    Zs = np.zeros(n)  # Zs=zeros(n,1);
    Length = np.zeros(n)  # Length=zeros(n,1);
    Length = np.array(Sk)  # Length=Sk(:,1);
  
    for i in range(1, len(Xs)):  # for i=2:length(Xs)
        alpha1 = alpha[i - 1]  # alpha1=alpha(i-1);
        alpha2 = alpha[i]      # alpha2=alpha(i);
        phi1 = phi[i - 1]      # phi1=phi(i-1);
        phi2 = phi[i]          # phi2=phi(i);
        #         ppp=abs(phi1-phi2);
        #         if ppp>pi&&phi1<pi
        #             phi1=phi1+2*pi;
        #         elseif ppp>pi&&phi1>pi
        #             phi1=abs(phi1-2*pi);
        #         end
        ds = Sk[i] - Sk[i - 1]  # ds=Sk(i)-Sk(i-1);
        if alpha1 != alpha2 and phi1 != phi2:  # if alpha1~=alpha2&&phi1~=phi2
            dx = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            dy = ds * (np.cos(alpha1) - np.cos(alpha2)) / (alpha2 - alpha1) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        elif alpha1 == alpha2 and phi1 != phi2:  # elseif alpha1==alpha2&&phi1~=phi2
            #             dx=ds*sin(alpha1)/(phi2-phi1)*(sin(phi2)-sin(phi1));
            dx = ds * np.sin(alpha2) / (phi2 - phi1) * (np.sin(phi2) - np.sin(phi1))
            #             dy=ds*sin(alpha1)/(phi2-phi1)*(cos(phi1)-cos(phi2));
            dy = ds * np.sin(alpha2) / (phi2 - phi1) * (np.cos(phi1) - np.cos(phi2))
            #             dz=ds*cos(alpha1);
            dz = ds * np.cos(alpha2)
        elif alpha1 != alpha2 and phi1 == phi2:  # elseif alpha1~=alpha2&&phi1==phi2
            #             dx=ds/(alpha2-alpha1)*(cos(alpha1)-cos(alpha2))*cos(phi1);
            dx = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.cos(phi2)
            #             dy=ds/(alpha2-alpha1)*(cos(alpha1)-cos(alpha2))*sin(phi1);
            dy = ds / (alpha2 - alpha1) * (np.cos(alpha1) - np.cos(alpha2)) * np.sin(phi2)
            dz = ds / (alpha2 - alpha1) * (np.sin(alpha2) - np.sin(alpha1))
        else:
            #             dx=ds*sin(alpha1)*cos(phi1);
            dx = ds * np.sin(alpha2) * np.cos(phi2)
            #             dy=ds*sin(alpha1)*sin(phi1);
            dy = ds * np.sin(alpha2) * np.sin(phi2)
            #             dz=ds*cos(alpha1);
            dz = ds * np.cos(alpha2)
        Xs[i] = Xs[i - 1] + dx  # Xs(i)=Xs(i-1)+dx;
        Ys[i] = Ys[i - 1] + dy  # Ys(i)=Ys(i-1)+dy;
        Zs[i] = Zs[i - 1] + dz  # Zs(i)=Zs(i-1)+dz;

    return Length, Xs, Ys, Zs

    
    
    
