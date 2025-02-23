import pandas as pd
from fastapi import Response
import io
from entity.DTO import HydroDTO
from service.Hydro import Hydro

def process_hydro_data(hydro_dto : HydroDTO):
    # 读取 Excel 文件
    guiji = pd.read_excel(hydro_dto.file_path).values  

    # 计算结果
    P, Plg, Pdm, Pgn, Phk, ECD, Pgnyx, Phkyx, ECDyx, Sk = Hydro(
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

    df = pd.DataFrame({
        "井深 (m)": Sk.flatten(),  
        "钻柱压力 (Pgn, MPa)": Pgn.flatten(),
        "环空压力 (Phk, MPa)": Phk.flatten(),
        "ECD (g/cm³)": ECD.flatten()
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=hydro_data.csv"})
    
    