#!/bin/bash

# NeuroScan AI - Automated Setup Script
# This script sets up both backend and frontend automatically

echo "============================================"
echo "   NeuroScan AI - Automated Setup"
echo "   Microsoft Imagine Cup 2025"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.10+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check if Node.js is installed
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

echo ""
echo "============================================"
echo "   Setting up Backend"
echo "============================================"
echo ""

cd backend

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install backend dependencies${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}Creating data directories...${NC}"
mkdir -p models
mkdir -p data

echo -e "${GREEN}✓ Backend setup complete${NC}"

cd ..

echo ""
echo "============================================"
echo "   Setting up Frontend"
echo "============================================"
echo ""

cd frontend

# Install npm dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install frontend dependencies${NC}"
    exit 1
fi

cd ..

echo ""
echo "============================================"
echo "   Setting up ML Models"
echo "============================================"
echo ""

cd ml

# Generate synthetic dataset
echo -e "${YELLOW}Generating synthetic dataset for demo...${NC}"
source ../backend/venv/bin/activate
python feature_extraction.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Synthetic dataset created${NC}"
else
    echo -e "${YELLOW}⚠ Could not generate dataset (optional step)${NC}"
fi

# Train classifier
echo -e "${YELLOW}Training classifier...${NC}"
python train_classifier.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Classifier trained and saved${NC}"
else
    echo -e "${YELLOW}⚠ Could not train classifier (will use rule-based model)${NC}"
fi

cd ..

echo ""
echo "============================================"
echo "   Setup Complete!"
echo "============================================"
echo ""
echo -e "${GREEN}✓ All components installed successfully!${NC}"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}Note: You may need to allow camera permissions in your browser${NC}"
echo ""
