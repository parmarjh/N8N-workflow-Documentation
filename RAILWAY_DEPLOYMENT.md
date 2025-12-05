# Railway Deployment Fix Guide

## Common Railway Deployment Issues \u0026 Solutions

### Issue 1: Port Binding Error
**Symptom**: Application fails to start, logs show "Address already in use"

**Solution**: Update Dockerfile CMD to use Railway's `$PORT` variable

**Current Dockerfile** (line 63):
```dockerfile
CMD ["python", "-u", "run.py", "--host", "0.0.0.0", "--port", "8000"]
```

**Fixed Version**:
```dockerfile
CMD ["sh", "-c", "python -u run.py --host 0.0.0.0 --port ${PORT:-8000}"]
```

---

### Issue 2: Missing Environment Variables
**Required Variables**:

| Variable | Value | Purpose |
|----------|-------|---------|
| `PORT` | Auto-set by Railway | Server port |
| `PYTHON_VERSION` | `3.11` | Python runtime |
| `CI` | `false` | Enable workflow indexing |
| `RAILWAY_ENVIRONMENT` | `production` | Environment mode |

**How to Add**:
1. Go to Railway project → Variables tab
2. Click "New Variable"
3. Add each variable above

---

### Issue 3: Build Timeout
**Symptom**: Build fails after 10-15 minutes

**Causes**:
- Workflow indexing takes too long (2,061 files)
- Large Docker image
- Slow dependency installation

**Solutions**:

#### Option A: Skip Initial Indexing
Add to Railway Variables:
```
CI=true
```
This skips workflow indexing during build. Database will be empty initially.

#### Option B: Pre-build Database
1. Build database locally:
   ```bash
   python workflow_db.py --index --force
   ```
2. Commit `database/workflows.db` to git (remove from .gitignore)
3. Redeploy

#### Option C: Increase Build Resources
- Upgrade Railway plan for faster builds
- Or optimize Dockerfile (see below)

---

### Issue 4: Out of Memory
**Symptom**: Process killed during startup, "OOMKilled" in logs

**Solution**: Optimize memory usage

**Add to run.py** (before indexing):
```python
import gc
gc.collect()  # Force garbage collection
```

**Or**: Upgrade Railway plan to higher memory tier

---

### Issue 5: Database Not Persisting
**Symptom**: Database resets on each deployment

**Solution**: Use Railway Volumes

1. Go to Railway project → Service → Settings
2. Scroll to "Volumes"
3. Click "New Volume"
4. Configure:
   - **Mount Path**: `/app/database`
   - **Size**: `1 GB`

---

## Optimized Dockerfile for Railway

Create `Dockerfile.railway` with these optimizations:

```dockerfile
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create app user
RUN groupadd -g 1001 appuser && \
    useradd -m -u 1001 -g appuser appuser

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Create directories
RUN mkdir -p /app/database /app/workflows && \
    chown -R appuser:appuser /app

USER appuser

# Use Railway's PORT variable
CMD sh -c "python -u run.py --host 0.0.0.0 --port ${PORT:-8000}"
```

---

## Quick Fix Checklist

### Step 1: Update Dockerfile
```bash
# Edit line 63 in Dockerfile
CMD ["sh", "-c", "python -u run.py --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Step 2: Add railway.json
Create `railway.json` in repository root (already created for you).

### Step 3: Set Environment Variables in Railway
```
PORT = (auto-set by Railway)
PYTHON_VERSION = 3.11
CI = false
```

### Step 4: Add Volume (Optional but Recommended)
- Mount Path: `/app/database`
- Size: 1 GB

### Step 5: Commit and Push
```bash
git add Dockerfile railway.json
git commit -m "Fix Railway deployment configuration"
git push origin main
```

### Step 6: Redeploy in Railway
- Railway will auto-deploy on push
- Or manually trigger: Settings → Deployments → Deploy

---

## Deployment Logs to Check

### Successful Deployment Logs Should Show:
```
✅ Dependencies verified
✅ Directories verified
🔄 Setting up database
📚 Indexing workflows...
✅ Indexed 2061 workflows
🌐 Starting server at http://0.0.0.0:$PORT
```

### Failed Deployment - Look For:
- ❌ `Address already in use` → Port issue
- ❌ `ModuleNotFoundError` → Missing dependencies
- ❌ `OOMKilled` → Out of memory
- ❌ `Timeout` → Build taking too long

---

## Railway-Specific Configuration

### Recommended Settings

**Service Settings**:
- **Builder**: Dockerfile
- **Dockerfile Path**: `Dockerfile`
- **Start Command**: (leave empty, uses CMD from Dockerfile)
- **Watch Paths**: (leave empty for full repo)

**Healthcheck**:
- **Path**: `/api/stats`
- **Timeout**: 10 seconds
- **Interval**: 30 seconds

**Networking**:
- **Public Domain**: Enabled
- **Private Networking**: Enabled (if using other Railway services)

---

## Testing Your Deployment

Once deployed, test these endpoints:

```bash
# Replace with your Railway URL
RAILWAY_URL="https://your-app.up.railway.app"

# Health check
curl $RAILWAY_URL/api/stats

# Search workflows
curl "$RAILWAY_URL/api/search?q=telegram"

# API documentation
open $RAILWAY_URL/docs
```

---

## Cost Optimization

### Free Tier ($0/month)
- **Limit**: $5 credit/month
- **Usage**: ~550 hours
- **Good for**: Testing, low-traffic apps

### Hobby Plan ($5/month)
- **Includes**: $5 credit
- **Additional**: $0.000231/GB-hour for resources
- **Good for**: Personal projects

### Pro Plan ($20/month)
- **Includes**: $20 credit
- **Priority**: Support, faster builds
- **Good for**: Production apps

---

## Next Steps

1. ✅ Update Dockerfile CMD (see Step 1)
2. ✅ Add railway.json (already created)
3. ✅ Set environment variables in Railway
4. ✅ Add volume for database persistence
5. ✅ Commit and push changes
6. ✅ Monitor deployment logs
7. ✅ Test endpoints

**Your Railway app will be live at**: `https://n8n-workflow-documentation.up.railway.app`
