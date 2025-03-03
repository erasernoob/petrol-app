# api/routes/hydro.py
from fastapi import Response
import io
from fastapi import APIRouter
import pandas as pd
from entity.DTO import DrillVibrationDTO, MSEDTO

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
hydro_cache = {}

@router.get('/drill/vibration')
def get_limit_hydro(drillViration: DrillVibrationDTO):
    SSI, t, AngleDisplacements_bit, AngleVelocities_bit, AngleAcceleration_bit, Tb, relativeAngleDisplacements, relativeAngleVelocities = drillVibration_func()


    # 创建 DataFrame
    df = pd.DataFrame({
    "t": t.flatten(),  # 时间
    "AngleDisplacements_bit": AngleDisplacements_bit.flatten(),  # 角位移
    "AngleVelocities_bit": AngleVelocities_bit.flatten(),  # 角速度
    "AngleAcceleration_bit": AngleAcceleration_bit.flatten(),  # 角加速度
    "Tb": Tb.flatten(),  # 钻头扭矩
    "relativeAngleDisplacements": relativeAngleDisplacements.flatten(),  # 相对角位移
    "relativeAngleVelocities": relativeAngleVelocities.flatten(),  # 相对角速度
    "SSI": SSI, # 振动等级
    })

    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()
    
    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})

def drillVibration_func():
    return

def mse_func():
    return


@router.get('/drill/mse')
def get_mse(mse_DTO : MSEDTO):
    canshu = pd.read_excel(mse_DTO.file_path).values  
    MSE, wob, rpm, rop, Depth = mse_func(canshu)
    df = pd.DataFrame({
        "MSE": MSE.flatten(),  # 总循环压耗
        "wob": wob.flatten(),  # 钻压
        "rpm": rpm.flatten(),  # 转速
        "rop": rop.flatten(),  # 机械钻速
        "Depth": Depth.flatten()  # 井深
    })
    # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()

    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})


    
    


