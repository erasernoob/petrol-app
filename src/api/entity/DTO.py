from pydantic import BaseModel, validator
from typing import Optional

class HydroDTO(BaseModel):
    file_path: Optional[str]
    pailiang: Optional[float]  # 排量 (L/min)
    Dw: Optional[float]        # 井眼直径 (m)
    Rzz: Optional[float]       # 钻柱外径 (m)
    rzz: Optional[float]       # 钻柱内径 (m)
    Lzz: Optional[float]       # 钻柱长度 (m)
    Rzt: Optional[float]       # 钻铤外径 (m)
    rzt: Optional[float]       # 钻铤内径 (m)
    Lzt: Optional[float]       # 钻铤长度 (m)
    lbmx: Optional[int]        # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float]  # 钻井液密度 (kg/m³)
    n: Optional[float]         # 流性指数
    K: Optional[float]         # 稠度系数 (Pa·s^n)
    miu: Optional[float]       # 塑性粘度 (Pa·s)
    taof: Optional[float]      # 屈服值 (Pa)
    A1: Optional[float]        # 喷嘴1尺寸 (mm)
    C1: Optional[int]          # 喷嘴1个数
    A2: Optional[float]        # 喷嘴2尺寸 (mm)
    C2: Optional[int]          # 喷嘴2个数
    A3: Optional[float]        # 喷嘴3尺寸 (mm)
    C3: Optional[int]          # 喷嘴3个数
    Lp: Optional[float]        # 单根钻杆长度 (m)
    Li: Optional[float]        # 接头长度 (m)
    rzzjt: Optional[float]     # 接头内径 (m)
    L1: Optional[float]        # 地面高压管线长度 (m)
    d1: Optional[float]        # 地面高压管线内径 (m)
    L2: Optional[float]        # 立管长度 (m)
    d2: Optional[float]        # 立管内径 (m)
    L3: Optional[float]        # 水龙带长度 (m)
    d3: Optional[float]        # 水龙带内径 (m)
    L4: Optional[float]        # 方钻杆长度 (m)
    d4: Optional[float]        # 方钻杆内径 (m)
    yxmd: Optional[float]      # 岩屑密度 (kg/m³)
    H: Optional[float]         # 岩屑床高度 (%)
    yx: Optional[int]

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class TorqueDTO(BaseModel):
    file_path1: Optional[str]
    file_path2: Optional[str]
    wc: Optional[int]          # 工况选择
    v: Optional[float]         # 钻进速度 (m/s)
    omega: Optional[float]     # 转速 (rad/s)
    T0: Optional[float]        # 钻压 (N)
    rhoi: Optional[int]        # 钻井液密度 (kg/m³)
    Dw: Optional[float]        # 井眼直径 (m)
    tgxs: Optional[int]        # 套管下深 (m)
    miua11: Optional[float]    # 套管段摩阻系数
    miua22: Optional[float]    # 裸眼段摩阻系数
    js: Optional[int]          # 计算井深 (m)

class LimitEyeDTO(BaseModel):
    file_path: Optional[str]
    pailiang: Optional[float]  # 排量 (L/min)
    Dw: Optional[float]        # 井眼直径 (m)
    Rzz: Optional[float]       # 钻柱外径 (m)
    rzz: Optional[float]       # 钻柱内径 (m)
    Lzz: Optional[float]       # 钻柱长度 (m)
    Rzt: Optional[float]       # 钻铤外径 (m)
    rzt: Optional[float]       # 钻铤内径 (m)
    Lzt: Optional[float]       # 钻铤长度 (m)
    lbmx: Optional[int]        # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float]  # 钻井液密度 (kg/m³)
    n: Optional[float]         # 流性指数
    K: Optional[float]         # 稠度系数 (Pa·s^n)
    miu: Optional[float]       # 塑性粘度 (Pa·s)
    taof: Optional[float]      # 屈服值 (Pa)
    y: Optional[int]
    yxmd: Optional[float]
    H: Optional[float]
    jsjg: Optional[int]        # 井深计算间隔 (m)

