@echo off
title NexusCareer AI Copilot - Start Services

echo ========================================================
echo   NexusCareer AI Copilot (HACKHAZARDS '26)
echo   Explainable AI Career Copilot
echo ========================================================
echo.

echo [1/2] Starting FastAPI Backend Engine...
cd backend
start "NexusCareer Backend" cmd /k "python main.py"
cd ..

echo [2/2] Starting React Frontend Interface...
cd frontend
start "NexusCareer Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo   All systems nominal!
echo   Frontend running at: http://localhost:5173
echo   Backend running at:  http://localhost:8000
echo ========================================================
echo You can now minimize this window.
pause
