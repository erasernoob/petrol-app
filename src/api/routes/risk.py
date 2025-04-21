# api/routes/hydro.py
import time
from fastapi import Response
import pandas as pd
import numpy as np
import os
from fastapi import APIRouter
from service import hydra
from service.risk_model import train_main, generate_predict, load_model
from service.risk_result_plot import process_tva_column, analyze_trend
from pathlib import Path
from entity.DTO import ModelPredictDTO, ModelTrainDTO
from service.risk_result_plot import analyze_trend, process_tva_column


router = APIRouter()

risk_cache = {}

# handle the csv and the excel
def read_file(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception:
        df = pd.read_excel(filepath)
        return df
    

def handle_the_filelist(filelist):
    dfs = []

    for path in filelist:
        df = read_file(path)
        dfs.append(df)
    
    df_res = pd.concat(dfs, ignore_index=True)
    print(f"df_res: {df_res}")
    # get the user path
    path = os.path.join(os.environ['USERPROFILE'], 'PETRO_APP_MODEL_TRAIN.xlsx')
    df_res.to_excel(path, index=True)
    return path

@router.post("/risk/train")
async def model_train(dto: ModelTrainDTO):
    # handle the list to be a one single file

    train_path = handle_the_filelist(dto.file_path_list)
    print(f"train_path: {train_path}")
    global risk_cache
    model, test_loader, scaler_y = train_main(train_path, 
               dto.target_file_path, 
               dto.LSTM_nums, 
               dto.LSTM_layers,
               dto.neuron_cnt,
               dto.window_size,
               dto.lr,
               dto.num_epochs
               ) 
    risk_cache = {
        "model": model,
        "test_loader": test_loader,
        "scaler_y": scaler_y,
    }
    return {
        "msg": '模型训练完成'
    }

@router.post("/risk/predict")
async def model_train():
    # 加载模型，并开始出图
    global risk_cache
    model, test_loader, scaler_y = risk_cache.values()
    model = load_model(model)
    print(f"加载之后的模型: {model}")
    
    TVA_res, MAE, RMSE, R  = generate_predict(model, test_loader, scaler_y).values()

    x = [i for i in range(1, len(TVA_res) + 1)]
    # 保存预测结果
    risk_cache["TVA_RES"] = TVA_res.flatten()

    return {
        "x": x,
        "TVA": TVA_res.flatten().tolist(),
        "MAE": MAE, 
        "RMSE": RMSE, 
        "R": R
    }

# 预警结果
@router.post("/risk/warning")
async def model_warning_res():
    global risk_cache
    df =  pd.DataFrame(risk_cache['TVA_RES'], columns='TVA')
    return analyze_trend(process_tva_column(df, show_plot=False))
    


    

    
    
    
