@echo off
title SparkCart Studio
cd /d "%~dp0.."
call app\findpy.bat
if not defined PY (echo Python is missing. Run SparkCart-Studio-Install.bat first. & pause & exit /b 1)
set "ARGS="
:run
%PY% app\server.py %ARGS%
if "%errorlevel%"=="3" (set "ARGS=--no-open" & goto run)
pause
