# api/routes/torque.py
import numpy as np
from fastapi import Response
from pathlib import Path
from service import limit_eye, limit_mecha, limit_mecha_curve
from service import limit_hydra, limit_curve
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import LimitEyeDTO, LimitCurveDTO, LimitHydroDTO, LimitMechanismDTO

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
torque_cache = {}

@router.post('/limit/eye')
def get_limit_eye(limit_eye_dto : LimitEyeDTO):
    # 从 DTO 获取参数
    guiji = pd.read_excel(limit_eye_dto.file_path).values  

    lbmx = limit_eye_dto.lbmx
    pailiang = limit_eye_dto.pailiang
    fluidden = limit_eye_dto.fluidden
    n = limit_eye_dto.n
    K = limit_eye_dto.K
    miu = limit_eye_dto.miu
    taof = limit_eye_dto.taof
    Dw = limit_eye_dto.Dw
    Rzz = limit_eye_dto.Rzz
    rzz = limit_eye_dto.rzz
    Lzz = limit_eye_dto.Lzz
    Rzt = limit_eye_dto.Rzt
    rzt = limit_eye_dto.rzt
    Lzt = limit_eye_dto.Lzt
    y = limit_eye_dto.y
    yxmd = limit_eye_dto.yxmd
    H = limit_eye_dto.H

    ECD, Sk = limit_eye.main(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, y, yxmd, H)
    interval = limit_eye_dto.jsjg

    ECD_values = ECD[interval::interval].tolist()  # 从 ECD 中提取间隔为 interval 的元素
    Sk_values = Sk[interval::interval].tolist()  # 从 Sk 中提取间隔为 interval 的元素
    
    # 确保最后一个元素在结果中
    if ECD_values[-1] != ECD[-1]:
        ECD_values.append(ECD[-1])  # 如果最后一个元素没有包含在内，添加到列表中
    if Sk_values[-1] != Sk[-1]:
        Sk_values.append(Sk[-1])  # 如果最后一个元素没有包含在内，添加到列表中
    


    # 将数据保存为 CSV 文件
    df = pd.DataFrame({
        "Sk": pd.Series(Sk_values),
        "ECD": pd.Series(ECD_values),
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})



@router.post('/limit/hydro')
def get_limit_hydro(limit_hydro_dto: LimitHydroDTO):
    Sk, P, Plg = limit_hydra.main(limit_hydro_dto)


    # 创建 DataFrame
    df = pd.DataFrame({
        "P": P, # 总循环压耗
        "Plg": Plg[:len(Sk)], # 立管压力
        "Sk": Sk,
    })



    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})
    
@router.post("/limit/mechanism/curve")
async def get_limit_mecanism_curve(dto: LimitMechanismDTO):
    T_out, X, max_depth = limit_mecha_curve.main(dto)
    fs = T_out[:, -2]
    fh = T_out[:, -1]

    T_out = T_out[:, :-2]
    
    df = pd.DataFrame(
    T_out,
    columns=[
        f"{(i + 1) * dto.jsjg if i + 1 != T_out.shape[1] else max_depth}m"
        for i in range(T_out.shape[1])
    ]
    )
    df["井深"] = X
    df["正弦屈曲临界载荷"] = fs
    df["螺旋屈曲临界载荷"] = fh

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})
    

@router.post("/limit/mechanism")
async def get_limit_mechanism_result(limit_mechanism_dto: LimitMechanismDTO ):
    T_result, M_reuslt, aq_result, x_coords = limit_mecha.main(limit_mechanism_dto)
    T_result = T_result.flatten()
    aq_result = aq_result.flatten()

    for index, t in enumerate(T_result):
        if t <= 0:
            aq_result[index] = np.nan

    df = pd.DataFrame({
        "Sk": x_coords.flatten(),   
        "T": T_result, # 井口轴向力
        "M": M_reuslt.flatten(), # 井口扭矩
        "aq": aq_result # 安全系数
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})


@router.post("/limit/curve")
async def get_limit_curve_result(limit_curve_dto: LimitCurveDTO ):
    # 读取上传的 Excel 文件
    guiji = pd.read_excel(limit_curve_dto.file_path1).values  
    
    # 钻具组合去掉第一列的列名
    zuanju = pd.read_excel(limit_curve_dto.file_path2, header=None)
    zuanju = zuanju.iloc[:, 1:].values

    fh, fs = limit_curve.main(
        guiji, 
        zuanju,
        limit_curve_dto.Holedia, 
        limit_curve_dto.ml, 
        limit_curve_dto.js
    )

    df = pd.DataFrame({
        "Sk": pd.Series(range(1, int(limit_curve_dto.js) + 1)),
        "fs": pd.Series(fs),
        "fh": pd.Series(fh),
    })

      # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

    

def limit_curve_function(guiji, Holedia, ml, zuanju, js):
    return 
    

    

    


    

    
    

    