@echo off
title Eshara System Launcher
echo ====================================================
echo      ESHARA - REAL-TIME SIGN LANGUAGE SYSTEM
echo ====================================================
echo.
echo Starting the three-tier web architecture...
echo.

:: 1. Start the Node.js/Express Backend API
echo [1/3] Starting Backend (Node.js/Express)...
start "Eshara Backend API" cmd /k "cd backend && npm run dev"

:: 2. Start the FastAPI Model Services
echo [2/3] Starting Model Services (FastAPI)...
start "Eshara Model Services" cmd /k "cd model-services && uvicorn app:app --reload --port 8000"

:: 3. Start the React/Vite Frontend
echo [3/3] Starting Frontend UI (React)...
start "Eshara Frontend UI" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo All three services have been launched in separate windows!
echo - Frontend running at: http://localhost:5173
echo - Backend API running at: http://localhost:3000
echo - Model Services running at: http://localhost:8000
echo ====================================================
pause
