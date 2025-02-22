# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import hydro   # 导入拆分的路由

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadFile")
async def get_uploaded_file():
    return {"message": "File uploaded successfully"}
