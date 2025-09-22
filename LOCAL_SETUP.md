# 🖥️ Local Development Setup Guide

## 📋 Prerequisites

### Required Software
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/)

### Database Options
**Option A: MongoDB Atlas (Recommended)**
- Free cloud database (no local installation needed)

**Option B: Local MongoDB**
- [MongoDB Community Edition](https://www.mongodb.com/try/download/community)

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd people-analytics
```

### 2. Backend Setup (Terminal 1)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings (see below)

# Start backend server
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### 3. Frontend Setup (Terminal 2)
```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create environment file
cp .env.example .env
# Edit .env with backend URL (see below)

# Start frontend development server
npm start
# or 
yarn start
```

### 4. Open Your Browser
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8001/docs

---

## 🔧 Environment Configuration

### Backend Environment (.env)
Create `/backend/.env`:
```bash
# Database
MONGO_URL=mongodb://localhost:27017
# OR for MongoDB Atlas:
# MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics

DB_NAME=people_analytics

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000

# OpenAI API Key (required for AI analysis)
EMERGENT_LLM_KEY=sk-your-openai-api-key-here
# Get key at: https://platform.openai.com/api-keys

# Optional: Emergent LLM Key (if you have access)
# EMERGENT_LLM_KEY=sk-emergent-your-key-here
```

### Frontend Environment (.env)
Create `/frontend/.env`:
```bash
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🗄️ Database Setup Options

### Option A: MongoDB Atlas (Cloud - Recommended)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free account
3. Create new cluster (free tier: 512MB)
4. Create database user
5. Get connection string
6. Add to backend `.env`:
   ```bash
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics
   ```

### Option B: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # Windows (as service)
   net start MongoDB
   
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```
3. Use in backend `.env`:
   ```bash
   MONGO_URL=mongodb://localhost:27017
   ```

---

## 🔑 API Keys Setup

### OpenAI API Key (Required for AI Analysis)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account / Sign in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to backend `.env`:
   ```bash
   EMERGENT_LLM_KEY=sk-your-actual-key-here
   ```

**Note**: You'll need billing set up on OpenAI for API usage beyond free credits.

---

## 🏃‍♂️ Running the Application

### Method 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Method 2: Using Scripts

Create these helper scripts in your root directory:

**`start-backend.sh` (macOS/Linux):**
```bash
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**`start-backend.bat` (Windows):**
```batch
@echo off
cd backend
call venv\Scripts\activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**`start-frontend.sh` (macOS/Linux):**
```bash
#!/bin/bash
cd frontend
npm start
```

Make executable:
```bash
chmod +x start-backend.sh start-frontend.sh
```

---

## 🧪 Testing Your Setup

### 1. Check Backend Health
- Visit: http://localhost:8001
- Should see: `{"message": "People Analytics API is running"}`
- API Docs: http://localhost:8001/docs

### 2. Check Frontend
- Visit: http://localhost:3000
- Should see: People Analytics dashboard

### 3. Test Full Integration
1. **Upload Graph Data**: Click "Upload Graph" button
2. **Ask Question**: Select a sample question or type your own
3. **View Results**: Should see AI analysis and graph visualization

---

## 📊 Sample Data for Testing

Create a test file `sample-graph.json`:
```json
{
  "nodes": [
    {"data": {"id": "1", "full_name": "Alice Johnson", "department": "Engineering", "designation": "Tech Lead"}},
    {"data": {"id": "2", "full_name": "Bob Smith", "department": "Marketing", "designation": "Marketing Manager"}},
    {"data": {"id": "3", "full_name": "Carol Brown", "department": "Sales", "designation": "Sales Director"}},
    {"data": {"id": "4", "full_name": "David Wilson", "department": "HR", "designation": "HR Manager"}}
  ],
  "edges": [
    {"data": {"source": "1", "target": "2", "weight": 0.8}},
    {"data": {"source": "2", "target": "3", "weight": 0.6}},
    {"data": {"source": "3", "target": "4", "weight": 0.7}},
    {"data": {"source": "1", "target": "4", "weight": 0.5}}
  ]
}
```

Upload this file to test the application functionality.

---

## 🔧 Troubleshooting

### Common Issues

**Backend Won't Start:**
```bash
# Check Python version
python --version  # Should be 3.9+

# Check if virtual environment is activated
which python  # Should point to venv

# Install missing dependencies
pip install -r requirements.txt

# Check for port conflicts
lsof -i :8001  # macOS/Linux
netstat -an | findstr :8001  # Windows
```

**Frontend Won't Start:**
```bash
# Check Node version
node --version  # Should be 16+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -i :3000  # macOS/Linux
netstat -an | findstr :3000  # Windows
```

**Database Connection Errors:**
```bash
# Local MongoDB not running
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
net start MongoDB  # Windows

# Check MongoDB Atlas connection
# Verify username/password in connection string
# Check IP whitelist (add 0.0.0.0/0 for development)
```

**CORS Errors:**
```bash
# Check backend CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:3000

# Check frontend REACT_APP_BACKEND_URL
REACT_APP_BACKEND_URL=http://localhost:8001
```

**OpenAI API Errors:**
```bash
# Check API key format (should start with sk-)
# Verify billing is set up on OpenAI account
# Check API key permissions
```

### Debug Mode

**Enable detailed backend logging:**
```bash
# Add to backend/.env
LOG_LEVEL=DEBUG

# Or run with debug flag
uvicorn server:app --reload --host 0.0.0.0 --port 8001 --log-level debug
```

**Frontend debugging:**
```bash
# Open browser developer tools (F12)
# Check Console tab for JavaScript errors
# Check Network tab for API request failures
```

---

## 🔄 Development Workflow

### Making Changes

**Backend Changes:**
- FastAPI auto-reloads on file changes
- Check http://localhost:8001/docs for API updates

**Frontend Changes:**
- React auto-reloads on file changes
- Check browser console for errors

**Database Changes:**
- Use MongoDB Compass or Atlas web interface
- Or connect via CLI: `mongo` / `mongosh`

### Code Structure

```
backend/
├── server.py          # Main FastAPI application
├── requirements.txt   # Python dependencies
└── .env              # Environment variables

frontend/
├── src/
│   ├── App.js        # Main React component
│   ├── App.css       # Main styles
│   └── components/   # UI components
├── package.json      # Node dependencies
└── .env             # Environment variables
```

---

## 📚 Useful Commands

### Backend
```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
pytest

# Check code style
black server.py
flake8 server.py
```

### Frontend
```bash
# Install new package
npm install package-name
# or
yarn add package-name

# Run tests
npm test

# Build for production
npm run build

# Analyze bundle size
npm run analyze
```

### Database
```bash
# Connect to local MongoDB
mongosh
# or
mongo

# Connect to Atlas
mongosh "mongodb+srv://cluster.mongodb.net/people_analytics" --username <username>

# Basic commands
show dbs
use people_analytics
show collections
db.graph_data.find()
```

---

## 🎯 Next Steps

Once your local setup is working:

1. **Explore Features:**
   - Try different graph layouts
   - Test various question categories
   - Upload your own organizational data

2. **Customize:**
   - Modify question categories in `App.js`
   - Add new analysis functions in `server.py`
   - Customize styling in `App.css`

3. **Deploy:**
   - Follow `DEPLOYMENT.md` when ready to go live
   - Test locally first to ensure everything works

---

## 🆘 Need Help?

1. **Check logs** in your terminal windows
2. **Verify environment variables** are set correctly
3. **Test each component** individually (database, backend, frontend)
4. **Check browser developer tools** for frontend issues
5. **Review error messages** carefully - they usually point to the issue

Happy coding! 🚀✨