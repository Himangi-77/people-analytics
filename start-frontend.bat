@echo off
echo 🚀 Starting People Analytics Frontend...

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from example...
    copy .env.example .env
    echo 📝 Please edit frontend\.env if needed
    echo    Default backend URL: http://localhost:8001
)

REM Start the development server
echo 🌟 Starting React development server on http://localhost:3000
echo 🔧 Make sure backend is running on http://localhost:8001
echo.
npm start

pause