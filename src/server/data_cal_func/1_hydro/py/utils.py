import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline


def deal_curve_data2(data1):
    # ȥ�����۹켣�е��ظ�ֵ��������������
    sortedData = data1[np.argsort(np.round(data1[:, 0]))]  # ����һ����������
    _, uniqueIndices = np.unique(sortedData[:, 0], return_index=True)  # ��ȡ��һ�е�Ψһ����
    data = sortedData[np.sort(uniqueIndices)]  # ͨ��������ȡΨһ��������

    # ��ȡ����
    S = np.round(data[:, 0]).astype(int).reshape(-1, 1)
    alphaa = data[:, 1].reshape(-1, 1)
    phia = data[:, 2].reshape(-1, 1)
    n = int(S[-1, 0])

    # ���� Cubic Spline ��ֵ
    i_values = np.arange(1, n + 1).reshape(-1, 1)  # ���� 1 �� n ��������
    spline_alpha = CubicSpline(S.flatten(), alphaa.flatten())  # 'spline' ��ֵ
    spline_phi = CubicSpline(S.flatten(), phia.flatten())  # 'spline' ��ֵ
    alphas = np.abs(spline_alpha(i_values)).reshape(-1, 1)  # ȡ����ֵ
    phis = np.abs(spline_phi(i_values)).reshape(-1, 1)  # ȡ����ֵ

    # ȡģ 360
    alphas = np.mod(alphas, 360)
    phis = np.mod(phis, 360)

    # ���¶��� S
    S = np.arange(1, n + 1).reshape(-1, 1)
    alpha = np.flipud(alphas) * np.pi / 180  # ��ת��ת��Ϊ����
    phi = np.flipud(phis) * np.pi / 180  # ��ת��ת��Ϊ����

    # ��ʼ������
    np_count = S.shape[0]  # ����
    A = np.zeros((np_count, np_count))
    D1 = np.zeros((np_count, 1))
    D2 = np.zeros((np_count, 1))

    # ���㲽�� Ls
    Ls = S[1:] - S[:-1]

    # ������� A ������ D1, D2
    for i in range(1, np_count - 1):
        Lk0 = Ls[i - 1, 0]
        Lk1 = Ls[i, 0]
        alphak1 = alpha[i + 1, 0]
        alphak0 = alpha[i, 0]
        alphak00 = alpha[i - 1, 0]
        phik1 = phi[i + 1, 0]
        phik0 = phi[i, 0]
        phik00 = phi[i - 1, 0]

        D1[i, 0] = 6 / (Lk0 + Lk1) * ((alphak1 - alphak0) / Lk1 - (alphak0 - alphak00) / Lk0)
        D2[i, 0] = 6 / (Lk0 + Lk1) * ((phik1 - phik0) / Lk1 - (phik0 - phik00) / Lk0)

        lamk = Lk1 / (Lk0 + Lk1)
        miuk = 1 - lamk
        A[i, i - 1: i + 2] = [miuk, 2, lamk]

    # ���� Mk, mk
    Mk = np.zeros((np_count, 1))
    mk = np.zeros((np_count, 1))
    A_sub = A[1:-1, 1:-1]
    Mk[1:-1] = np.linalg.solve(A_sub, D1[1:-1])
    mk[1:-1] = np.linalg.solve(A_sub, D2[1:-1])

    # ������
    Sk = S
    alphak = alpha
    phik = phi

    return Mk, mk, Sk, alphak, phik



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

    # �任�ɴӾ��׵����ڵ�����
    Length = data[-1, 0] - Length
    Xs0 = Xs[-1] - Xs
    Ys0 = Ys[-1] - Ys
    Zs0 = Zs[-1] - Zs

    # ͬǰ�� xyz ����ϵ���屣��һ��
    Xs = Zs0
    Ys = Xs0
    Zs = Ys0

    return Length, Xs, Ys, Zs


def diff_func(vars, span):
    vars = np.asarray(vars).flatten()  # ȷ�� vars �� 1D ����
    span = np.asarray(span).flatten()

    diff_var1 = np.zeros_like(vars)

    # ������ֵ����
    for i in range(len(vars)):
        if i == 0:  # ǰ����
            diff_var1[i] = (vars[i + 1] - vars[i]) / (span[i + 1] - span[i])
        elif i == len(vars) - 1:  # ������
            diff_var1[i] = (vars[-1] - vars[-2]) / (span[-1] - span[-2])
        else:  # ���Ĳ��
            diff_var1[i] = (vars[i + 1] - vars[i - 1]) / (span[i + 1] - span[i - 1])

    # ƽ�������ȼ��� MATLAB �� smooth��
    diff_var = savgol_filter(diff_var1, window_length=101, polyorder=3, mode='nearest')  # 101 �Ǵ��ڴ�С���ɵ���

    return diff_var

def prepare_data():

    return 1

def deal_trank(Sk,alpha,phi):

    return Length,Xs,Ys,Zs

    
    
    
