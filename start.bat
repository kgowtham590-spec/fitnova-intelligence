@echo off
title FitNova AI Sales Call Intelligence
color 0A

echo ========================================
echo    FitNova AI Sales Call Intelligence
echo ========================================
echo.

REM -------------------------------------------------
REM Check Python 3.11
REM -------------------------------------------------
set PY=C:\Users\kgowt\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PY%" (
    echo ERROR: Python 3.11 not found.
    echo Please install Python 3.11.
    pause
    exit /b 1
)

REM -------------------------------------------------
REM Check Node.js
REM -------------------------------------------------
where npm >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js is not installed.
    pause
    exit /b 1
)

echo [1/3] Starting Backend...

start "FitNova Backend" cmd /k "cd /d %~dp0backend && %PY% -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Waiting for backend...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Starting Frontend...

start "FitNova Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Waiting for frontend...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Opening Browser...

start http://localhost:3000

echo.
echo ========================================
echo  FitNova is now running!
echo.
echo  Frontend:
echo      http://localhost:3000
echo.
echo  Backend:
echo      http://127.0.0.1:8000
echo.
echo  API Docs:
echo      http://127.0.0.1:8000/api/v1/docs
echo ========================================
echo.
echo Close the Backend and Frontend windows to stop the application.
exit