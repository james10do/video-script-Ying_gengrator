#!/bin/bash
echo "🎬 正在启动视频脚本生成器..."
source .venv/bin/activate
streamlit run main.py --server.headless true
