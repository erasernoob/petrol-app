from pydantic import BaseModel

class HydroDTO(BaseModel):
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


