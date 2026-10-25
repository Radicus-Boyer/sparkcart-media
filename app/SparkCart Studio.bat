@echo off
title SparkCart Studio
cd /d "%~dp0.."
call app\findpy.bat
if not defined PY (echo Python is missing. Run SparkCart-Studio-Install.bat first. & pause & exit /b 1)
%PY% app\server.py
pause
