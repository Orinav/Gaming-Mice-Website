@echo off
echo Starting Mouse Catalog Project...

cd /d "%~dp0"
:: 1. Fetch data from the API first USING THE VIRTUAL ENVIRONMENT
echo Fetching latest mice data from the API... Please wait
cd backend
call ..\.venv\Scripts\python.exe api_client.py
cd ..

:: 2. Start Flask Server in a new window USING THE VIRTUAL ENVIRONMENT
echo Starting Backend Server...
start "Flask Backend" cmd /k "cd backend && ..\.venv\Scripts\python.exe app.py"

:: 3. Start Vue Frontend in another new window
echo Starting Frontend...
start "Vue Frontend" cmd /k "cd frontend && npm run dev"

echo All processes started successfully!