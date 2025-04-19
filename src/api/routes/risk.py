# api/routes/hydro.py
import time
from fastapi import Response
import pandas as pd
import numpy as np
import io
from fastapi import APIRouter
from service import hydra
from pathlib import Path
from entity.DTO import ModelPredictDTO, ModelTrainDTO
from service.risk_result_plot import analyze_trend, process_tva_column


router = APIRouter()

risk_cache = {}

@router.post("/risk/train")
async def model_train(dto: ModelTrainDTO):
    time.sleep(10)
    return {"msg": "训练完成", "code": 200}

@router.post("/risk/upload")
async def model_train():
    return {"msg": "训练完成", "code": 200}



@router.post("/risk/predict")
async def model_train(dto: ModelPredictDTO):
    input_file_path = "D:\\petrol-test\\TVA\\TVA.xlsx"
    data  = analyze_trend(process_tva_column(input_path=input_file_path, show_plot=False))
    return {"data": data}
    # print(data)

@router.post("/risk/warning")
async def model_train():
    input_file_path = "D:\\petrol-test\\TVA\\TVA.xlsx"
    
    df = pd.read_excel(input_file_path)
    x = np.arange(len(df["预测值"]))  # 时间序列
    return {
        "x": x.tolist(),
        "TVA": df["预测值"].tolist(),
        "MAE": 1.7188, 
        "RMSE":2.4487, 
        "R": 0.8753
    }
    


    

    
    
    
