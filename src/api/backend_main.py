# api/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes import hydro, limit, drill, torque, risk   # 导入拆分的路由
from routes import hydro, limit, drill, torque   # 导入拆分的路由

app = FastAPI()

# CORS 配置
origins = [
    "http://localhost:1420",  # Tauri 前端
    "*"  # 生产环境不要用 "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册相关路由
app.include_router(hydro.router)  # 注册 hydro 相关 API
app.include_router(limit.router)  # 注册  相关 API
app.include_router(torque.router)  # 注册 s 相关 API
app.include_router(drill.router)  # 注册 s 相关 API
# app.include_router(risk.router)  # 注册 s 相关 API


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 后端的主程序进入入口
def main():
    uvicorn.run(app, host='127.0.0.1', port=8000,  reload=False)

if __name__ == "__main__":
    main()
    

    

