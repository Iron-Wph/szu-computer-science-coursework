@echo off
echo 启动AI智能问答系统...
echo.

echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 正在检查配置...
python test_config.py
if errorlevel 1 (
    echo.
    echo 配置检查失败，请先配置环境变量
    echo 参考 config_setup.md 文件进行配置
    pause
    exit /b 1
)

echo.
echo 正在安装依赖...
pip install -r requirements.txt

echo.
echo 启动服务器...
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
python app.py

pause