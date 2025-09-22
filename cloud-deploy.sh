#!/bin/bash

echo "☁️ People Analytics App - Cloud Deployment Setup"
echo "================================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Preparing for cloud deployment...${NC}"

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "People Analytics App - Ready for cloud deployment"
    git branch -M main
    echo -e "${GREEN}✅ Git repository created${NC}"
else
    echo -e "${GREEN}✅ Git repository exists${NC}"
fi

# Check if files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}📝 Committing latest changes...${NC}"
    git add .
    git commit -m "Latest updates for cloud deployment"
fi

echo ""
echo -e "${BLUE}📋 Deployment Checklist:${NC}"
echo ""
echo "1. 🗄️  **MongoDB Atlas Setup** (2 minutes):"
echo "   → https://cloud.mongodb.com"
echo "   → Create free cluster (512MB)"
echo "   → Add database user with password"
echo "   → Network access: Allow 0.0.0.0/0"
echo "   → Get connection string"
echo ""
echo "2. 🔥 **Deploy Backend to Render** (5 minutes):"
echo "   → https://render.com"
echo "   → New Web Service → Connect GitHub"
echo "   → Root Directory: backend"
echo "   → Build: pip install -r requirements.txt"
echo "   → Start: uvicorn server:app --host 0.0.0.0 --port \$PORT"
echo "   → Environment variables:"
echo "     PYTHON_VERSION=3.9.18"
echo "     MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/people_analytics"
echo "     DB_NAME=people_analytics"
echo "     CORS_ORIGINS=*"
echo "     EMERGENT_LLM_KEY=sk-your-openai-key"
echo ""
echo "3. 🌐 **Deploy Frontend to Vercel** (3 minutes):"
echo "   → https://vercel.com"
echo "   → Import Project → GitHub → Your repo"
echo "   → Root Directory: frontend"
echo "   → Environment variable:"
echo "     REACT_APP_BACKEND_URL=https://your-backend.onrender.com"
echo ""
echo "4. 🔄 **Update CORS** (1 minute):"
echo "   → Go back to Render → Environment variables"
echo "   → Update CORS_ORIGINS=https://your-frontend.vercel.app"
echo ""
echo "5. 🧪 **Test Deployment**:"
echo "   → Upload sample-data.json"
echo "   → Ask sample questions"
echo "   → Verify AI analysis works"
echo ""

# Check for required files
missing_files=()

if [ ! -f "backend/requirements.txt" ]; then
    missing_files+=("backend/requirements.txt")
fi

if [ ! -f "backend/Dockerfile" ]; then
    missing_files+=("backend/Dockerfile")
fi

if [ ! -f "backend/render.yaml" ]; then
    missing_files+=("backend/render.yaml")
fi

if [ ! -f "frontend/package.json" ]; then
    missing_files+=("frontend/package.json")
fi

if [ ! -f "frontend/vercel.json" ]; then
    missing_files+=("frontend/vercel.json")
fi

if [ ${#missing_files[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ All deployment files present${NC}"
else
    echo -e "${RED}❌ Missing files: ${missing_files[*]}${NC}"
fi

echo ""
echo -e "${BLUE}🔗 Platform URLs:${NC}"
echo "   🔥 Render (Backend): https://render.com"
echo "   🌐 Vercel (Frontend): https://vercel.com"
echo "   🗄️  MongoDB Atlas: https://cloud.mongodb.com"
echo "   🔑 OpenAI API Keys: https://platform.openai.com/api-keys"
echo ""

echo -e "${BLUE}📚 Documentation:${NC}"
echo "   📖 Step-by-step guide: ./CLOUD_DEPLOYMENT.md"
echo "   🔥 Render specific: ./render-deploy.md"
echo "   ✈️  Fly.io alternative: ./fly-deploy.md"
echo "   ☁️  All alternatives: ./cloud-alternatives.md"
echo ""

echo -e "${YELLOW}💡 Quick Tips:${NC}"
echo "   • Use Render for backend (best FastAPI support)"
echo "   • Use Vercel for frontend (best React support)"
echo "   • MongoDB Atlas has 512MB free tier"
echo "   • Get OpenAI API key for AI features"
echo "   • Total cost: \$0/month for development!"
echo ""

if [ ! -z "$(git remote -v)" ]; then
    echo -e "${GREEN}✅ Ready to deploy! Push to GitHub and follow the guide.${NC}"
else
    echo -e "${YELLOW}📝 Next: Add GitHub remote and push:${NC}"
    echo "   git remote add origin https://github.com/yourusername/people-analytics.git"
    echo "   git push -u origin main"
fi

echo ""
echo -e "${GREEN}🎉 Cloud deployment setup complete!${NC}"
echo -e "${BLUE}Follow CLOUD_DEPLOYMENT.md for detailed instructions.${NC}"