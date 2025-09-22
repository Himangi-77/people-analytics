#!/bin/bash

echo "🚀 Starting People Analytics Frontend..."

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "📝 Please edit frontend/.env if needed"
    echo "   Default backend URL: http://localhost:8001"
fi

# Start the development server
echo "🌟 Starting React development server on http://localhost:3000"
echo "🔧 Make sure backend is running on http://localhost:8001"
echo ""
npm start