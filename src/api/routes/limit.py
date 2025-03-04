# api/routes/torque.py
from fastapi import Response
from pathlib import Path
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
    guiji = pd.read_excel(limit_eye_dto.file_path1).values  

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

    # 调用 hydro 函数计算结果
    ECD, Sk, Pgn, Phk = limit_eye_function(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt)


    base_path = Path("D:/petrol-app/mock/limit")
        # 读取 Excel 文件
    ECO = pd.read_excel(base_path / "ECD.xlsx").values.flatten()
    Sk = pd.read_excel(base_path / "Sk.xlsx").values.flatten()

    # 将数据保存为 CSV 文件
    df = pd.DataFrame({
        "Sk": Sk.flatten(),
        # "Pgn": Pgn.flatten(),
        # "Phk": Phk.flatten(),
        "ECD": ECD.flatten()
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

def limit_eye_function():
    return Sk, P, Plg

def limit_hydro_function():
    return 
    


@router.post('/limit/hydro')
def get_limit_hydro(limit_hydro_dto: LimitHydroDTO):
    Sk, P, Plg = limit_hydro_function(limit_hydro_dto)

    base_path = Path("D:/petrol-app/mock/limit")
        # 读取 Excel 文件
    df_P = pd.read_excel(base_path / "总循环压耗.xlsx")
    df_Plg = pd.read_excel(base_path / "立管压力.xlsx")

    Sk = df_P.iloc[:,0]
    P = df_P.iloc[:,1]
    Plg = df_Plg.iloc[:,1]


    # 创建 DataFrame
    df = pd.DataFrame({
        "P": Sk.flatten(), # 总循环压耗
        "Plg": Plg.flatten(), # 立管压力
        "Sk": P.flatten(),
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

def limit_mechanism(guiji, zuanju, wc, T0, rhoi, Dw, tgxs, miua11, miua22, qfqd, jsjg, v, omega):
        return

@router.post("/limit/mechanism")
async def get_limit_mechanism_result(limit_mechanism_dto: LimitMechanismDTO ):
    # 读取上传的 Excel 文件
    guiji = pd.read_excel(limit_mechanism_dto.file_path1).values  
    zuanju = pd.read_excel(limit_mechanism_dto.file_path2).values  

    x_coords, T_result, M_reuslt, aq_result = limit_mechanism(
        guiji, zuanju, 
        limit_mechanism_dto.wc, 
        limit_mechanism_dto.T0, 
        limit_mechanism_dto.rhoi, 
        limit_mechanism_dto.Dw, 
        limit_mechanism_dto.tgxs, 
        limit_mechanism_dto.miua11, 
        limit_mechanism_dto.miua22, 
        limit_mechanism_dto.qfqd, 
        limit_mechanism_dto.jsjg, 
        limit_mechanism_dto.v, 
        limit_mechanism_dto.omega
    )
    
    base_path = Path("D:/petrol-app/mock/drill")

    df_M = pd.read_excel(base_path / "旋转钻进_井口扭矩.xlsx")
    df_T = pd.read_excel(base_path / "旋转钻进_井口轴向力.xlsx")
    df_aq = pd.read_excel(base_path / "旋转钻进_安全系数.xlsx")

    Sk = df_M.iloc[:, 0]

    T = df_T.iloc[:, 1]
    M = df_M.iloc[:, 1]
    aq = df_aq.iloc[:, 1]

    df = pd.DataFrame({
        'Sk': Sk,
        'T': T,
        'M': M,
        'aq': aq
    })



    # df = pd.DataFrame({
    #     "Sk": x_coords.flatten(),   
    #     "T": T_result.flatten(), # 井口轴向力
    #     "M": M_reuslt.flatten(), # 井口扭矩
    #     "aq": aq_result.flatten() # 安全系数
    # })

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
    zuanju = pd.read_excel(limit_curve_dto.file_path1).values  
    Sk, fs, fh = limit_curve_function(
        guiji, 
        limit_curve_dto.Holedia, 
        limit_curve_dto.ml, 
        zuanju, 
        limit_curve_dto.js
    )

    

    df = pd.DataFrame({
        "Sk": Sk.flatten(),   
        "fs": fs.flatten(), # 正弦
        "fh (kN)": fh.flatten() # 螺旋
    })

      # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

    

def limit_curve_function(guiji, Holedia, ml, zuanju, js):
    return 
    

    

    


    

    
    

    