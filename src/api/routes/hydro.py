# api/routes/hydro.py
from fastapi import Response
import io
from fastapi import APIRouter
from service import hydra
import pandas as pd
from pathlib import Path
from entity.DTO import HydroDTO


# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
hydro_cache = {}


@router.post("/hydro")
async def get_hydro_chart_result(hydro_dto: HydroDTO):
    global hydro_cache


    # 读取 Excel 文件
    # TODO: change this to upload the file
    guiji = pd.read_excel(hydro_dto.file_path).values  

    # 计算结果
    Sk, Pgn, Phk, ECD, P, Plg, Pdm, dertaPzt = hydra.main(
        guiji, hydro_dto.lbmx, hydro_dto.pailiang, hydro_dto.fluidden, 
        hydro_dto.n, hydro_dto.K, hydro_dto.miu, hydro_dto.taof, 
        hydro_dto.Dw, hydro_dto.A1, hydro_dto.C1, hydro_dto.A2, 
        hydro_dto.C2, hydro_dto.A3, hydro_dto.C3, hydro_dto.Rzz, 
        hydro_dto.rzz, hydro_dto.Lzz, hydro_dto.Rzt, hydro_dto.rzt, 
        hydro_dto.Lzt, hydro_dto.L1, hydro_dto.d1, hydro_dto.L2, 
        hydro_dto.d2, hydro_dto.L3, hydro_dto.d3, hydro_dto.L4, 
        hydro_dto.d4, hydro_dto.Lp, hydro_dto.Li, hydro_dto.rzzjt, 
        hydro_dto.yxmd, hydro_dto.H, hydro_dto.yx
    )

    print(ECD)


    df = pd.DataFrame({
        "井深 (m)": pd.Series(Sk.flatten()),  
        "钻柱压力 (Pgn, MPa)": pd.Series(Pgn.flatten()),
        "环空压力 (Phk, MPa)": pd.Series(Phk.flatten()),
        "ECD (g/cm³)": pd.Series(ECD.flatten()),
    })

    hydro_cache = {
    "总循环压耗（MPa）": float(P),  
    "立管压力（MPa）": float(Plg),
    "地面管汇压耗（MPa）": float(Pdm),
    "钻头压降（MPa）": float(dertaPzt)  
    }

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=hydro_data.csv"})


@router.post('/hydro/data')
def get_extra_hydro_data():
    if not hydro_cache:
        return {"error": 'nothing in the cache'}
    print(hydro_cache)
    return hydro_cache
    

