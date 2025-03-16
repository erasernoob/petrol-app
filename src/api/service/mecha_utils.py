import numpy as np
from scipy.optimize import least_squares
from scipy.interpolate import interp1d
import pandas as pd
from scipy.interpolate import interp1d
from service import utils
from scipy.integrate import solve_ivp


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
