#!/bin/bash

echo "启动AI智能问答系统..."
echo

echo "正在检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到Python，请先安装Python"
    exit 1
fi

echo
echo "正在安装依赖..."
pip3 install -r requirements.txt

echo
echo "启动服务器..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务器"
echo
python3 app.py