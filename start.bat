@echo off
setlocal EnableExtensions
chcp 65001 >nul
title 雅思阅读精读器
cd /d "%~dp0"

set "PORT=8000"
if defined IELTS_PORT set "PORT=%IELTS_PORT%"
set "APP_URL=http://127.0.0.1:%PORT%/index.html"

echo.
echo  ========================================
echo          雅思阅读精读器 · 一键启动
echo  ========================================
echo.

rem 查找 Python；使用 goto 避免 Windows 批处理嵌套括号兼容问题。
where py >nul 2>nul
if errorlevel 1 goto TRY_PYTHON
set "PYTHON_CMD=py -3"
goto PYTHON_OK

:TRY_PYTHON
where python >nul 2>nul
if errorlevel 1 goto NO_PYTHON
set "PYTHON_CMD=python"
goto PYTHON_OK

:NO_PYTHON
echo [启动失败] 没有找到 Python。
echo 请先安装 Python 3，并在安装时勾选“Add Python to PATH”。
echo.
pause
exit /b 1

:PYTHON_OK
rem 优先查找 Chrome，避免 Edge 原生朗读兼容问题。
set "CHROME="
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not defined CHROME if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "CHROME=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined CHROME if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set "CHROME=%LocalAppData%\Google\Chrome\Application\chrome.exe"

rem 已经启动时只打开页面，不重复占用端口。
powershell -NoProfile -Command "try { $c = New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1', %PORT%); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>nul
if errorlevel 1 goto START_SERVER

echo [提示] 阅读器已经在运行，正在打开页面……
if defined CHROME goto OPEN_EXISTING_CHROME
echo [提示] 未找到 Chrome，改用系统默认浏览器。
start "" "%APP_URL%"
exit /b 0

:OPEN_EXISTING_CHROME
start "" "%CHROME%" "%APP_URL%"
exit /b 0

:START_SERVER
echo [1/2] 正在启动本地服务：http://127.0.0.1:%PORT%
if defined IELTS_SKIP_BROWSER goto RUN_SERVER
if defined CHROME goto DELAY_OPEN_CHROME
echo [2/2] 未找到 Chrome，将使用系统默认浏览器……
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 1; Start-Process '%APP_URL%'"
goto RUN_SERVER

:DELAY_OPEN_CHROME
echo [2/2] 将使用 Google Chrome 打开阅读器……
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 1; Start-Process -FilePath '%CHROME%' -ArgumentList '%APP_URL%'"

:RUN_SERVER
echo.
echo 阅读器运行期间请保留本窗口。
echo 关闭本窗口后，本地服务随之停止；文章和生词数据不会因此被删除。
echo.
%PYTHON_CMD% -m http.server %PORT% --bind 127.0.0.1
echo.
echo 本地服务已停止。
pause
