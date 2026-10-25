@echo off
title SparkCart Studio
cd /d "%~dp0.."
call app\findpy.bat
if not defined PY (echo Python is missing. Run SparkCart-Studio-Install.bat first. & pause & exit /b 1)
rem Close any older copy of the app that is still running in the background
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8765" ^| findstr LISTENING') do taskkill /PID %%p /F >nul 2>nul
set "ARGS="
:run
%PY% app\server.py %ARGS%
if "%errorlevel%"=="3" (set "ARGS=--no-open" & goto run)
pause
