# api/routes/torque.py
from fastapi import Response
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import TorqueDTO
from pathlib import Path
from service.Hydro import Hydro

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
torque_cache = {}

@router.post("/torque")
async def get_torque_data(torque_dto: TorqueDTO):
    global torque_cache

    # 轨迹和钻具组合
    orbit = pd.read_excel(torque_dto.file_path1).values  
    drill = pd.read_excel(torque_dto.file_path2).values  

    # 云图 N E TCS T M Sk
    # N, E, TCS, T, M, Sk = main_func(
    #     orbit, drill, torque_dto.wc, torque_dto.T0, torque_dto.rhoi, 
    #     torque_dto.Dw, torque_dto.tgxs, torque_dto.miua11, torque_dto.miua22, 
    #     torque_dto.js, torque_dto.v, torque_dto.omega)

    base_path = Path("D:/petrol-app/mock/torque")
    
        # 读取 Excel 文件
    N = pd.read_excel(base_path / "N.xlsx").values.flatten()
    E = pd.read_excel(base_path / "E.xlsx").values.flatten()
    T = pd.read_excel(base_path / "T.xlsx").values.flatten()
    M = pd.read_excel(base_path / "M.xlsx").values.flatten()
    TCS = pd.read_excel(base_path / "TCS.xlsx").values.flatten()
    Sk = pd.read_excel(base_path / "Sk.xlsx").values.flatten()


# Creating a dictionary of Series
    data = {
        "N": pd.Series(N),
        "E": pd.Series(E),
        "TCS": pd.Series(TCS),
        "T": pd.Series(T),
        "M": pd.Series(M),
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
    

 

