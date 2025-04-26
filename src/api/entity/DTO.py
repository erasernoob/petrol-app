from pydantic import BaseModel, validator
from typing import Optional

class HydroDTO(BaseModel):
    file_path: Optional[str] = None
    pailiang: Optional[float] = None  # 排量 (L/min)
    Dw: Optional[float] = None        # 井眼直径 (m)
    Rzz: Optional[float] = None       # 钻柱外径 (m)
    rzz: Optional[float] = None       # 钻柱内径 (m)
    Lzz: Optional[float] = None       # 钻柱长度 (m)
    Rzt: Optional[float] = None       # 钻铤外径 (m)
    rzt: Optional[float] = None       # 钻铤内径 (m)
    Lzt: Optional[float] = None       # 钻铤长度 (m)
    lbmx: Optional[int] = None        # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float] = None  # 钻井液密度 (kg/m³)
    n: Optional[float] = None         # 流性指数
    K: Optional[float] = None         # 稠度系数 (Pa·s^n)
    miu: Optional[float] = None       # 塑性粘度 (Pa·s)
    taof: Optional[float] = None      # 屈服值 (Pa)
    A1: Optional[float] = None        # 喷嘴1尺寸 (mm)
    C1: Optional[int] = None          # 喷嘴1个数
    A2: Optional[float] = None        # 喷嘴2尺寸 (mm)
    C2: Optional[int] = None          # 喷嘴2个数
    A3: Optional[float] = None        # 喷嘴3尺寸 (mm)
    C3: Optional[int] = None          # 喷嘴3个数
    Lp: Optional[float] = None        # 单根钻杆长度 (m)
    Li: Optional[float] = None        # 接头长度 (m)
    rzzjt: Optional[float] = None     # 接头内径 (m)
    L1: Optional[float] = None        # 地面高压管线长度 (m)
    d1: Optional[float] = None        # 地面高压管线内径 (m)
    L2: Optional[float] = None        # 立管长度 (m)
    d2: Optional[float] = None        # 立管内径 (m)
    L3: Optional[float] = None        # 水龙带长度 (m)
    d3: Optional[float] = None        # 水龙带内径 (m)
    L4: Optional[float] = None        # 方钻杆长度 (m)
    d4: Optional[float] = None        # 方钻杆内径 (m)
    yxmd: Optional[float] = None      # 岩屑密度 (kg/m³)
    H: Optional[float] = None         # 岩屑床高度 (%)
    yx: Optional[int] = None

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class TorqueDTO(BaseModel):
    file_path1: Optional[str] = None
    file_path2: Optional[str] = None
    wc: Optional[int] = None          # 工况选择
    v: Optional[float] = None         # 钻进速度 (m/s)
    omega: Optional[float] = None     # 转速 (rad/s)
    T0: Optional[float] = None        # 钻压 (N)
    rhoi: Optional[int] = None        # 钻井液密度 (kg/m³)
    Dw: Optional[float] = None        # 井眼直径 (m)
    tgxs: Optional[int] = None        # 套管下深 (m)
    miua11: Optional[float] = None    # 套管段摩阻系数
    miua22: Optional[float] = None    # 裸眼段摩阻系数
    js: Optional[int] = None          # 计算井深 (m)

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class LimitEyeDTO(BaseModel):
    file_path: Optional[str] = None
    pailiang: Optional[float] = None  # 排量 (L/min)
    Dw: Optional[float] = None        # 井眼直径 (m)
    Rzz: Optional[float] = None       # 钻柱外径 (m)
    rzz: Optional[float] = None       # 钻柱内径 (m)
    Lzz: Optional[float] = None       # 钻柱长度 (m)
    Rzt: Optional[float] = None       # 钻铤外径 (m)
    rzt: Optional[float] = None       # 钻铤内径 (m)
    Lzt: Optional[float] = None       # 钻铤长度 (m)
    lbmx: Optional[int] = None        # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float] = None  # 钻井液密度 (kg/m³)
    n: Optional[float] = None         # 流性指数
    K: Optional[float] = None         # 稠度系数 (Pa·s^n)
    miu: Optional[float] = None       # 塑性粘度 (Pa·s)
    taof: Optional[float] = None      # 屈服值 (Pa)
    y: Optional[int] = None
    yxmd: Optional[float] = None
    H: Optional[float] = None
    jsjg: Optional[int] = None        # 井深计算间隔 (m)

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class LimitHydroDTO(BaseModel):
    file_path: Optional[str] = None
    # 基础参数
    pailiang: Optional[float] = None  # 排量 (L/min)
    Dw: Optional[float] = None        # 井眼直径 (m)
    Rzz: Optional[float] = None       # 钻柱外径 (m)
    rzz: Optional[float] = None       # 钻柱内径 (m)
    Lzz: Optional[float] = None       # 钻柱长度 (m)
    Rzt: Optional[float] = None       # 钻铤外径 (m)
    rzt: Optional[float] = None       # 钻铤内径 (m)
    Lzt: Optional[float] = None       # 钻铤长度 (m)
    jsjg: Optional[int] = None        # 井深计算间隔 (m)
    # 流体参数
    lbmx: Optional[int] = None        # 流变模型 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: Optional[float] = None  # 钻井液密度 (kg/m³)
    n: Optional[float] = None         # 幂律指数
    K: Optional[float] = None         # 稠度系数 (Pa·s^n)
    miu: Optional[float] = None       # 塑性粘度 (Pa·s)
    taof: Optional[float] = None      # 屈服值 (Pa)
    # 喷嘴压力参数
    A1: Optional[float] = None        # 喷嘴1尺寸 (mm)
    C1: Optional[int] = None          # 喷嘴1个数
    A2: Optional[float] = None        # 喷嘴2尺寸 (mm)
    C2: Optional[int] = None          # 喷嘴2个数
    A3: Optional[float] = None        # 喷嘴3尺寸 (mm)
    C3: Optional[int] = None          # 喷嘴3个数
    # 钻杆接头参数
    Lp: Optional[float] = None        # 单根钻杆长度 (m)
    Li: Optional[float] = None        # 接头长度 (m)
    rzzjt: Optional[float] = None     # 接头内径 (m)
    # 地面管道参数
    L1: Optional[float] = None        # 地面高压管线长度 (m)
    d1: Optional[float] = None        # 地面高压管线内径 (m)
    L2: Optional[float] = None        # 立管长度 (m)
    d2: Optional[float] = None        # 立管内径 (m)
    L3: Optional[float] = None        # 水龙带长度 (m)
    d3: Optional[float] = None        # 水龙带内径 (m)
    L4: Optional[float] = None        # 方钻杆长度 (m)
    d4: Optional[float] = None        # 方钻杆内径 (m)
    # 岩屑参数
    y: Optional[int] = None
    yxmd: Optional[float] = None      # 岩屑密度 (kg/m³)
    H: Optional[float] = None         # 岩屑床高度 (%)

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class LimitMechanismDTO(BaseModel):
    file_path1: Optional[str] = None
    file_path2: Optional[str] = None
    wc: Optional[int] = None          # 工况选择 (旋转钻进 = 1, 滑动钻进 = 2, 起钻 = 3, 下钻 = 4, 倒划眼 = 5)
    v: Optional[float] = None         # 钻进速度 (m/s)
    omega: Optional[float] = None     # 转速 (rad/s)
    T0: Optional[float] = None        # 钻压 (N)
    rhoi: Optional[float] = None      # 钻井液密度 (kg/m³)
    Dw: Optional[float] = None        # 井眼直径 (m)
    tgxs: Optional[float] = None      # 套管下深 (m)
    miua11: Optional[float] = None    # 套管段摩阻系数
    miua22: Optional[float] = None    # 裸眼段摩阻系数
    qfqd: Optional[float] = None      # 钻柱屈服强度 (MPa)
    jsjg: Optional[int] = None        # 井深计算间隔 (m)
    ml: Optional[int] = None          # 钻柱模量

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class LimitCurveDTO(BaseModel):
    file_path1: Optional[str] = None
    file_path2: Optional[str] = None
    Holedia: Optional[float] = None   # 井眼直径 (m)
    ml: Optional[float] = None        # 钻柱弹性模量 (MPa)
    js: Optional[float] = None        # 计算井深 (m)

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class DrillVibrationDTO(BaseModel):
    # 钻头参数
    Lb: Optional[float] = None        # 钻头长度 (m)
    Db: Optional[float] = None        # 钻头直径 (m)
    Lp: Optional[float] = None        # 钻杆长度 (m)
    p1: Optional[float] = None        # 钻杆密度 (kg/m³)
    Dp: Optional[float] = None        # 钻杆外径 (m)
    dp: Optional[float] = None        # 钻杆内径 (m)
    Lpw: Optional[float] = None       # 加重钻杆长度 (m)
    p3: Optional[float] = None        # 加重钻杆密度 (kg/m³)
    Dpw: Optional[float] = None       # 加重钻杆外径 (m)
    dc: Optional[float] = None        # 加重钻杆内径 (m)
    Lc: Optional[float] = None        # 钻铤长度 (m)
    p2: Optional[float] = None        # 钻铤密度 (kg/m³)
    Dc: Optional[float] = None        # 钻铤外径 (m)
    dpw: Optional[float] = None       # 钻铤内径 (m)
    # 钻井液参数
    uf: Optional[float] = None        # 钻井液塑性粘度 (mPa.s)
    sita3: Optional[float] = None     # 旋转粘度计读数（3转）
    sita100: Optional[float] = None   # 旋转粘度计读数（100转）
    sita200: Optional[float] = None   # 旋转粘度计读数（200转）
    # 计算参数
    wob: Optional[float] = None       # 钻压 (kN)
    V: Optional[float] = None         # 转速 (RPM)
    miusb: Optional[float] = None     # 静摩擦系数
    miucb: Optional[float] = None     # 动摩擦系数
    Lv: Optional[float] = None        # 垂直段长度 (m)
    dl: Optional[float] = None        # 质量块长度 (m)
    TIME: Optional[float] = None      # 计算时长 (s)
    Dt: Optional[float] = None        # 时间步长 (s)

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class MSEDTO(BaseModel):
    file_path: Optional[str] = None

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class ModelTrainDTO(BaseModel):
    target_file_path: Optional[str] = None
    LSTM_nums: Optional[int] = None   # LSTM个数
    LSTM_layers: Optional[int] = None # LSTM层数
    neuron_cnt: Optional[int] = None
    window_size: Optional[int] = None
    lr: Optional[float] = None
    num_epochs: Optional[int] = None  # 训练批次

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class ModelPredictDTO(BaseModel):
    file_path: Optional[str] = None

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v