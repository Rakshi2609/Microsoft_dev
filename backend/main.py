"""
NeuroScan AI - Backend Main Application
Imagine Cup Healthcare Project

FastAPI backend for stroke risk screening using facial asymmetry analysis.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NeuroScan AI API",
    description="Smartphone-based early stroke risk screening using facial asymmetry analysis",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NeuroScan AI API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "scan": "/api/scan/image",
            "history": "/api/history"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "NeuroScan AI"}

# Import routes
from routes import scan, history

# Register route modules
app.include_router(scan.router, prefix="/api", tags=["Scan"])
app.include_router(history.router, prefix="/api", tags=["History"])

if __name__ == "__main__":
    logger.info("Starting NeuroScan AI Backend Server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
