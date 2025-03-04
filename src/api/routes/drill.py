# api/routes/hydro.py
from fastapi import Response
import io
from fastapi import APIRouter
from pathlib import Path
import pandas as pd
from entity.DTO import DrillVibrationDTO, MSEDTO

# 创建 APIRouter 实例
router = APIRouter()

# FAST API的全局缓存
hydro_cache = {}

@router.post('/drill/vibration')
def get_limit_hydro(drillViration: DrillVibrationDTO):
    # SSI, t, AngleDisplacements_bit, AngleVelocities_bit, AngleAcceleration_bit, Tb, relativeAngleDisplacements, relativeAngleVelocities = drillVibration_func()

    base_path = Path("D:/petrol-app/mock/drill")

    # 读取前四个文件，假设每个文件有两列：时间和数据
    df_angle_a = pd.read_excel(base_path / "角加速度.xlsx")
    df_angle_x = pd.read_excel(base_path / "角位移.xlsx")
    df_angle_v = pd.read_excel(base_path / "角速度.xlsx")
    df_drill_m = pd.read_excel(base_path / "钻头扭矩.xlsx")

    # 读取第五个文件，假设有两列数据，没有时间列
    df_relative = pd.read_excel(base_path / "钻头粘滑振动相轨迹.xlsx")

    # 提取时间（假设前四个文件的时间列完全一致，以第一个文件为例）
    time = df_angle_a.iloc[:, 0]

    # 提取前四个文件的第二列数据
    angle_a_data = df_angle_a.iloc[:, 1]
    angle_x_data = df_angle_x.iloc[:, 1]
    angle_v_data = df_angle_v.iloc[:, 1]
    drill_m_data = df_drill_m.iloc[:, 1]

    # 假设第五个文件有两列，命名为 relative1 和 relative2
    relativex = df_relative.iloc[:, 0]
    relativey = df_relative.iloc[:, 1]

    # 构造最终的 DataFrame：时间 + 6 列数据
    df = pd.DataFrame({
        'time': time,
        'SSI': 1.35262176582197,
        'angle_a': angle_a_data,
        'angle_x': angle_x_data,
        'angle_v': angle_v_data,
        'drill_m': drill_m_data,
        'relativex': relativex,
        'relativey': relativey
    })

    



    
 


    # 创建 DataFrame
    # df = pd.DataFrame({
    # "t": t.flatten(),  # 时间
    # "AngleDisplacements_bit": AngleDisplacements_bit.flatten(),  # 角位移
    # "AngleVelocities_bit": AngleVelocities_bit.flatten(),  # 角速度
    # "AngleAcceleration_bit": AngleAcceleration_bit.flatten(),  # 角加速度
    # "Tb": Tb.flatten(),  # 钻头扭矩
    # "relativeAngleDisplacements": relativeAngleDisplacements.flatten(),  # 相对角位移
    # "relativeAngleVelocities": relativeAngleVelocities.flatten(),  # 相对角速度
    # "SSI": SSI, # 振动等级
    # })


    


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


@router.post('/drill/mse')
def get_mse(mse_DTO : MSEDTO):
    canshu = pd.read_excel(mse_DTO.file_path).values  
    # MSE, wob, rpm, rop, Depth = mse_func(canshu)

    base_path = Path("D:/petrol-app/mock/drill")
    
        # 读取 Excel 文件
    MSE = pd.read_excel(base_path / "MSE.xlsx").values.flatten()
    rop = pd.read_excel(base_path / "rop.xlsx").values.flatten()

    rpm = pd.read_excel(base_path / "rpm.xlsx").values.flatten()
    Sk = pd.read_excel(base_path / "Sk.xlsx").values.flatten()
    wob = pd.read_excel(base_path / "wob.xlsx").values.flatten()


# Creating a dictionary of Series
    data = {
        "MSE": pd.Series(MSE),
        "rop": pd.Series(rop),
        "rpm": pd.Series(rpm), # 垂深
        "wob": pd.Series(wob), # 扭矩
        "Sk": pd.Series(Sk)
    }
    # Creating DataFrame
    df = pd.DataFrame(data)

    # df = pd.DataFrame({
    #     "MSE": MSE.flatten(),  # 总循环压耗
    #     "wob": wob.flatten(),  # 钻压
    #     "rpm": rpm.flatten(),  # 转速
    #     "rop": rop.flatten(),  # 机械钻速
    #     "Depth": Depth.flatten()  # 井深
    # })
    # # **转换为 CSV 格式**
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8")
    csv_data = output.getvalue()

    return Response(content=csv_data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=torque_data.csv"})


    
    


