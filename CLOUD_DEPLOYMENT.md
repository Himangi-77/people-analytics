# ☁️ Cloud Deployment Guide - Railway Alternatives

Since Railway doesn't work well with FastAPI, here are **better alternatives** that fully support Python/FastAPI deployment via GitHub.

## 🏆 **Recommended: Render + Vercel + MongoDB Atlas**

**Why this combination?**
- ✅ **Render**: Best FastAPI support, 750 hours/month free
- ✅ **Vercel**: Perfect for React, unlimited free projects  
- ✅ **MongoDB Atlas**: 512MB free database
- ✅ **Total cost**: $0/month for development

---

## 🚀 **Step-by-Step Deployment**

### **Phase 1: Prepare Repository**

1. **Push to GitHub:**
```bash
git add .
git commit -m "People Analytics - Ready for cloud deployment"
git push origin main
```

2. **Repository structure should be:**
```
your-repo/
├── backend/          # FastAPI app
├── frontend/         # React app  
├── README.md
└── deployment files (already created)
```

### **Phase 2: Setup Database (MongoDB Atlas)**

1. **Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)**
2. **Create account** → **Build a Database** → **Free Shared**
3. **Create cluster** (takes 3-5 minutes)
4. **Database Access** → **Add Database User**
   - Username: `your-username`
   - Password: `strong-password`
5. **Network Access** → **Add IP Address** → **Allow Access from Anywhere** (`0.0.0.0/0`)
6. **Connect** → **Connect your application** → Copy connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/people_analytics
   ```

### **Phase 3: Deploy Backend (Render)**

1. **Go to [Render](https://render.com)**
2. **Sign up** with GitHub account
3. **New** → **Web Service** 
4. **Build and deploy from Git repository**
5. **Connect your repository**
6. **Configure:**
   ```
   Name: people-analytics-backend
   Region: Oregon (US West) 
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
   ```

7. **Advanced** → **Environment Variables:**
   ```bash
   PYTHON_VERSION=3.9.18
   MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics
   DB_NAME=people_analytics
   CORS_ORIGINS=*
   EMERGENT_LLM_KEY=sk-your-openai-api-key
   ```

8. **Create Web Service** → Wait for deployment (~5 minutes)
9. **Copy your backend URL**: `https://people-analytics-backend-xxxx.onrender.com`

### **Phase 4: Deploy Frontend (Vercel)**

1. **Go to [Vercel](https://vercel.com)**
2. **Import Project** → **Continue with GitHub**
3. **Import your repository**
4. **Configure:**
   ```
   Project Name: people-analytics-frontend
   Framework Preset: Create React App
   Root Directory: frontend
   ```

5. **Environment Variables:**
   ```bash
   REACT_APP_BACKEND_URL=https://people-analytics-backend-xxxx.onrender.com
   ```

6. **Deploy** → Wait (~2 minutes)
7. **Copy your frontend URL**: `https://people-analytics-frontend.vercel.app`

### **Phase 5: Update CORS**

1. **Go back to Render** → Your service → **Environment**
2. **Update CORS_ORIGINS:**
   ```bash
   CORS_ORIGINS=https://people-analytics-frontend.vercel.app,http://localhost:3000
   ```
3. **Save** → Service will auto-redeploy

### **Phase 6: Test Deployment**

1. **Visit your frontend URL**
2. **Test features:**
   - Upload graph data (use `sample-data.json`)
   - Ask sample questions
   - Verify AI analysis works
   - Check graph visualization

---

## 🔧 **Alternative Platforms**

### **Option B: Fly.io (More Advanced)**

**Better performance, $5 free credit/month**

1. **Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Deploy backend:**
```bash
cd backend
flyctl auth signup
flyctl launch --no-deploy
flyctl secrets set MONGO_URL="your-connection-string"
flyctl secrets set EMERGENT_LLM_KEY="your-openai-key"
flyctl deploy
```

3. **Frontend same as Vercel above**

### **Option C: Digital Ocean App Platform**

**$5/month after $100 free credit**

1. **Go to [Digital Ocean](https://cloud.digitalocean.com/apps)**
2. **Create App** → **GitHub** → Connect repo
3. **Configure:**
   - **Backend**: Python, root directory `backend`
   - **Frontend**: Node.js, root directory `frontend`
4. **Add environment variables**
5. **Deploy**

---

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | 750h/month | $7/month | Beginners |
| **Fly.io** | $5 credit/month | ~$2-3/month | Performance |
| **Digital Ocean** | $100 credit (60 days) | $5/month | Features |
| **Heroku** | 550h/month | $7/month | Simplicity |

---

## 🔑 **Environment Variables Reference**

### **Backend (All Platforms):**
```bash
PYTHON_VERSION=3.9.18
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/people_analytics
DB_NAME=people_analytics
CORS_ORIGINS=https://your-frontend-url.vercel.app
EMERGENT_LLM_KEY=sk-your-openai-api-key
```

### **Frontend (Vercel):**
```bash
REACT_APP_BACKEND_URL=https://your-backend-url.onrender.com
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

**CORS Errors:**
```bash
# Update CORS_ORIGINS in backend environment
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

**Build Failures:**
```bash
# Check build logs in platform dashboard
# Verify Python version: 3.9.18
# Check requirements.txt is complete
```

**Database Connection:**
```bash
# Verify MongoDB Atlas connection string
# Check IP whitelist includes 0.0.0.0/0
# Confirm database user has read/write permissions
```

**OpenAI API Issues:**
```bash
# Verify API key starts with 'sk-'
# Check OpenAI account has billing set up
# Test API key independently
```

---

## 🔄 **Continuous Deployment**

Both Render and Vercel support automatic deployments:
1. **Push to GitHub** → **Platforms auto-deploy**
2. **Check deployment status** in dashboards
3. **View logs** for any issues

```bash
git add .
git commit -m "Update features"
git push origin main
# Both platforms will automatically deploy
```

---

## 📊 **Expected Performance**

### **Render (Free Tier):**
- ✅ **Always-on** for first 750 hours/month
- ⏱️ **30-second cold start** after sleep
- 📈 **Good for development** and small production

### **Fly.io:**
- ✅ **No cold starts**
- ⚡ **Fast global deployment**
- 💰 **~$2-3/month** typical usage

### **Vercel (Frontend):**
- ⚡ **Instant global CDN**
- 🚀 **Zero cold starts**
- 📊 **Excellent performance metrics**

---

## 🎯 **Recommended Deployment Path**

1. **Start with Render + Vercel** (easiest, most generous free tier)
2. **Get OpenAI API key** (required for AI features)
3. **Use MongoDB Atlas** (512MB free is plenty for testing)
4. **Test thoroughly** before sharing
5. **Consider Fly.io upgrade** if you need better performance

---

## 🔗 **Quick Links**

- **Render**: https://render.com
- **Vercel**: https://vercel.com  
- **MongoDB Atlas**: https://cloud.mongodb.com
- **Fly.io**: https://fly.io
- **OpenAI API**: https://platform.openai.com/api-keys

---

## 🎉 **You're Live!**

Your People Analytics app with PageRank analysis, AI insights, and interactive visualization is now deployed to the cloud! 

**Share your URLs:**
- **App**: `https://your-app.vercel.app`
- **API**: `https://your-backend.onrender.com/docs`

Perfect for organizational network analysis! 🚀✨