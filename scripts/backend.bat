@echo off
cd /d "%~dp0\..\src\api"

REM 清理旧构建
rmdir /s /q build dist

REM 安装依赖
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
pip install pyinstaller

REM 打包命令
pyinstaller --onefile --name backend ^
  --hidden-import=routes ^
  --hidden-import=entity ^
  --hidden-import=service ^
  --paths="." ^
  --add-data="routes;routes" ^
  --add-data="entity;entity" ^
  --add-data="service;service" ^
  backend_main.py

REM 处理不同平台的可执行文件后缀
set EXECUTABLE=backend.exe

REM 移动可执行文件
if not exist ..\..\src-tauri\bin mkdir ..\..\src-tauri\bin
move /y dist\%EXECUTABLE% ..\..\src-tauri\bin\


REM 验证是否成功移动
if exist "..\..\src-tauri\bin\%EXECUTABLE%" (
    echo %EXECUTABLE%
    echo  backend.exe moved successfully!
) else (
    echo  ERROR: backend.exe not found! Build failed.
    exit /b 1
)

@REM deactivate
@REM REM rmdir /s /q venv build dist
