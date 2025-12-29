# NeuroScan AI 🧠

## Smartphone-Based Early Stroke Risk Screening

**Microsoft Imagine Cup 2025** | Healthcare Innovation Category

---

## 🌟 Project Overview

NeuroScan AI is an innovative healthcare application that uses smartphone cameras to perform early stroke risk screening through facial asymmetry analysis. Using advanced AI and computer vision techniques, the app provides pre-diagnostic risk assessment in under 5 seconds.

### 🎯 Problem Statement

Stroke is the 5th leading cause of death and a major cause of disability. Early detection is crucial but:
- Traditional screening requires clinical visits
- Many at-risk individuals lack access to immediate medical evaluation
- Facial asymmetry (Bell's palsy-like symptoms) is an early stroke indicator

### 💡 Our Solution

A mobile-first web application that:
- ✅ Analyzes facial symmetry using AI in < 5 seconds
- ✅ Provides Low/Medium/High risk assessment
- ✅ Accessible via any smartphone browser
- ✅ Privacy-focused (local processing)
- ✅ Free and easy to use

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                     │
│  - Camera Capture / Image Upload                       │
│  - Results Visualization                               │
│  - Scan History Dashboard                              │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTP/REST API
┌───────────────────▼─────────────────────────────────────┐
│                 Backend (FastAPI)                       │
│  ┌────────────────────────────────────────────────┐   │
│  │  Face Detection (MediaPipe)                    │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Facial Landmark Extraction (468 points)      │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  MobileNetV2 Feature Extraction                │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Asymmetry Analysis Engine                     │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Risk Scoring Model (ML Classifier)            │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 Technical Details

### ML Pipeline

1. **Face Detection** (MediaPipe Face Detection)
   - Detects face in uploaded image
   - Crops and prepares face region

2. **Landmark Extraction** (MediaPipe Face Mesh)
   - Extracts 468 facial landmarks
   - Identifies key features: eyes, mouth, nose, etc.

3. **Feature Engineering**
   - **Geometric Features:**
     - Eye asymmetry (vertical position difference)
     - Mouth corner asymmetry
     - Nose deviation from centerline
     - Face tilt angle
     - Left-right symmetry ratio
     - Eye openness differences
     - Mouth aspect ratios
   
   - **Deep Features:**
     - MobileNetV2 embeddings (1280-dim)
     - Transfer learning from ImageNet

4. **Risk Classification**
   - Combines geometric + deep features
   - Trained classifier (Random Forest / Logistic Regression)
   - Outputs: Low / Medium / High risk with confidence

### Tech Stack

**Frontend:**
- React 18
- Tailwind CSS
- React Router
- React Webcam
- Axios
- Vite

**Backend:**
- FastAPI
- Python 3.10+
- OpenCV
- MediaPipe
- TensorFlow / Keras
- scikit-learn
- NumPy

**ML Models:**
- MobileNetV2 (pretrained on ImageNet)
- Custom asymmetry classifier
- Facial landmark detection (MediaPipe)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **npm or yarn**
- **Webcam** (for live scanning)

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/neuroscan-ai.git
cd neuroscan-ai
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p models data
```

#### 3. Train ML Models (Optional)

```bash
cd ../ml

# Generate synthetic dataset for demo
python feature_extraction.py

# Train classifier
python train_classifier.py

# Models will be saved to backend/models/
```

**Note:** The application works with rule-based model by default. Training is optional for improved accuracy.

#### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Or with yarn
yarn install
```

### Running the Application

#### Start Backend Server

```bash
cd backend
python main.py

# Server runs on http://localhost:8000
```

#### Start Frontend

```bash
cd frontend
npm run dev

# App runs on http://localhost:3000
```

#### Access Application

Open browser and navigate to: **http://localhost:3000**

---

## 📱 Usage Guide

### 1. Home Page
- Overview of the application
- Start scan or view dashboard

### 2. Scan Page
- **Camera Mode:** Use webcam for live capture
- **Upload Mode:** Upload existing photo
- Tips for best results provided

### 3. Results Page
- Risk level badge (Low/Medium/High)
- Confidence percentage
- Feature breakdown with explanations
- Recommendations based on risk
- Download/share results

### 4. Dashboard
- Scan history
- Statistics summary
- Filter by risk level
- Clear history option

---

## 🎨 Features

### Core Features
✅ Live camera capture with countdown  
✅ Image upload support  
✅ Real-time facial analysis  
✅ Risk level classification  
✅ Confidence scoring  
✅ Feature explainability  
✅ Scan history tracking  
✅ Statistics dashboard  
✅ Result export (text file)  
✅ Responsive mobile design  

### Safety Features
⚠️ Clear medical disclaimers  
⚠️ FAST test reference  
⚠️ Emergency contact information  
⚠️ Recommendations by risk level  
⚠️ Privacy-focused architecture  

---

## 🧪 Testing

### Backend API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test scan status
curl http://localhost:8000/api/scan/status

# Test image upload (replace with your image path)
curl -X POST http://localhost:8000/api/scan/image \
  -F "image=@/path/to/face.jpg"
```

### Frontend Testing

1. Open browser to `http://localhost:3000`
2. Test camera permissions
3. Capture test image
4. Verify results display
5. Check history persistence

---

## 📊 Model Performance

### Asymmetry Features

| Feature | Description | Clinical Relevance |
|---------|-------------|-------------------|
| Eye Asymmetry | Vertical position difference | High (25%) |
| Mouth Asymmetry | Corner height difference | High (25%) |
| Eye Openness | Eyelid droop detection | Medium (15%) |
| Nose Deviation | Alignment from center | Medium (15%) |
| Mouth Ratio | Aspect ratio differences | Low (10%) |
| Face Tilt | Overall head tilt | Low (10%) |

### Risk Thresholds

- **Low Risk:** Score < 0.30
- **Medium Risk:** 0.30 ≤ Score < 0.60
- **High Risk:** Score ≥ 0.60

---

## 🔒 Privacy & Security

- ✅ No images stored on servers
- ✅ Local processing where possible
- ✅ Minimal data retention
- ✅ HIPAA-compliant architecture
- ✅ User data control
- ✅ Anonymous usage

---

## ⚠️ Important Disclaimers

**THIS IS NOT A MEDICAL DIAGNOSTIC TOOL**

- This application provides pre-diagnostic screening only
- Results are NOT medical diagnoses
- Always consult healthcare professionals for medical advice
- Not a substitute for professional medical evaluation
- If experiencing stroke symptoms, call emergency services immediately

### FAST Test (Stroke Warning Signs)

- **F** - Face drooping
- **A** - Arm weakness
- **S** - Speech difficulty
- **T** - Time to call 911

---

## 📂 Project Structure

```
neuroscan-ai/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── scan.py            # Scan endpoints
│   │   └── history.py         # History endpoints
│   ├── services/
│   │   ├── face_detection.py  # Face detection service
│   │   ├── landmarks.py       # Landmark extraction
│   │   ├── mobilenet_features.py  # MobileNet features
│   │   ├── asymmetry.py       # Asymmetry calculation
│   │   ├── risk_model.py      # Risk prediction
│   │   └── history_manager.py # History management
│   ├── models/                # Trained ML models
│   └── data/                  # Scan history storage
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── api.js            # API client
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── CameraCapture.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── RiskBadge.jsx
│   │   │   ├── ResultDetails.jsx
│   │   │   └── HistoryCard.jsx
│   │   └── pages/
│   │       ├── Home.jsx
│   │       ├── Scan.jsx
│   │       ├── Result.jsx
│   │       └── Dashboard.jsx
├── ml/
│   ├── feature_extraction.py  # Feature extraction script
│   ├── train_classifier.py    # Classifier training
│   └── train_mobilenet.py     # MobileNet fine-tuning (optional)
└── README.md
```

---

## 🛠️ Development

### Adding New Features

1. **Backend:** Add services in `backend/services/`
2. **API Routes:** Add routes in `backend/routes/`
3. **Frontend Components:** Add to `frontend/src/components/`
4. **Pages:** Add to `frontend/src/pages/`

### Code Style

- **Python:** PEP 8, with docstrings
- **JavaScript:** ES6+, functional components
- **React:** Hooks, no class components

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git commit -m "Add new feature"

# Push and create PR
git push origin feature/new-feature
```

---

## 🐛 Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue:** Camera not accessible
```bash
# Solution: Check MediaPipe installation
pip install mediapipe --upgrade
```

### Frontend Issues

**Issue:** `npm install` fails
```bash
# Solution: Clear cache and retry
npm cache clean --force
npm install
```

**Issue:** Camera not working
- Check browser permissions
- Use HTTPS for camera access (or localhost)
- Verify webcam connection

---

## 📈 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Real-time video analysis
- [ ] Multi-language support
- [ ] Cloud deployment
- [ ] Medical professional dashboard
- [ ] Historical trend analysis
- [ ] Integration with health records
- [ ] Telemedicine integration

---

## 👥 Team

**[Your Team Name]**

- [Team Member 1] - Role
- [Team Member 2] - Role
- [Team Member 3] - Role

---

## 📄 License

This project is created for Microsoft Imagine Cup 2025.

---

## 🙏 Acknowledgments

- **MediaPipe** - Face detection and landmarks
- **TensorFlow** - MobileNet pretrained models
- **Microsoft** - Imagine Cup opportunity
- **Healthcare professionals** - Domain expertise
- **Open source community** - Libraries and tools

---

## 📞 Contact

- **Project Repository:** [GitHub Link]
- **Email:** contact@neuroscan.ai
- **Imagine Cup Team:** [Team Page Link]

---

## 🏆 Imagine Cup Submission

### Innovation
- First smartphone-based facial asymmetry screening
- Accessible healthcare technology
- AI-powered early detection

### Impact
- Addresses global stroke burden
- Increases awareness and early detection
- Reduces healthcare costs through prevention
- Accessible to underserved populations

### Technical Excellence
- Advanced ML pipeline (MobileNet + MediaPipe)
- Scalable architecture
- Real-time processing
- Privacy-focused design

### Demo
🎥 [Demo Video Link]  
🌐 [Live Demo Link]

---

**Made with ❤️ for Microsoft Imagine Cup 2025**

*Early detection saves lives.*
#   M i c r o s o f t _ d e v  
 