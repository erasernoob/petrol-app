from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.server.entity.DTO import Hydro

app = FastAPI()
origins = [
    # "http://localhost:5173",  # Vite 开发服务器默认端口
    "http://localhost:1420",  # Tauri 开发时的前端端口
    "*"  # ⚠️ 不推荐在生产环境中使用 "*"，建议指定域名
]
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的来源
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有请求方法（GET, POST, PUT, DELETE, etc.）
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadFile")
async def getUploadedFile():
    return {"message": "Hello World"}



# hydro---------------------------------------------

@app.post("/hydro")
async def getHydroParams(data : Hydro):
    print(data)
