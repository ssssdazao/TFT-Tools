@echo off
cd /d "%~dp0TFT_Tool"

echo ===================================================
echo 正在使用 Anaconda 环境安装依赖...
echo Python 路径: f:\geren\anaconda\python.exe
echo ===================================================

"f:\geren\anaconda\python.exe" -m pip install -r requirements.txt

echo.
echo ===================================================
echo 依赖安装完成，正在启动云顶之弈分析工具...
echo ===================================================

"f:\geren\anaconda\python.exe" -m streamlit run main.py

pause
