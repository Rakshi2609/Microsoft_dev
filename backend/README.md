# NeuroScan AI - Backend

FastAPI backend for stroke risk screening using facial asymmetry analysis.

## Quick Start

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server runs on http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### POST /api/scan/image
Upload image for stroke risk assessment.

**Request:**
- Content-Type: multipart/form-data
- Body: image file (JPG/PNG)

**Response:**
```json
{
  "risk": "Medium",
  "confidence": 0.72,
  "score": 0.43,
  "features": {
    "eye_asymmetry": 0.18,
    "mouth_asymmetry": 0.21,
    "nose_deviation": 0.11,
    "face_tilt": 0.08,
    "symmetry_ratio": 0.85
  },
  "timestamp": "2025-01-01T12:00:00",
  "disclaimer": "This is a pre-diagnostic screening tool..."
}
```

### GET /api/history
Retrieve all scan history.

### GET /api/history/stats/summary
Get statistics summary.

## Development

```bash
# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint
flake8 .
```
