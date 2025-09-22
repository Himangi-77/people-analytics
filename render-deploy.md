# 🔥 Deploy to Render (FastAPI + React)

Render is the best Railway alternative with excellent FastAPI support.

## 🎯 **Why Render?**
- ✅ **Native FastAPI support**
- ✅ **750 hours/month free** (always-on for small apps)
- ✅ **Auto-deploy from GitHub**
- ✅ **Built-in HTTPS**
- ✅ **No sleep/cold starts** on free tier

---

## 🚀 **Step-by-Step Deployment**

### 1. **Setup GitHub Repository**
```bash
git add .
git commit -m "People Analytics App - Ready for deployment"
git push origin main
```

### 2. **Deploy Backend to Render**

1. **Go to [Render](https://render.com)**
2. **Sign up/Login** with GitHub
3. **New Web Service** → **Build and deploy from a Git repository**
4. **Connect your repository**
5. **Configure settings:**

```yaml
Name: people-analytics-backend
Region: Oregon (US West)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
```

6. **Environment Variables** (click Advanced):
```bash
PYTHON_VERSION=3.9.18
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics
DB_NAME=people_analytics
CORS_ORIGINS=https://your-frontend-url.vercel.app
EMERGENT_LLM_KEY=sk-your-openai-key
```

7. **Create Web Service** → Wait for deployment (~3-5 minutes)

8. **Get your backend URL**: `https://your-app-name.onrender.com`

### 3. **Deploy Frontend to Vercel**

1. **Go to [Vercel](https://vercel.com)**
2. **Import Project** from GitHub
3. **Configure:**
```yaml
Framework Preset: Create React App
Root Directory: frontend
Build Command: npm run build
Output Directory: build
```

4. **Environment Variables:**
```bash
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

5. **Deploy** → Get URL: `https://your-app.vercel.app`

### 4. **Update CORS Settings**

Go back to Render → Environment Variables → Update:
```bash
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

### 5. **Test Your Deployment**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-backend.onrender.com/docs`

---

## 🔧 **Render Configuration Files**

Add these to your repo for easier deployment:

**`render.yaml`** (in root directory):
```yaml
services:
  - type: web
    name: people-analytics-backend
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn server:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.18
      - key: MONGO_URL
        sync: false  # Set manually in dashboard
      - key: DB_NAME
        value: people_analytics
      - key: CORS_ORIGINS
        sync: false  # Set manually in dashboard  
      - key: EMERGENT_LLM_KEY
        sync: false  # Set manually in dashboard
```

---

## 💡 **Render Free Tier Limits**
- **750 hours/month** (31 days × 24 hours = 744 hours)
- **512MB RAM**
- **Auto-sleep after 15 minutes of inactivity**
- **Free HTTPS & custom domains**
- **Unlimited GitHub repositories**

---

## 🔧 **Auto-Deploy Setup**

Render automatically redeploys when you push to GitHub:
```bash
git add .
git commit -m "Update features"
git push origin main
# Render auto-deploys in ~2-3 minutes
```

---

## 📊 **Monitoring & Logs**

1. **Render Dashboard** → Your service → **Logs tab**
2. **Metrics tab** for performance monitoring
3. **Events tab** for deployment history

---

## 🚨 **Common Issues & Fixes**

**Build Failures:**
```bash
# Check Python version in render.yaml
PYTHON_VERSION=3.9.18

# Ensure requirements.txt is complete
pip freeze > requirements.txt
```

**Memory Issues:**
```bash
# Optimize imports in server.py
# Use lighter dependencies where possible
```

**Cold Starts:**
```bash
# Render free tier sleeps after 15 minutes
# First request after sleep takes ~30 seconds
# Consider upgrading to Starter plan ($7/month) for always-on
```

---

## 💰 **Pricing**
- **Free**: 750 hours/month, sleeps after 15min
- **Starter**: $7/month, always-on, 1GB RAM
- **Standard**: $25/month, 4GB RAM

Perfect for development and small production apps! 🎉