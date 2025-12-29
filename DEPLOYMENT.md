# NeuroScan AI - Deployment Guide

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Production Deployment

### Option 1: Docker Deployment

#### Create Dockerfile for Backend
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
      - ./backend/models:/app/models

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### Option 2: Azure Deployment

#### Backend (Azure App Service)
```bash
# Login to Azure
az login

# Create resource group
az group create --name neuroscan-rg --location eastus

# Create App Service plan
az appservice plan create --name neuroscan-plan --resource-group neuroscan-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group neuroscan-rg --plan neuroscan-plan --name neuroscan-backend --runtime "PYTHON:3.10"

# Deploy
cd backend
zip -r deploy.zip .
az webapp deployment source config-zip --resource-group neuroscan-rg --name neuroscan-backend --src deploy.zip
```

#### Frontend (Azure Static Web Apps)
```bash
# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Deploy
cd frontend
npm run build
az staticwebapp create --name neuroscan-frontend --resource-group neuroscan-rg --source dist
```

### Option 3: AWS Deployment

#### Backend (AWS Elastic Beanstalk)
```bash
# Install EB CLI
pip install awsebcli

# Initialize
cd backend
eb init -p python-3.10 neuroscan-backend

# Create environment
eb create neuroscan-backend-env

# Deploy
eb deploy
```

#### Frontend (AWS Amplify)
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Configure
amplify configure

# Initialize
cd frontend
amplify init

# Add hosting
amplify add hosting

# Publish
amplify publish
```

## Environment Variables

### Backend (.env)
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Origins
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Model Paths
MODEL_PATH=./models/classifier.pkl
SCALER_PATH=./models/scaler.pkl

# Data Storage
DATA_DIR=./data

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env.production)
```env
VITE_API_URL=https://api.yourdomain.com/api
```

## Performance Optimization

### Backend
- Enable GPU acceleration for TensorFlow (if available)
- Use model quantization for faster inference
- Implement Redis caching for repeated requests
- Use Gunicorn with multiple workers

### Frontend
- Enable code splitting
- Optimize images and assets
- Use CDN for static assets
- Enable service worker for PWA

## Monitoring

### Backend Monitoring
```python
# Add to main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### Frontend Monitoring
```javascript
// Add Google Analytics or Application Insights
```

## Security Checklist

- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] API authentication (if needed)
- [ ] Security headers configured
- [ ] Regular dependency updates
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens

## Scaling Considerations

1. **Backend Scaling:**
   - Horizontal: Multiple backend instances behind load balancer
   - Vertical: Increase CPU/RAM for single instance
   - Database: Migrate from JSON to PostgreSQL/MongoDB

2. **Frontend Scaling:**
   - CDN distribution (CloudFront, Azure CDN)
   - Edge caching
   - Image optimization service

3. **Model Serving:**
   - Separate model serving service (TensorFlow Serving)
   - Model versioning
   - A/B testing different models

## Backup & Recovery

```bash
# Backup history data
tar -czf backup-$(date +%Y%m%d).tar.gz backend/data/

# Backup models
tar -czf models-$(date +%Y%m%d).tar.gz backend/models/

# Restore
tar -xzf backup-YYYYMMDD.tar.gz -C backend/data/
```

## Health Checks

### Backend Health Endpoint
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Frontend Health Check
```javascript
// Check API connectivity
const checkHealth = async () => {
  try {
    await axios.get('/api/health');
    return true;
  } catch {
    return false;
  }
};
```

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Check CORS_ORIGINS configuration
   - Verify frontend URL matches allowed origins

2. **Model Loading Errors:**
   - Ensure models directory exists
   - Check file permissions
   - Verify model file paths

3. **Camera Not Working:**
   - Must use HTTPS (except localhost)
   - Check browser permissions
   - Verify MediaPipe installation

## CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          # Your deployment commands
      
      - name: Deploy Frontend
        run: |
          # Your deployment commands
```

## Cost Estimation

### Azure (Monthly)
- App Service (B1): $13
- Static Web Apps: $9
- Storage: $1
- **Total: ~$25/month**

### AWS (Monthly)
- EC2 (t3.small): $15
- S3 + CloudFront: $5
- **Total: ~$20/month**

### Self-Hosted
- VPS (2GB RAM): $10-20/month
- Domain: $12/year
- **Total: ~$15/month**
