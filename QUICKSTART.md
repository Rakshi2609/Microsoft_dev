# NeuroScan AI - Quick Start Guide

Welcome to NeuroScan AI! This guide will help you get started quickly.

## Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.10 or higher
- ✅ Node.js 18 or higher
- ✅ Webcam (for live scanning)
- ✅ 2GB+ free disk space

## Installation Options

### Option 1: Automated Setup (Recommended)

#### Windows
```bash
setup.bat
```

#### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

## Running the Application

### Step 1: Start Backend

Open a terminal:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Start Frontend

Open a **new** terminal:
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
```

### Step 3: Open Application

Open your browser and navigate to: **http://localhost:3000**

## First Scan

1. Click **"Start Scan Now"** on the home page
2. Allow camera permissions when prompted
3. Choose **Camera** or **Upload** mode
4. Follow on-screen instructions
5. Click **"Analyze Image"**
6. View your results!

## Troubleshooting

### Camera Not Working
- **Issue:** Camera access denied
- **Solution:** 
  - Check browser permissions (Settings → Privacy → Camera)
  - Ensure you're using HTTPS or localhost
  - Try a different browser

### Backend Won't Start
- **Issue:** Port 8000 already in use
- **Solution:**
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # macOS/Linux
  lsof -ti:8000 | xargs kill -9
  ```

### Module Not Found
- **Issue:** Python module missing
- **Solution:**
  ```bash
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt --upgrade
  ```

### npm Install Fails
- **Issue:** Node modules not installing
- **Solution:**
  ```bash
  cd frontend
  rm -rf node_modules package-lock.json
  npm cache clean --force
  npm install
  ```

## API Documentation

Once the backend is running, view API docs:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Testing the API

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Scan status
curl http://localhost:8000/api/scan/status

# Upload image
curl -X POST http://localhost:8000/api/scan/image \
  -F "image=@/path/to/your/face.jpg"
```

### Using the Frontend
1. Go to http://localhost:3000/scan
2. Upload or capture an image
3. Click "Analyze Image"
4. View results

## Next Steps

- 📖 Read the [full README](README.md)
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 🔒 Review [SECURITY.md](SECURITY.md) for security guidelines

## Getting Help

- **Issues:** Create an issue on GitHub
- **Questions:** Check the FAQ in README.md
- **Email:** contact@neuroscan.ai

## Important Reminders

⚠️ **Medical Disclaimer:**
- This is NOT a medical diagnostic tool
- Results are for screening purposes only
- Always consult healthcare professionals
- Call emergency services if experiencing stroke symptoms

## Demo Credentials

For testing purposes, the application works without authentication. In production, implement proper security measures.

## Performance Tips

- Use latest Chrome/Firefox for best camera support
- Ensure good lighting for accurate results
- Face camera directly
- Remove glasses if possible

---

**Made with ❤️ for Microsoft Imagine Cup 2025**

Happy screening! 🎉
