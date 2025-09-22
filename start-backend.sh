#!/bin/bash

echo "🚀 Starting People Analytics Backend..."

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "📝 Please edit backend/.env with your configuration"
    echo "   Required: EMERGENT_LLM_KEY (OpenAI API key)"
    echo "   Optional: MONGO_URL (defaults to local MongoDB)"
fi

# Start the server
echo "🌟 Starting FastAPI server on http://localhost:8001"
echo "📚 API Documentation: http://localhost:8001/docs"
echo ""
uvicorn server:app --reload --host 0.0.0.0 --port 8001