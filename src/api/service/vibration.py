import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from pathlib import Path
import os

class StickSlipModel:
    def __init__(self):
        # 全局参数
        self.wob = 100            # 钻压，kN
        self.WOB = None           # 钻压，N
        self.v = None             # 转速，rad/s
        self.V = 90               # 转速，RPM
        self.Lp = 5765.26         # 钻杆长度，m
        self.Lpw = 47.26          # 加重钻杆长度，m
        self.Lc = 6.89            # 钻铤长度，m
        self.Lb = 0.24            # 钻头长度，m
        self.p1 = 8629            # 钻杆密度，kg/m3
        self.p2 = 8518            # 钻铤密度，kg/m3
        self.p3 = 9058            # 加重钻杆密度，kg/m3
        self.Dp = 0.127           # 钻杆外径，m
        self.Dpw = 0.127          # 加重钻杆外径，m
        self.Dc = 0.1715          # 钻铤外径，m
        self.dp = 0.1086          # 钻杆内径，m
        self.dpw = 0.0762         # 钻铤内径，m
        self.dc = 0.0572          # 加重钻杆内径，m
        self.Db = 0.2159          # 钻头直径，m
        self.Rb = None            # 钻头半径，m
        self.dl = 500             # 质量块长度，m
        self.np = None            # 钻杆质量块个数
        self.npw = None           # 加重钻杆质量块个数
        self.nc = None            # 钻铤质量块个数
        self.Lv = 3306            # 垂直段长度，m
        self.nv = None            # 垂直段质量块个数
        self.n = None             # 总质量块个数
        self.Jp = None            # 钻杆转动惯量
        self.Jpw = None           # 加重钻杆转动惯量
        self.Jc = None            # 钻铤转动惯量
        self.Jb = 471             # 钻头转动惯量
        self.Kp = None            # 钻杆刚度
        self.Kpw = None           # 加重钻杆刚度
        self.Kpc = None           # 钻铤刚度
        self.Kcb = 907            # 钻头刚度
        self.Cp = 140             # 钻杆阻尼
        self.Cpw = 80             # 加重钻杆阻尼
        self.Cpc = 190            # 钻铤阻尼
        self.Ccb = 181            # 钻头阻尼
        self.Cb = None            # 钻头与岩石阻尼
        self.miusb = 0.8          # 静摩擦系数
        self.miucb = 0.5          # 动摩擦系数
        self.Dv = 0.000001        # 最小滑动转速
        self.gamab = 0.9          # 摩擦扭矩下降率
        self.uf = 67              # 钻井液塑性粘度 mPa.s
        self.miuS = 0.8           # 接触面积修正系数
        self.Sp = None            # 钻杆接触面积
        self.Spw = None           # 加重钻杆接触面积
        self.Sc = None            # 钻铤接触面积
        self.Sb = None            # 钻头接触面积
        self.Dwell = None         # 井眼直径
        self.Dlp = None           # 钻杆与井壁的泥浆厚度
        self.Dlpw = None          # 加重钻杆与井壁的泥浆厚度
        self.Dlc = None           # 钻铤与井壁的泥浆厚度
        self.Dlb = None           # 钻头与井壁的泥浆厚度
        self.sita3 = 7            # 旋转粘度计读数（3转）
        self.sita100 = 41         # 旋转粘度计读数（100转）
        self.sita200 = 69         # 旋转粘度计读数（200转）
        self.sigma = None         # 赫巴屈服应力
        self.k = None             # 稠度系数
        self.nl = None            # 流度指数
        
        # 计算参数
        self.TIME = 50            # 计算时长，s
        self.Dt = 0.01            # 时间步长，s

    def initialize_parameters(self):
        # 自动计算参数
        self.WOB = self.wob * 1000
        self.v = (self.V) / 60 * 2 * np.pi  # 转速 rad/s
        self.welldepth = self.Lp + self.Lpw + self.Lc + self.Lb  # 井深
        self.Rb = self.Db / 2  # 钻头半径

        self.np = int(np.ceil(self.Lp / self.dl))    # 钻杆质量块个数
        self.npw = int(np.ceil(self.Lpw / self.dl))  # 加重钻杆质量块个数
        self.nc = int(np.ceil(self.Lc / self.dl))    # 钻铤质量块个数
        self.nv = int(np.ceil(self.Lv / self.dl))    # 垂直段质量块个数
        self.n = 1 + self.np + self.npw + self.nc

        self.Jp = 54 * self.p1 * np.pi * (self.dl) * (self.Dp**4 - self.dp**4) / 32  # 转动惯量
        self.Jpw = 100 * self.p3 * np.pi * (self.Lpw) * (self.Dpw**4 - self.dpw**4) / 32
        self.Jc = 150 * self.p2 * np.pi * (self.Lc) * (self.Dc**4 - self.dc**4) / 32

        E = 210e9  # 钻柱弹性模量
        nu = 0.3   # 钻柱泊松比
        G = E / 2 / (1 + nu)  # 钻柱剪切模量

        self.Kp = 0.36 * np.pi * G * (self.Dp**4 - self.dp**4) / (32 * self.dl)  # 刚度
        self.Kpw = 0.0079 * np.pi * G * (self.Dpw**4 - self.dpw**4) / (32 * self.Lpw)
        self.Kpc = 0.00109 * np.pi * G * (self.Dc**4 - self.dc**4) / (32 * self.Lc)

        self.Cb = 0.7 * np.pi * self.uf * self.Lc * self.Dc**3 * 0.5 / (self.Db - self.Dc)  # 钻头与岩石阻尼

        self.Sp = self.miuS * np.pi * self.Dp * self.dl    # 接触面积
        self.Sc = self.miuS * np.pi * self.Dc * self.Lc
        self.Spw = self.miuS * np.pi * self.Dpw * self.Lpw
        self.Sb = self.miuS * np.pi * self.Db * self.Lb

        self.Dwell = self.Db  # 井眼直径
        self.Dlp = (self.Dwell - self.Dp) / 2  # 各段泥浆厚度
        self.Dlpw = (self.Dwell - self.Dpw) / 2
        self.Dlc = (self.Dwell - self.Dc) / 2
        self.Dlb = (self.Dwell - 0.7 * self.Db) / 2

        self.sigma = 0.511 * self.sita3  # 赫巴屈服应力
        self.nl = 3.26 * np.log10((self.sita200 - self.sita3) / (self.sita100 - self.sita3))  # 流度指数
        self.k = 0.511 * (self.sita100 - self.sita3) / (170.2**self.nl)  # 稠度系数

    def odefunc(self, t, y):
        """微分方程求解函数"""
        n = self.n
        dydt = np.zeros(2*n)
        
        # 分离角位移和角速度
        x = y[:n]
        d = y[n:2*n]
        
        # 钻头与岩石互作用以及钻井液阻尼
        Tab = self.Cb * d[n-1]
        Tr = (self.Ccb) * (d[n-2] - d[n-1]) + self.Kcb * (x[n-2] - x[n-1]) - Tab
        Tsb = self.WOB * self.Rb * self.miusb
        miub = self.miucb + (self.miusb - self.miucb) * np.exp(-self.gamab * abs(d[n-1]))
        
        if abs(d[n-1]) < self.Dv and abs(Tr) < Tsb:
            Tfb = Tr
            Clb = 0
        elif abs(d[n-1]) < self.Dv and abs(Tr) >= Tsb:
            Tfb = Tsb * np.sign(Tr)
            Clb = 0
        else:
            Tfb = self.WOB * self.Rb * miub * np.sign(d[n-1])
            Clb = self.Sb * (self.sigma / (abs(d[n-1]) * self.Db / 2) + 
                           self.k * (((abs(d[n-1]) * self.Db / 2)**(self.nl-1)) / self.Dlb**self.nl))
        
        Clbb = np.real(Clb) * d[n-1]
        
        # 角位移的导数就是角速度
        dydt[:n] = d
        
        # 动力学方程
        # 第一个节点（井口）
        dydt[n] = (-self.Kp * (x[0] - self.v * t) - (self.Cp) * (d[0] - self.v) - 
                 self.Kp * (x[0] - x[1]) - (self.Cp) * (d[0] - d[1]) - 
                 (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jp
        
        # 垂直段除了第一个节点外的节点
        for i in range(1, self.nv-1):
            dydt[n+i] = (-self.Kp * (x[i] - x[i-1]) - (self.Cp) * (d[i] - d[i-1]) - 
                        self.Kp * (x[i] - x[i+1]) - (self.Cp) * (d[i] - d[i+1]) - 
                        (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jp
        
        # 垂直段的最后一个节点
        if self.nv > 1:
            dydt[n+self.nv-1] = (-self.Kp * (x[self.nv-1] - x[self.nv-2]) - (self.Cp) * (d[self.nv-1] - d[self.nv-2]) - 
                              self.Kp * (x[self.nv-1] - x[self.nv]) - (self.Cp) * (d[self.nv-1] - d[self.nv]) - 
                              np.real(Tfb) - (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jp
        
        # 钻杆段除了垂直段的节点
        for i in range(self.nv, self.np-1):
            dydt[n+i] = (-self.Kp * (x[i] - x[i-1]) - (self.Cp) * (d[i] - d[i-1]) - 
                        self.Kp * (x[i] - x[i+1]) - (self.Cp) * (d[i] - d[i+1]) - 
                        (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jp
        
        # 钻杆段的最后一个节点
        if self.np > 0:
            dydt[n+self.np-1] = (-self.Kp * (x[self.np-1] - x[self.np-2]) - (self.Cp) * (d[self.np-1] - d[self.np-2]) - 
                              self.Kpw * (x[self.np-1] - x[self.np]) - (self.Cpw) * (d[self.np-1] - d[self.np]) - 
                              np.real(Tfb) - (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jp
        
        # 加重钻杆段的节点
        if self.npw < 2 and self.npw > 0:
            dydt[n+self.np] = (-self.Kpw * (x[self.np] - x[self.np-1]) - (self.Cpw) * (d[self.np] - d[self.np-1]) - 
                              self.Kpc * (x[self.np] - x[self.np+1]) - (self.Cpc) * (d[self.np] - d[self.np+1]) - 
                              (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jpw
        elif self.npw > 1:
            for i in range(self.np, self.np+self.npw-1):
                dydt[n+i] = (-self.Kpw * (x[i] - x[i-1]) - (self.Cpw) * (d[i] - d[i-1]) - 
                            self.Kpw * (x[i] - x[i+1]) - (self.Cpw) * (d[i] - d[i+1]) - 
                            (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jpw
        
        # 加重钻杆段的最后一个节点
        if self.npw > 0:
            dydt[n+self.np+self.npw-1] = (-self.Kpw * (x[self.np+self.npw-1] - x[self.np+self.npw-2]) - 
                                       (self.Cpw) * (d[self.np+self.npw-1] - d[self.np+self.npw-2]) - 
                                       self.Kpc * (x[self.np+self.npw-1] - x[self.np+self.npw]) - 
                                       (self.Cpc) * (d[self.np+self.npw-1] - d[self.np+self.npw]) - 
                                       np.real(Tfb) - (self.Spw / self.Sb) * (np.real(Clbb))) / self.Jpw
        
        # 钻铤段的节点
        if self.nc < 2 and self.nc > 0:
            dydt[n+self.np+self.npw] = (-self.Kpc * (x[self.np+self.npw] - x[self.np+self.npw-1]) - 
                                     (self.Cpc) * (d[self.np+self.npw] - d[self.np+self.npw-1]) - 
                                     self.Kcb * (x[self.np+self.npw] - x[self.np+self.npw+1]) - 
                                     (self.Ccb) * (d[self.np+self.npw] - d[self.np+self.npw+1]) - 
                                     np.real(Tfb) - (self.Sc / self.Sb) * (np.real(Clbb))) / self.Jc
        elif self.nc > 1:
            for i in range(self.np+self.npw, self.np+self.npw+self.nc-1):
                dydt[n+i] = (-self.Kpc * (x[i] - x[i-1]) - (self.Cpc) * (d[i] - d[i-1]) - 
                            self.Kpc * (x[i] - x[i+1]) - (self.Cpc) * (d[i] - d[i+1]) - 
                            np.real(Tfb) - (self.Sc / self.Sb) * (np.real(Clbb))) / self.Jc
        
        # 钻铤段的最后一个节点
        if self.nc > 0:
            dydt[n+self.np+self.npw+self.nc-1] = (-self.Kpc * (x[self.np+self.npw+self.nc-1] - x[self.np+self.npw+self.nc-2]) - 
                                              (self.Cpc) * (d[self.np+self.npw+self.nc-1] - d[self.np+self.npw+self.nc-2]) - 
                                              self.Kcb * (x[self.np+self.npw+self.nc-1] - x[self.n-1]) - 
                                              (self.Ccb) * (d[self.np+self.npw+self.nc-1] - d[self.n-1]) - 
                                              np.real(Tfb) - (self.Sc / self.Sb) * (np.real(Clbb))) / self.Jc
        
        # 钻头节点
        dydt[2*n-1] = (self.Kcb * (x[n-2] - x[n-1]) + (self.Ccb) * (d[n-2] - d[n-1]) - 
                     Tab - np.real(Tfb) - (np.real(Clb) * d[n-1])) / self.Jb
        
        if t % 10 < 0.1:
            print(f"Time: {t:.2f}, d: {d[n-1]:.4f}")
        
        return dydt

    def solve_model(self):
        # 初始条件
        x0 = np.zeros(self.n)  # 初始角位移
        v0 = np.zeros(self.n)  # 初始角速度
        y0 = np.concatenate((x0, v0))
        
        # 时间配置
        time = self.TIME * 10
        dt = 10 * self.Dt
        tspan = np.arange(0, time+dt, dt)
        
        # 解决系统方程
        solution = solve_ivp(
            self.odefunc,
            [0, time],
            y0,
            method='RK45',
            t_eval=tspan,
            rtol=1e-6,
            atol=1e-8
        )
        
        t = solution.t
        y = solution.y.T
        
        return t, y

    def process_results(self, t, y):
        n = self.n
        
        # 提取结果
        # 钻铤
        AngleDisplacements_collar = y[:, n-2] * 0.1                        # 角位移
        AngleVelocities_collar = y[:, 2*n-2]                              # 角速度
        AngleAcceleration_collar = np.zeros_like(AngleVelocities_collar)   # 角加速度
        
        # 钻头
        AngleDisplacements_bit = y[:, n-1] * 0.1                          # 角位移
        AngleVelocities_bit = y[:, 2*n-1]                                # 角速度
        AngleAcceleration_bit = np.zeros_like(AngleVelocities_bit)        # 角加速度
        
        # 计算角加速度和相关参数
        Tb = np.zeros_like(t)
        Tzp = np.zeros_like(t)
        
        for i in range(len(t)):
            dydt = self.odefunc(t[i], y[i, :])
            AngleAcceleration_collar[i] = dydt[2*n-2]
            AngleAcceleration_bit[i] = dydt[2*n-1]
            if AngleAcceleration_bit[i] > 20:
                AngleAcceleration_bit[i] = 0
            
            # 计算钻头扭矩
            Tb[i] = (self.Kcb * 5 * (AngleDisplacements_collar[i] - AngleDisplacements_bit[i]) + 
                    self.Ccb * (AngleVelocities_collar[i] - AngleVelocities_bit[i])) * 10**(-3)  # 钻头扭矩
            Tzp[i] = Tb[i] + 8  # 井口扭矩
        
        # 计算相对角位移和角速度
        relativeAngleDisplacements = self.v * t * 0.1 - AngleDisplacements_bit  # 相对角位移
        relativeAngleVelocities = AngleVelocities_bit - self.v               # 相对角速度
        
        # 计算SSI
        half_idx = int(0.5 * len(t))
        vb_max = np.max(AngleVelocities_bit[half_idx:])  # 钻头最大角速度
        vb_min = np.min(AngleVelocities_bit[half_idx:])  # 钻头最小角速度
        SSI = (vb_max - vb_min) / (2 * self.v)           # 粘滑振动等级SSI
        
        # 评估风险等级
        if SSI < 0.5:
            riskLevel = '安全'
            color = 'green'
        elif SSI >= 0.5 and SSI < 1.0:
            riskLevel = '低风险'
            color = 'yellow'
        elif SSI >= 1.0 and SSI < 1.5:
            riskLevel = '中风险'
            color = 'orange'
        else:
            riskLevel = '高风险'
            color = 'red'
        
        print(f'v: {self.v:.4f}, WOB: {self.WOB:.1f}, SSI: {SSI:.4f}, 风险等级: {riskLevel}')
        
        # 返回处理后的结果
        # 修改了参数名称对应为前端的参数名称     
        results = {
            'time': t * 0.1,  # 转换时间单位为秒
            'angel_x': AngleDisplacements_bit,
            'angle_v': AngleVelocities_bit,
            'angle_a': AngleAcceleration_bit,
            'drill_m': Tb,
            'relativex': relativeAngleDisplacements,
            'relativey': relativeAngleVelocities,
            'SSI': SSI,
        }
        
        return results

    def get_download_folder(self, prefix):
        """ 获取当前操作系统的下载文件夹路径 """
        if os.name == 'nt':  # Windows
            return Path(os.environ['USERPROFILE']) / 'Downloads'
        elif os.name == 'posix':  # macOS/Linux
            return Path.home() / 'Downloads'
        else:
            raise Exception("Unsupported OS")

    def save_results(self, results):

        output_folder = self.get_download_folder("粘滑振动")
        # 创建输出目录
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
        # 输出角位移数据
        data3 = np.column_stack((results['time'], results['angel_x']))
        pd.DataFrame(data3).to_excel(output_folder / '角位移.xlsx', header=False, index=False)

        # 输出角速度数据
        data2 = np.column_stack((results['time'], results['angle_v']))
        pd.DataFrame(data2).to_excel(output_folder / '角速度.xlsx', header=False, index=False)

        # 输出角加速度数据
        data1 = np.column_stack((results['time'], results['angle_a']))
        pd.DataFrame(data1).to_excel(output_folder / '角加速度.xlsx', header=False, index=False)

        # 输出钻头扭矩数据
        data4 = np.column_stack((results['time'], results['drill_m']))
        pd.DataFrame(data4).to_excel(output_folder / '钻头扭矩.xlsx', header=False, index=False)

        # 输出钻头粘滑振动相轨迹数据
        data5 = np.column_stack((results['relativex'], results['relativey']))
        pd.DataFrame(data5).to_excel(output_folder / '钻头粘滑振动相轨迹.xlsx', header=False, index=False)
    

        
        # # 保存SSI值和风险等级
        # with open(output_folder / 'SSI分析结果.txt', 'w') as f:
        #     f.write(f'SSI: {results["SSI"]:.4f}\n')
        #     f.write(f'风险等级: {results["riskLevel"]}\n')

    def plot_results(self, results):
        # 输出角位移图
        plt.figure(figsize=(10, 6))
        plt.plot(results['t'], results['AngleDisplacements_bit'])
        plt.xlabel('时间（s）')
        plt.ylabel('角位移（rad）')
        plt.grid(True)
        plt.savefig('output/角位移.png', dpi=300)
        plt.close()
        
        # 输出角速度图
        plt.figure(figsize=(10, 6))
        plt.plot(results['t'], results['AngleVelocities_bit'])
        plt.xlabel('时间（s）')
        plt.ylabel('角速度（rad/s）')
        plt.grid(True)
        plt.savefig('output/角速度.png', dpi=300)
        plt.close()
        
        # 输出角加速度图
        plt.figure(figsize=(10, 6))
        plt.plot(results['t'], results['AngleAcceleration_bit'])
        plt.xlabel('时间（s）')
        plt.ylabel('角加速度（rad/s^2）')
        plt.grid(True)
        plt.savefig('output/角加速度.png', dpi=300)
        plt.close()
        
        # 输出钻头扭矩图
        plt.figure(figsize=(10, 6))
        plt.plot(results['t'], results['Tb'])
        plt.xlabel('时间（s）')
        plt.ylabel('钻头扭矩（kN·m）')
        plt.grid(True)
        plt.savefig('output/钻头扭矩.png', dpi=300)
        plt.close()
        
        # 输出钻头粘滑振动相轨迹图
        plt.figure(figsize=(10, 6))
        plt.plot(results['relativeAngleDisplacements'], results['relativeAngleVelocities'])
        plt.xlabel('相对角位移（rad）')
        plt.ylabel('相对角速度（rad/s）')
        plt.grid(True)
        plt.savefig('output/钻头粘滑振动相轨迹.png', dpi=300)
        plt.close()

    def run_simulation(self):
        # 初始化参数
        self.initialize_parameters()
        
        # 求解模型
        t, y = self.solve_model()
        
        # 处理结果
        results = self.process_results(t, y)
        
        # 保存结果
        # self.save_results(results)
        
        # 绘制结果
        # self.plot_results(results)
        
        return results

# def main():
#     model = StickSlipModel()
#     results = model.run_simulation()
#     for k, v in results.items():
#         print(f"key : {k}, type: {type(v)}")

# if __name__ == "__main__":
#     main()