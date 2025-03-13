# api/routes/torque.py
from fastapi import Response
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import TorqueDTO
from pathlib import Path
from service import torque

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
torque_cache = {}

@router.post("/torque")
async def get_torque_data(torque_dto: TorqueDTO):
    global torque_cache

    # 轨迹和钻具组合
    orbit = pd.read_excel(torque_dto.file_path1, header=None).to_numpy()
    zuanju = pd.read_excel(torque_dto.file_path2, header=None).to_numpy()  

    # 云图 N E TCS T M Sk
    N, E, TCS, T, M, Sk = torque.mainfunc(
        orbit, zuanju, torque_dto.wc, torque_dto.T0, torque_dto.rhoi, 
        torque_dto.Dw, torque_dto.tgxs, torque_dto.miua11, torque_dto.miua22, 
        torque_dto.js, torque_dto.v, torque_dto.omega)
    


# Creating a dictionary of Series
    data = {
        "N": pd.Series(N),
        "E": pd.Series(E),
        "TCS": pd.Series(TCS), # 垂深
        "T": pd.Series(T), # 轴向力
        "M": pd.Series(M), # 扭矩
        "Sk": pd.Series(Sk)
    }

    # Creating DataFrame
    df = pd.DataFrame(data)

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

def main_func():
    return
    

 

