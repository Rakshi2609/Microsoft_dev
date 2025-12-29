@echo off
REM NeuroScan AI - Automated Setup Script for Windows
REM This script sets up both backend and frontend automatically

echo ============================================
echo    NeuroScan AI - Automated Setup
echo    Microsoft Imagine Cup 2025
echo ============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check if Node.js is installed
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

echo ============================================
echo    Setting up Backend
echo ============================================
echo.

cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
echo [OK] Backend dependencies installed
echo.

REM Create necessary directories
echo Creating data directories...
if not exist "models" mkdir models
if not exist "data" mkdir data

echo [OK] Backend setup complete
echo.

cd ..

echo ============================================
echo    Setting up Frontend
echo ============================================
echo.

cd frontend

REM Install npm dependencies
echo Installing Node.js dependencies...
call npm install

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
echo [OK] Frontend dependencies installed
echo.

cd ..

echo ============================================
echo    Setting up ML Models
echo ============================================
echo.

cd ml

REM Activate backend venv
call ..\backend\venv\Scripts\activate.bat

REM Generate synthetic dataset
echo Generating synthetic dataset for demo...
python feature_extraction.py

if %errorlevel% neq 0 (
    echo [WARNING] Could not generate dataset (optional step)
)

REM Train classifier
echo Training classifier...
python train_classifier.py

if %errorlevel% neq 0 (
    echo [WARNING] Could not train classifier (will use rule-based model)
)

cd ..

echo.
echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo [OK] All components installed successfully!
echo.
echo To run the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:3000 in your browser
echo.
echo Note: You may need to allow camera permissions in your browser
echo.
pause
