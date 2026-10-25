@echo off
rem Sets PY to a real python.exe (ignores the Windows Store stub) and adds winget tools to PATH.
set "PATH=%LocalAppData%\Microsoft\WinGet\Links;%ProgramFiles%\Git\cmd;%PATH%"
for /d %%D in ("%LocalAppData%\Microsoft\WinGet\Packages\Gyan.FFmpeg*") do for /d %%E in ("%%D\ffmpeg-*") do set "PATH=%%E\bin;%PATH%"
set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do if exist "%%D\python.exe" set "PY=%%D\python.exe"
if not defined PY for /d %%D in ("%ProgramFiles%\Python3*") do if exist "%%D\python.exe" set "PY=%%D\python.exe"
if not defined PY python --version >nul 2>nul && set "PY=python"
