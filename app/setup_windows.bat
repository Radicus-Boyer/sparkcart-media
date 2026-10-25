@echo off
rem One-time setup for SparkCart Studio on Windows. Safe to run again.
setlocal
cd /d "%~dp0.."
echo === SparkCart Studio setup ===
python --version >nul 2>nul || (winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements & set NEWPY=1)
where git >nul 2>nul || winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
where ffmpeg >nul 2>nul || winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
echo.
where git >nul 2>nul || set NEWPY=1
where ffmpeg >nul 2>nul || set NEWPY=1
if defined NEWPY (echo Something was just installed. CLOSE this window and run SparkCart-Studio-Install.bat again. & pause & exit /b)
python -m pip install --upgrade pip
python -m pip install numpy pillow onnxruntime kokoro-onnx soundfile num2words tzdata
if not exist app\bin mkdir app\bin
if not exist app\bin\yt-dlp.exe curl -L -o app\bin\yt-dlp.exe https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe
if not exist engine\models mkdir engine\models
if not exist engine\models\kokoro.onnx curl -L -o engine\models\kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
if not exist engine\models\voices.bin curl -L -o engine\models\voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python -c "import kokoro_onnx, num2words, PIL, numpy, soundfile; print('Render engine ready')"
echo.
echo Done. Start the app with: app\SparkCart Studio.bat
pause
