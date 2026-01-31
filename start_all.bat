@echo off
chcp 65001 > nul

:: 设置项目根目录
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: 显示启动信息
echo =========================================
echo         智能垃圾分类识别系统
 echo =========================================
echo 正在准备启动服务...
echo 项目根目录: %PROJECT_ROOT%
echo =

:: 检查Python是否安装
echo 检查Python环境...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境，请先安装Python
    echo 建议安装Python 3.8或更高版本
    pause
    exit /b 1
)
echo ✅ Python环境检测成功

:: 检查依赖包
echo 检查必要的依赖包...
pip show streamlit > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装streamlit包，尝试安装...
    pip install streamlit > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装streamlit失败
        pause
        exit /b 1
    )
)

pip show flask > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装flask包，尝试安装...
    pip install flask > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装flask失败
        pause
        exit /b 1
    )
)

pip show flask_cors > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装flask_cors包，尝试安装...
    pip install flask_cors > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装flask_cors失败
        pause
        exit /b 1
    )
)

pip show torch > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装torch包，尝试安装...
    pip install torch > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装torch失败
        pause
        exit /b 1
    )
)

pip show torchvision > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装torchvision包，尝试安装...
    pip install torchvision > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装torchvision失败
        pause
        exit /b 1
    )
)

pip show Pillow > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装Pillow包，尝试安装...
    pip install Pillow > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装Pillow失败
        pause
        exit /b 1
    )
)

pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未安装requests包，尝试安装...
    pip install requests > nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 安装requests失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖包检查完成

:: 检查必要文件
echo 检查项目文件...
if not exist "%PROJECT_ROOT%\garbage_classify_app01.py" (
    echo 错误: 未找到Streamlit前端文件 garbage_classify_app01.py
    pause
    exit /b 1
)
if not exist "%PROJECT_ROOT%\web.py" (
    echo 错误: 未找到Flask后端文件 web.py
    pause
    exit /b 1
)
if not exist "%PROJECT_ROOT%\model\model_01.pt" (
    echo 错误: 未找到模型文件 model\model_01.pt
    pause
    exit /b 1
)
echo ✅ 项目文件检查完成

:: 启动后端服务
echo 正在启动Flask后端服务...
start "Flask后端服务" cmd /k "cd /d "%PROJECT_ROOT%" && echo 启动Flask后端服务... && python web.py"

:: 等待2秒，确保后端服务有足够时间启动
timeout /t 2 /nobreak > nul

:: 启动前端服务
echo 正在启动Streamlit前端应用...
start "Streamlit前端应用" cmd /k "cd /d "%PROJECT_ROOT%" && echo 启动Streamlit前端应用... && streamlit run garbage_classify_app01.py"

:: 显示启动完成信息
echo =
echo =========================================
echo 服务启动完成！
echo =========================================
echo 🚀 后端服务: http://localhost:8080
 echo 🎯 前端应用: 请查看Streamlit终端窗口中的URL
 echo =
echo 提示:
echo 1. 两个终端窗口已自动打开
 echo 2. 请确保两个服务都正常启动
 echo 3. 如果遇到启动失败，请查看终端窗口中的错误信息
 echo 4. 关闭服务时，请直接关闭对应的终端窗口
 echo =
echo 按任意键退出此窗口...
pause > nul
exit /b 0