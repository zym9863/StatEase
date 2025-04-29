@echo off
echo StatEase - 简易统计分析工具启动脚本
echo ====================================

REM 检查是否存在虚拟环境
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成
)

REM 激活虚拟环境并安装依赖
echo 激活虚拟环境...
call venv\Scripts\activate

echo 安装依赖...
pip install -r requirements.txt

echo 启动应用...
python app.py

pause