@echo off
chcp 65001 >nul
echo.
echo   🎬 视频脚本生成器 - 启动中...
echo   -----------------------------------
echo.
call .venv\Scripts\Activate.ps1
streamlit run main.py --server.headless true
