# api/routes/hydro.py
from fastapi import Response
import io
from fastapi import APIRouter
from service.vibration import StickSlipModel 
from pathlib import Path
from service import mse
import pandas as pd
from entity.DTO import DrillVibrationDTO, MSEDTO

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
mse_cache = {}

@router.post('/drill/vibration')
def get_limit_hydro(drillVirationDto: DrillVibrationDTO):

    model = StickSlipModel()
    for key, value in vars(drillVirationDto).items():
        setattr(model, key, value)
    results = model.run_simulation()
    # 处理成相同长度的数组
    for _, v in results.items():
        v = pd.Series(v)
    df = pd.DataFrame(results)

    # 保存excel文件
    # model.save_results(results)

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

@router.post('/drill/mse/optimized')
def get_mse_optimized():
    global mse_cache
    return mse_cache

@router.post('/drill/mse')
def get_mse(mse_DTO : MSEDTO):

    Sk, wob, rop, rpm, MSE, UCS, wob_res, rpm_res, rop_res = mse.calcu_mse(mse_DTO.file_path)
    
    data = {
        "MSE": (MSE),
        "rop": (rop),
        "rpm": (rpm), # 垂深
        "wob": (wob), # 扭矩
        "Sk": (Sk)
    }
    # Creating DataFrame
    df = pd.DataFrame(data)

    if len(UCS) != 0:
        df["UCS"]  = UCS
        mse_cache[wob_res] = wob_res
        mse_cache[rpm_res] = rpm_res
        mse_cache[rop_res] = rop_res

    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()

    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})


    
    


