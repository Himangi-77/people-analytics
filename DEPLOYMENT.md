# 🚀 Deployment Guide

Deploy your People Analytics app to free hosting platforms via GitHub.

## 📋 Overview

**Recommended Stack:**
- Frontend: **Vercel** (React)
- Backend: **Railway** (FastAPI) 
- Database: **MongoDB Atlas** (Free 512MB)

## 🔧 Step 1: Prepare GitHub Repository

1. **Create GitHub Repository**
```bash
git init
git add .
git commit -m "Initial commit: People Analytics App"
git branch -M main
git remote add origin https://github.com/yourusername/people-analytics.git
git push -u origin main
```

## 🗄️ Step 2: Setup MongoDB Atlas (Database)

1. **Create Account**: Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. **Create Cluster**: Choose "Free Shared" cluster
3. **Database Access**: Create database user with password
4. **Network Access**: Add IP `0.0.0.0/0` (allow from anywhere)
5. **Get Connection String**: 
   ```
   mongodb+srv://username:password@cluster.mongodb.net/people_analytics
   ```

## 🔥 Step 3: Deploy Backend to Railway

1. **Create Account**: Go to [Railway](https://railway.app)
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your GitHub repo
4. **Configure**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

5. **Environment Variables**:
   ```
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics
   DB_NAME=people_analytics
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   EMERGENT_LLM_KEY=your_openai_api_key
   ```

6. **Deploy**: Railway will auto-deploy and give you a URL like `https://your-app.railway.app`

## ⚡ Alternative: Deploy Backend to Render

1. **Create Account**: Go to [Render](https://render.com)
2. **New Web Service**: Connect GitHub repo
3. **Configure**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: `3.9.18`

4. **Environment Variables**: Same as Railway above

## 🌐 Step 4: Deploy Frontend to Vercel

1. **Create Account**: Go to [Vercel](https://vercel.com)
2. **Import Project**: Click "New Project" → Import from GitHub
3. **Configure**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Environment Variables**:
   ```
   REACT_APP_BACKEND_URL=https://your-backend.railway.app
   ```

5. **Deploy**: Vercel will auto-deploy and give you a URL like `https://your-app.vercel.app`

## 🔄 Step 5: Update CORS Settings

After frontend deployment, update backend environment variables:

**Railway/Render Environment Variables:**
```
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

## 📱 Step 6: Test Deployment

1. **Visit Frontend URL**: `https://your-app.vercel.app`
2. **Test Features**:
   - Upload graph data
   - Ask sample questions
   - Verify AI analysis works
   - Check graph visualization

## 🔑 Step 7: API Keys Setup

### OpenAI API Key (for AI Analysis)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to backend environment variables:
   ```
   EMERGENT_LLM_KEY=sk-your-openai-key-here
   ```

### Alternative: Use Emergent LLM Key
If you have access to Emergent integrations, use the provided key.

## 🔧 Advanced Configuration

### Custom Domain (Optional)
1. **Vercel**: Project Settings → Domains → Add custom domain
2. **Railway**: Project → Settings → Domains → Add custom domain

### Environment Management
1. **Development**: Use `.env.local`
2. **Production**: Use platform environment variables
3. **Staging**: Create separate deployments

### Monitoring & Logs
1. **Vercel**: Functions tab for frontend logs
2. **Railway**: Deployments tab for backend logs
3. **MongoDB Atlas**: Database monitoring

## 🚨 Troubleshooting

### Common Issues

**CORS Errors:**
```bash
# Update backend CORS_ORIGINS to include your frontend URL
CORS_ORIGINS=https://your-app.vercel.app
```

**Build Failures:**
```bash
# Check build logs in platform dashboards
# Ensure all dependencies in requirements.txt/package.json
```

**Database Connection:**
```bash
# Verify MongoDB Atlas connection string
# Check IP whitelist (0.0.0.0/0)
# Confirm database user permissions
```

**API Key Issues:**
```bash
# Verify OpenAI API key is valid
# Check billing/quota limits
# Ensure key has proper permissions
```

## 📊 Cost Summary

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Vercel** | 100GB bandwidth/month | Unlimited projects |
| **Railway** | $5 credit/month | ~500 hours |
| **Render** | 750 hours/month | Sleep after 15min idle |
| **MongoDB Atlas** | 512MB storage | 1 cluster |
| **OpenAI API** | $5 free credit | Pay per usage |

## 🔄 Continuous Deployment

Both platforms support automatic deployments:
- **Push to GitHub** → **Auto-deploy**
- **Environment variables** persist across deployments
- **Domain remains the same**

## 📈 Scaling Options

When you outgrow free tiers:
1. **Vercel Pro**: $20/month
2. **Railway Pro**: $20/month  
3. **MongoDB Atlas**: $9/month (2GB)
4. **Render Pro**: $7/month

## 🎯 Next Steps

1. Set up monitoring and alerts
2. Add custom analytics
3. Implement user authentication
4. Add data backup strategies
5. Configure CDN for better performance

Your People Analytics app is now live and ready for organizational network analysis! 🎉