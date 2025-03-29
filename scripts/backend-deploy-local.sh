#!/bin/bash
cd src/api

# 清理旧构建
rm -rf build/ dist/

# 安装依赖
source venv/Scripts/activate

# 打包命令
pyinstaller --onefile --name backend \
  --hidden-import=routes \
  --hidden-import=entity \
  --hidden-import=service \
  --paths="." \
  --add-data="routes:routes" \
  --add-data="entity:entity" \
  --add-data="service:service" \
  backend_main.py

# 处理不同平台的可执行文件后缀
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    EXECUTABLE="backend.exe"
else
    EXECUTABLE="backend"
fi

# 移动可执行文件
cp dist/$EXECUTABLE ../../src-tauri/bin/

deactivate
# rm -rf venv/ build/ dist/