# ⚡ Quick Deployment Guide

## 🚀 **1-Click Deploy Options**

### Option A: Vercel + Railway + MongoDB Atlas (Recommended)

**Total Setup Time: ~15 minutes**

1. **Fork/Clone to GitHub**
   ```bash
   git clone your-repo
   cd people-analytics
   ./deploy.sh  # Run setup script
   ```

2. **MongoDB Atlas (2 mins)**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free account → Create cluster → Get connection string

3. **Railway Backend (5 mins)**
   - Go to [Railway](https://railway.app) 
   - Connect GitHub → Select repo → Set root dir: `backend`
   - Add env vars (see below)

4. **Vercel Frontend (3 mins)**
   - Go to [Vercel](https://vercel.com)
   - Import GitHub repo → Set root dir: `frontend`
   - Add backend URL env var

5. **Done!** ✅

---

## 🔧 **Environment Variables**

### Backend (Railway)
```bash
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/people_analytics
DB_NAME=people_analytics
CORS_ORIGINS=https://your-app.vercel.app
EMERGENT_LLM_KEY=sk-your-openai-key
```

### Frontend (Vercel)
```bash
REACT_APP_BACKEND_URL=https://your-backend.railway.app
```

---

## 🆓 **Alternative Free Platforms**

### Backend Options:
- **Railway** (Recommended) - $5 credit/month
- **Render** - 750 hours/month free
- **Fly.io** - 3 apps free
- **PythonAnywhere** - Limited free tier

### Frontend Options:
- **Vercel** (Recommended) - Unlimited projects
- **Netlify** - 100GB/month
- **GitHub Pages** - Static only
- **Firebase Hosting** - 10GB/month

### Database Options:
- **MongoDB Atlas** (Recommended) - 512MB free
- **PlanetScale** - 1GB free MySQL
- **Supabase** - 500MB free PostgreSQL

---

## 🎯 **Platform-Specific Instructions**

### Vercel (Frontend)
```json
// vercel.json already configured
{
  "builds": [{"src": "package.json", "use": "@vercel/static-build"}],
  "routes": [{"src": "/(.*)", "dest": "/index.html"}]
}
```

### Railway (Backend)
```json
// railway.json already configured
{
  "build": {"builder": "DOCKERFILE"},
  "deploy": {"startCommand": "uvicorn server:app --host 0.0.0.0 --port $PORT"}
}
```

### Render (Backend Alternative)
```yaml
# render.yaml already configured
services:
  - type: web
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn server:app --host 0.0.0.0 --port $PORT
```

---

## 🔍 **Testing Your Deployment**

### ✅ Checklist
- [ ] Frontend loads at Vercel URL
- [ ] Backend responds at Railway URL
- [ ] Graph upload works
- [ ] AI analysis returns results
- [ ] Graph visualization displays
- [ ] No CORS errors in browser console

### 🔧 Common Fixes
```bash
# CORS Error
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Build Error
# Check logs in platform dashboard
# Verify all dependencies in requirements.txt

# Database Connection
# Check MongoDB Atlas IP whitelist: 0.0.0.0/0
```

---

## 💰 **Cost Breakdown (Monthly)**

| Service | Free Tier | Paid Upgrade |
|---------|-----------|--------------|
| Vercel | 100GB bandwidth | $20/month |
| Railway | $5 credit (~500 hours) | $20/month |
| MongoDB Atlas | 512MB | $9/month (2GB) |
| OpenAI API | $5 free credit | Pay per use |
| **Total Free** | **~$5/month** | **~$49/month** |

---

## 🚀 **One-Click Deploy Buttons**

Add these to your GitHub README:

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/people-analytics&project-name=people-analytics&repository-name=people-analytics&root-directory=frontend)

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/people-analytics&root-directory=backend)

---

## 🆘 **Need Help?**

1. **Check logs** in platform dashboards
2. **Verify environment variables** are set correctly
3. **Test APIs directly** using the provided URLs
4. **Review DEPLOYMENT.md** for detailed troubleshooting

---

## 🎉 **You're Live!**

Your People Analytics app is now deployed and ready for organizational network analysis!

**Share your app:**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-backend.railway.app/docs`

**Next steps:**
- Add custom domain
- Set up monitoring
- Scale as needed

Happy analyzing! 📊✨