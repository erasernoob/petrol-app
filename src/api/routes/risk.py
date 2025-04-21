# api/routes/hydro.py
import time
from fastapi import Response, UploadFile, File, HTTPException
import pandas as pd
import numpy as np
import os
from io import BytesIO
from fastapi import APIRouter
from service import hydra
from service.risk_model import train_main, generate_predict, load_model
from service.risk_result_plot import process_tva_column, analyze_trend
from pathlib import Path
from entity.DTO import ModelPredictDTO, ModelTrainDTO
from service.risk_result_plot import analyze_trend, process_tva_column


router = APIRouter()

risk_cache = {}
file_list = []

# 最终集合成一个文件的path
FINAL_FILE_PATH = os.path.join(os.environ['USERPROFILE'], 'PETRO_APP_MODEL_TRAIN.xlsx')
REQUIRED_COLUMNS = ['TVA','WOBA', 'ROPA', 'TQA', 'RPMA']

@router.post("/risk/upload")
async def upload_file(file: UploadFile = File(...)):
    global file_list
    file_content = await file.read()

    df = read_file(file=BytesIO(file_content))
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise HTTPException(status_code=503, detail="上传的历史样本集格式错误,请重新上传！")

    file_list.append(BytesIO(file_content))

    return {"msg": "upload successfully"}

# handle the csv and the excel
def read_file(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception:
        df = pd.read_excel(file)
        return df
    

def handle_the_filelist(filelist):
    dfs = []

    for path in filelist:
        df = read_file(path)
        dfs.append(df)
    
    df_res = pd.concat(dfs, ignore_index=True)
    print(f"df_res: {df_res}")
    # get the user path
    path = os.path.join(FINAL_FILE_PATH)
    df_res.to_excel(path, index=True)
    return path

@router.post("/risk/train")
async def model_train(dto: ModelTrainDTO):
    # handle the list to be a one single file
    global file_list

    try:
        train_path = handle_the_filelist(file_list)
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
    except Exception as e:
        # 清除FILELIS
        if os.path.exists(FINAL_FILE_PATH):
            os.remove(FINAL_FILE_PATH)
        raise HTTPException(status_code=500, detail=f"模型训练失败: {str(e)}")

    if os.path.exists(FINAL_FILE_PATH):
       os.remove(FINAL_FILE_PATH)

    return {
        "msg": '模型训练完成'
    }

@router.post("/risk/predict")
async def model_train():
    global risk_cache
    try:
        model, test_loader, scaler_y = risk_cache.values()
        model = load_model(model)
        print(f"加载之后的模型: {model}")
        
        TVA_res, MAE, RMSE, R  = generate_predict(model, test_loader, scaler_y).values()

        x = [i for i in range(1, len(TVA_res) + 1)]
        # 保存预测结果
        risk_cache["TVA_RES"] = TVA_res.flatten()
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

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
#    return {
#   "x": [0, 1, 2, 3, 4, 5, 6],
#   "tva_data": [58.87, 58.86, 58.88, 58.91, 58.85, 58.83, 58.82],
#   "peaks": [3],
#   "valleys": [5],
#   "danger_zones": [
#     {
#       "start": 2,
#       "end": 4,
#       "level": "high",
#       "color": "#ff4d4f",
#       "threshold": 58.9
#     },
#     {
#       "start": 5,
#       "end": 6,
#       "level": "medium",
#       "color": "#faad14",
#       "threshold": 58.84
#     }
#   ]
# }
    global risk_cache
    

    if risk_cache.get('TVA_RES') is None:
        risk_cache =  {}
        file_list = {}
        raise HTTPException(status_code=403, detail="没有预测数据，请再次训练模型！")
    target = risk_cache.get('TVA_RES')
    print(target)
    print(type(target))
    df = pd.DataFrame([[v] for v in target], columns=["TVA"])
    
    return analyze_trend(process_tva_column(df, show_plot=False))
    


    

    
    
    
