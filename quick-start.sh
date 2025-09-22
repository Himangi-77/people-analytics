#!/bin/bash

echo "🚀 People Analytics App - Quick Local Setup"
echo "==========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
else
    echo -e "${RED}❌ Python 3.9+ required. Download from https://python.org${NC}"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"
else
    echo -e "${RED}❌ Node.js 16+ required. Download from https://nodejs.org${NC}"
    exit 1
fi

# Check if MongoDB is running (optional)
if command -v mongosh &> /dev/null || command -v mongo &> /dev/null; then
    echo -e "${GREEN}✅ MongoDB CLI found${NC}"
else
    echo -e "${YELLOW}⚠️  MongoDB CLI not found. You can use MongoDB Atlas instead.${NC}"
fi

echo ""
echo -e "${BLUE}🔧 Setting up environment files...${NC}"

# Setup backend .env
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✅ Created backend/.env${NC}"
    echo -e "${YELLOW}📝 Please edit backend/.env and add your OpenAI API key${NC}"
else
    echo -e "${GREEN}✅ Backend .env already exists${NC}"
fi

# Setup frontend .env
if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✅ Created frontend/.env${NC}"
else
    echo -e "${GREEN}✅ Frontend .env already exists${NC}"
fi

echo ""
echo -e "${BLUE}📦 Setting up backend...${NC}"

# Backend setup
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
cd ..

echo -e "${GREEN}✅ Backend setup complete${NC}"

echo ""
echo -e "${BLUE}📦 Setting up frontend...${NC}"

# Frontend setup
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install -q
fi
cd ..

echo -e "${GREEN}✅ Frontend setup complete${NC}"

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${BLUE}📚 Next steps:${NC}"
echo "1. 🔑 Add your OpenAI API key to backend/.env:"
echo "   EMERGENT_LLM_KEY=sk-your-api-key-here"
echo ""
echo "2. 🚀 Start the application:"
echo "   Terminal 1: ./start-backend.sh"
echo "   Terminal 2: ./start-frontend.sh"
echo ""
echo "3. 🌐 Open in browser:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001/docs"
echo ""
echo "4. 📊 Test with sample data:"
echo "   Upload sample-data.json in the app"
echo ""
echo -e "${YELLOW}💡 Tip: Read LOCAL_SETUP.md for detailed instructions${NC}"
echo ""

# Make start scripts executable
chmod +x start-backend.sh start-frontend.sh

echo -e "${GREEN}Ready to launch! 🚀${NC}"