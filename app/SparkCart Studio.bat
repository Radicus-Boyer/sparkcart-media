@echo off
title SparkCart Studio
cd /d "%~dp0.."
where python >nul 2>nul || (echo Python is missing. Run app\setup_windows.bat first. & pause & exit /b 1)
python app\server.py
pause
