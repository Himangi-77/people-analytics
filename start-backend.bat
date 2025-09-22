@echo off
echo 🚀 Starting People Analytics Backend...

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from example...
    copy .env.example .env
    echo 📝 Please edit backend\.env with your configuration
    echo    Required: EMERGENT_LLM_KEY (OpenAI API key)
    echo    Optional: MONGO_URL (defaults to local MongoDB)
)

REM Start the server
echo 🌟 Starting FastAPI server on http://localhost:8001
echo 📚 API Documentation: http://localhost:8001/docs
echo.
uvicorn server:app --reload --host 0.0.0.0 --port 8001

pause