class LimitHydroDTO(BaseModel):
    file_path: Optional[str]
    # 基础参数
    pailiang: Optional[float]  # 排量 (L/min)
    Dw: Optional[float]        # 井眼直径 (m)
    Rzz: Optional[float]       # 钻柱外径 (m)
    rzz: Optional[float]       # 钻柱内径 (m)
    Lzz: Optional[float]       # 钻柱长度 (m)
    Rzt: Optional[float]       # 钻铤外径 (m)
    rzt: Optional[float]       # 钻铤内径 (m)
    Lzt: Optional[float]       # 钻铤长度 (m)
    jsjg: Optional[int]        # 井深计算间隔 (m)
    # 流体参数
    lbmx: Optional[int]        # 流变模型 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float]  # 钻井液密度 (kg/m³)
    n: Optional[float]         # 幂律指数
    K: Optional[float]         # 稠度系数 (Pa·s^n)
    miu: Optional[float]       # 塑性粘度 (Pa·s)
    taof: Optional[float]      # 屈服值 (Pa)
    # 喷嘴压力参数
    A1: Optional[float]        # 喷嘴1尺寸 (mm)
    C1: Optional[int]          # 喷嘴1个数
    A2: Optional[float]        # 喷嘴2尺寸 (mm)
    C2: Optional[int]          # 喷嘴2个数
    A3: Optional[float]        # 喷嘴3尺寸 (mm)
    C3: Optional[int]          # 喷嘴3个数
    # 钻杆接头参数
    Lp: Optional[float]        # 单根钻杆长度 (m)
    Li: Optional[float]        # 接头长度 (m)
    rzzjt: Optional[float]     # 接头内径 (m)
    # 地面管道参数
    L1: Optional[float]        # 地面高压管线长度 (m)
    d1: Optional[float]        # 地面高压管线内径 (m)
    L2: Optional[float]        # 立管长度 (m)
    d2: Optional[float]        # 立管内径 (m)
    L3: Optional[float]        # 水龙带长度 (m)
    d3: Optional[float]        # 水龙带内径 (m)
    L4: Optional[float]        # 方钻杆长度 (m)
    d4: Optional[float]        # 方钻杆内径 (m)
    # 岩屑参数
    y: Optional[int]
    yxmd: Optional[float]      # 岩屑密度 (kg/m³)
    H: Optional[float]         # 岩屑床高度 (%)

class LimitMechanismDTO(BaseModel):
    file_path1: Optional[str]
    file_path2: Optional[str]
    wc: Optional[int]          # 工况选择 (旋转钻进 = 1, 滑动钻进 = 2, 起钻 = 3, 下钻 = 4, 倒划眼 = 5)
    v: Optional[float]         # 钻进速度 (m/s)
    omega: Optional[float]     # 转速 (rad/s)
    T0: Optional[float]        # 钻压 (N)
    rhoi: Optional[float]      # 钻井液密度 (kg/m³)
    Dw: Optional[float]        # 井眼直径 (m)
    tgxs: Optional[float]      # 套管下深 (m)
    miua11: Optional[float]    # 套管段摩阻系数
    miua22: Optional[float]    # 裸眼段摩阻系数
    qfqd: Optional[float]      # 钻柱屈服强度 (MPa)
    jsjg: Optional[int]        # 井深计算间隔 (m)
    ml: Optional[int]          # 钻柱模量

class LimitCurveDTO(BaseModel):
    file_path1: Optional[str]
    file_path2: Optional[str]
    Holedia: Optional[float]   # 井眼直径 (m)
    ml: Optional[float]        # 钻柱弹性模量 (MPa)
    js: Optional[float]        # 计算井深 (m)

class DrillVibrationDTO(BaseModel):
    # 钻头参数
    Lb: Optional[float]        # 钻头长度 (m)
    Db: Optional[float]        # 钻头直径 (m)
    Lp: Optional[float]        # 钻杆长度 (m)
    p1: Optional[float]        # 钻杆密度 (kg/m³)
    Dp: Optional[float]        # 钻杆外径 (m)
    dp: Optional[float]        # 钻杆内径 (m)
    Lpw: Optional[float]       # 加重钻杆长度 (m)
    p3: Optional[float]        # 加重钻杆密度 (kg/m³)
    Dpw: Optional[float]       # 加重钻杆外径 (m)
    dc: Optional[float]        # 加重钻杆内径 (m)
    Lc: Optional[float]        # 钻铤长度 (m)
    p2: Optional[float]        # 钻铤密度 (kg/m³)
    Dc: Optional[float]        # 钻铤外径 (m)
    dpw: Optional[float]       # 钻铤内径 (m)
    # 钻井液参数
    uf: Optional[float]        # 钻井液塑性粘度 (mPa.s)
    sita3: Optional[float]     # 旋转粘度计读数（3转）
    sita100: Optional[float]   # 旋转粘度计读数（100转）
    sita200: Optional[float]   # 旋转粘度计读数（200转）
    # 计算参数
    wob: Optional[float]       # 钻压 (kN)
    V: Optional[float]         # 转速 (RPM)
    miusb: Optional[float]     # 静摩擦系数
    miucb: Optional[float]     # 动摩擦系数
    Lv: Optional[float]        # 垂直段长度 (m)
    dl: Optional[float]        # 质量块长度 (m)
    TIME: Optional[float]      # 计算时长 (s)
    Dt: Optional[float]        # 时间步长 (s)

class MSEDTO(BaseModel):
    file_path: Optional[str]

class ModelTrainDTO(BaseModel):
    target_file_path: Optional[str]
    LSTM_nums: Optional[int]   # LSTM个数
    LSTM_layers: Optional[int] # LSTM层数
    neuron_cnt: Optional[int]
    window_size: Optional[int]
    lr: Optional[float]
    num_epochs: Optional[int]  # 训练批次

class ModelPredictDTO(BaseModel):
    file_path: Optional[str]
