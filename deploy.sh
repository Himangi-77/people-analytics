#!/bin/bash

echo "🚀 People Analytics App - Deployment Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: People Analytics App"
    git branch -M main
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository already exists${NC}"
fi

echo ""
echo -e "${BLUE}📋 Deployment Checklist:${NC}"
echo ""
echo "1. 🗄️  Setup MongoDB Atlas:"
echo "   → https://www.mongodb.com/cloud/atlas"
echo "   → Create free cluster (512MB)"
echo "   → Get connection string"
echo ""
echo "2. 🔑 Get OpenAI API Key:"
echo "   → https://platform.openai.com/api-keys"
echo "   → Create new API key"
echo ""
echo "3. 🔥 Deploy Backend to Railway:"
echo "   → https://railway.app"
echo "   → New Project → Deploy from GitHub"
echo "   → Root Directory: backend"
echo "   → Add environment variables:"
echo "     MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/people_analytics"
echo "     DB_NAME=people_analytics"
echo "     CORS_ORIGINS=https://your-frontend.vercel.app"
echo "     EMERGENT_LLM_KEY=your-openai-key"
echo ""
echo "4. 🌐 Deploy Frontend to Vercel:"
echo "   → https://vercel.com"
echo "   → New Project → Import from GitHub"
echo "   → Root Directory: frontend"
echo "   → Add environment variable:"
echo "     REACT_APP_BACKEND_URL=https://your-backend.railway.app"
echo ""
echo "5. 🔄 Update CORS after frontend deployment"
echo ""

# Create GitHub remote setup
echo -e "${YELLOW}To push to GitHub:${NC}"
echo "git remote add origin https://github.com/yourusername/people-analytics.git"
echo "git push -u origin main"
echo ""

# Environment check
echo -e "${BLUE}📂 Current structure:${NC}"
ls -la | grep -E "(backend|frontend|README|DEPLOYMENT)"

echo ""
echo -e "${GREEN}🎉 Setup complete! Follow the deployment guide in DEPLOYMENT.md${NC}"
echo ""
echo -e "${YELLOW}💡 Quick Links:${NC}"
echo "   📖 Deployment Guide: ./DEPLOYMENT.md"
echo "   🔗 MongoDB Atlas: https://www.mongodb.com/cloud/atlas"
echo "   🔗 Railway: https://railway.app"
echo "   🔗 Vercel: https://vercel.com"
echo "   🔗 OpenAI: https://platform.openai.com/api-keys"