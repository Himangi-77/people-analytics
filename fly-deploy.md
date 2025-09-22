# ✈️ Deploy to Fly.io (FastAPI + React)

Fly.io is a modern deployment platform with excellent FastAPI support.

## 🎯 **Why Fly.io?**
- ✅ **Excellent FastAPI support**
- ✅ **$5 free credit/month** (generous allowance)
- ✅ **Global edge deployment**
- ✅ **Docker-based** (reliable)
- ✅ **No cold starts**

---

## 🚀 **Step-by-Step Deployment**

### 1. **Install Fly CLI**

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. **Setup Fly.io Account**
```bash
flyctl auth signup
# or
flyctl auth login
```

### 3. **Deploy Backend**

```bash
cd backend

# Initialize Fly app
flyctl launch --no-deploy

# Answer prompts:
# App name: people-analytics-backend
# Region: Choose closest to you
# Add PostgreSQL? No
# Add Redis? No
# Deploy now? No
```

This creates `fly.toml` config file. Update it:

**`backend/fly.toml`:**
```toml
app = "people-analytics-backend"
primary_region = "dfw"  # or your chosen region

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8001"
  PYTHON_VERSION = "3.9"

[http_service]
  internal_port = 8001
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/"

[deploy]
  release_command = "echo 'Deployment complete'"

[vm]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### 4. **Set Environment Variables**
```bash
flyctl secrets set MONGO_URL="mongodb+srv://username:password@cluster.mongodb.net/people_analytics"
flyctl secrets set DB_NAME="people_analytics"
flyctl secrets set EMERGENT_LLM_KEY="sk-your-openai-key"
flyctl secrets set CORS_ORIGINS="https://your-frontend.vercel.app,http://localhost:3000"
```

### 5. **Deploy Backend**
```bash
flyctl deploy

# Get your app URL
flyctl info
# Your backend: https://people-analytics-backend.fly.dev
```

### 6. **Deploy Frontend to Vercel**

Same as Render option:
1. Go to [Vercel](https://vercel.com)
2. Import GitHub repo
3. Set root directory: `frontend`
4. Add environment variable:
   ```bash
   REACT_APP_BACKEND_URL=https://people-analytics-backend.fly.dev
   ```

### 7. **Update CORS**
```bash
flyctl secrets set CORS_ORIGINS="https://your-app.vercel.app,http://localhost:3000"
```

---

## 🔧 **Fly.io Configuration Files**

**`backend/Dockerfile`** (already created):
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8001
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 💰 **Fly.io Pricing**
- **Free allowance**: $5/month credit
- **Shared CPU**: ~$2/month for small apps
- **Memory**: $0.0000018/MB/second
- **Bandwidth**: $0.02/GB

**Typical small app cost**: $1-3/month (well within free credit)

---

## 🔧 **Useful Fly Commands**

```bash
# Deploy
flyctl deploy

# Check status
flyctl status

# View logs
flyctl logs

# SSH into machine
flyctl ssh console

# Scale app
flyctl scale count 2

# Monitor resources
flyctl monitor
```

---

## 🚨 **Troubleshooting**

**Build Issues:**
```bash
# Check Dockerfile
flyctl logs

# Deploy with verbose output
flyctl deploy --verbose
```

**Memory Issues:**
```bash
# Increase memory in fly.toml
memory_mb = 1024
```

**Networking Issues:**
```bash
# Check app health
flyctl status
flyctl checks list
```

Perfect for production workloads! 🚀