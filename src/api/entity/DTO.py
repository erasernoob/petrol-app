from pydantic import BaseModel

class HydroDTO(BaseModel):
    file_path: str
    pailiang: float  # 排量 (L/min)
    Dw: float        # 井眼直径 (m)
    Rzz: float       # 钻柱外径 (m)
    rzz: float       # 钻柱内径 (m)
    Lzz: float       # 钻柱长度 (m)
    Rzt: float       # 钻铤外径 (m)
    rzt: float       # 钻铤内径 (m)
    Lzt: float       # 钻铤长度 (m)
    lbmx: int        # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: float  # 钻井液密度 (kg/m³)
    n: float         # 流性指数
    K: float         # 稠度系数 (Pa·s^n)
    miu: float       # 塑性粘度 (Pa·s)
    taof: float      # 屈服值 (Pa)
    A1: float        # 喷嘴1尺寸 (mm)
    C1: int          # 喷嘴1个数
    A2: float        # 喷嘴2尺寸 (mm)
    C2: int          # 喷嘴2个数
    A3: float        # 喷嘴3尺寸 (mm)
    C3: int          # 喷嘴3个数
    Lp: float        # 单根钻杆长度 (m)
    Li: float        # 接头长度 (m)
    rzzjt: float     # 接头内径 (m)
    L1: float        # 地面高压管线长度 (m)
    d1: float        # 地面高压管线内径 (m)
    L2: float        # 立管长度 (m)
    d2: float        # 立管内径 (m)
    L3: float        # 水龙带长度 (m)
    d3: float        # 水龙带内径 (m)
    L4: float        # 方钻杆长度 (m)
    d4: float        # 方钻杆内径 (m)
    yxmd: float      # 岩屑密度 (kg/m³)
    H: float         # 岩屑床高度 (%)
    yx: int
class TorqueDTO(BaseModel):
    file_path1: str
    file_path2: str
    wc: int  # 工况选择
    v: float  # 钻进速度 (m/s)
    omega: float  # 转速 (rad/s)
    T0: float  # 钻压 (N)
    rhoi: float  # 钻井液密度 (kg/m³)
    Dw: float  # 井眼直径 (m)
    tgxs: float  # 套管下深 (m)
    miua11: float  # 套管段摩阻系数
    miua22: float  # 裸眼段摩阻系数
    js: float  # 计算井深 (m)

class LimitEyeDTO(BaseModel):
    file_path: str
    pailiang: float  # 排量 (L/min)
    Dw: float  # 井眼直径 (m)
    Rzz: float  # 钻柱外径 (m)
    rzz: float  # 钻柱内径 (m)
    Lzz: float  # 钻柱长度 (m)
    Rzt: float  # 钻铤外径 (m)
    rzt: float  # 钻铤内径 (m)
    Lzt: float  # 钻铤长度 (m)
    lbmx: int  # 流变模式 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: float  # 钻井液密度 (kg/m³)
    n: float  # 流性指数
    K: float  # 稠度系数 (Pa·s^n)
    miu: float  # 塑性粘度 (Pa·s)
    taof: float  # 屈服值 (Pa)

class LimitHydroDTO(BaseModel):
    # 基础参数
    pailiang: float  # 排量 (L/min)
    Dw: float  # 井眼直径 (m)
    Rzz: float  # 钻柱外径 (m)
    rzz: float  # 钻柱内径 (m)
    Lzz: float  # 钻柱长度 (m)
    Rzt: float  # 钻铤外径 (m)
    rzt: float  # 钻铤内径 (m)
    Lzt: float  # 钻铤长度 (m)
    jsjg: float  # 井深计算间隔 (m)
    
    # 流体参数
    lbmx: int  # 流变模型 (1=宾汉, 2=幂律, 3=赫巴)
    fluidden: float  # 钻井液密度 (kg/m³)
    n: float  # 幂律指数
    K: float  # 稠度系数 (Pa·s^n)
    miu: float  # 塑性粘度 (Pa·s)
    taof: float  # 屈服值 (Pa)

    # 喷嘴压力参数
    A1: float  # 喷嘴1尺寸 (mm)
    C1: int  # 喷嘴1个数
    A2: float  # 喷嘴2尺寸 (mm)
    C2: int  # 喷嘴2个数
    A3: float  # 喷嘴3尺寸 (mm)
    C3: int  # 喷嘴3个数

    # 钻杆接头参数
    Lp: float  # 单根钻杆长度 (m)
    Li: float  # 接头长度 (m)
    rzzjt: float  # 接头内径 (m)

    # 地面管道参数
    L1: float  # 地面高压管线长度 (m)
    d1: float  # 地面高压管线内径 (m)
    L2: float  # 立管长度 (m)
    d2: float  # 立管内径 (m)
    L3: float  # 水龙带长度 (m)
    d3: float  # 水龙带内径 (m)
    L4: float  # 方钻杆长度 (m)
    d4: float  # 方钻杆内径 (m)

    # 岩屑参数
    yxmd: float  # 岩屑密度 (kg/m³)
    H: float  # 岩屑床高度 (%)
class LimitMechanismDTO(BaseModel):
    file_path1: str
    file_path2: str
    # 工况选择
    wc: int  # 工况选择 (旋转钻进 = 1, 滑动钻进 = 2, 起钻 = 3, 下钻 = 4, 倒划眼 = 5)
    
    # 钻井参数
    v: float  # 钻进速度 (m/s)
    omega: float  # 转速 (rad/s)
    T0: float  # 钻压 (N)
    rhoi: float  # 钻井液密度 (kg/m³)
    Dw: float  # 井眼直径 (m)
    tgxs: float  # 套管下深 (m)
    miua11: float  # 套管段摩阻系数
    miua22: float  # 裸眼段摩阻系数
    qfqd: float  # 钻柱屈服强度 (MPa)
    jsjg: float  # 井深计算间隔 (m)
class LimitCurveDTO(BaseModel):
    file_path1: str
    file_path2: str
    Holedia: float  # 井眼直径 (m)
    ml: float  # 钻柱弹性模量 (MPa)
    js: float  # 计算井深 (m)
class DrillVibrationDTO(BaseModel):
    # 钻头参数
    Lb: float  # 钻头长度 (m)
    Db: float  # 钻头直径 (m)
    Lp: float  # 钻杆长度 (m)
    p1: float  # 钻杆密度 (kg/m³)
    Dp: float  # 钻杆外径 (m)
    dp: float  # 钻杆内径 (m)
    Lpw: float  # 加重钻杆长度 (m)
    p3: float  # 加重钻杆密度 (kg/m³)
    Dpw: float  # 加重钻杆外径 (m)
    dc: float  # 加重钻杆内径 (m)
    Lc: float  # 钻铤长度 (m)
    p2: float  # 钻铤密度 (kg/m³)
    Dc: float  # 钻铤外径 (m)
    dpw: float  # 钻铤内径 (m)
    # 钻井液参数
    uf: float  # 钻井液塑性粘度 (mPa.s)
    sita3: float  # 旋转粘度计读数（3转）
    sita100: float  # 旋转粘度计读数（100转）
    sita200: float  # 旋转粘度计读数（200转）
    # 计算参数
    wob: float  # 钻压 (kN)
    V: float  # 转速 (RPM)
    miusb: float  # 静摩擦系数
    miucb: float  # 动摩擦系数
    Lv: float  # 垂直段长度 (m)
    dl: float  # 质量块长度 (m)
    TIME: float  # 计算时长 (s)
    Dt: float  # 时间步长 (s)

class MSE(BaseModel):
    file_path: str

