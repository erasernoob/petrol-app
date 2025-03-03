# api/routes/torque.py
from fastapi import Response
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import TorqueDTO
from service.Hydro import Hydro

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
torque_cache = {}

@router.get("/torque")
def get_torque_data(torque_dto: TorqueDTO):
    global torque_cache

    # 轨迹和钻具组合
    orbit = pd.read_excel(torque_dto.file_path1).values  
    drill = pd.read_excel(torque_dto.file_path2).values  

    # 云图 N E TCS T M Sk
    N, E, TCS, T, M, Sk = main_func(
        orbit, drill, torque_dto.wc, torque_dto.T0, torque_dto.rhoi, 
        torque_dto.Dw, torque_dto.tgxs, torque_dto.miua11, torque_dto.miua22, 
        torque_dto.js, torque_dto.v, torque_dto.omega)



    df = pd.DataFrame({
        "N": N.flatten(),   # 南北位移 (Y 轴)
        "E": E.flatten(),   # 东西位移 (X 轴)
        "TCS": TCS.flatten(), # 垂向深度 (Z 轴)
        "T": T.flatten(),   # 轴向力（用于颜色映射）
        "M": M.flatten(),   # 扭矩（用于颜色映射）
        "Sk": Sk.flatten()  # 井深 (用于 2D 曲线)
    })
    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

def main_func():
    return N, E, TCS, T, M, Sk
    

 

