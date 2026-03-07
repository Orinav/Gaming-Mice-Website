@echo off
echo Starting Mouse Catalog Project...

:: 1. Run the Scraper first USING THE VIRTUAL ENVIRONMENT
echo Running Scraper (Downloading latest mice data... Please wait)
cd backend
call ..\.venv\Scripts\python.exe scraper.py
cd ..

:: 2. Start Flask Server in a new window USING THE VIRTUAL ENVIRONMENT
echo Starting Backend Server...
start "Flask Backend" cmd /k "cd backend && ..\.venv\Scripts\python.exe app.py"

:: 3. Start Vue Frontend in another new window
echo Starting Frontend...
start "Vue Frontend" cmd /k "cd frontend && npm run dev"

echo All processes started successfully!