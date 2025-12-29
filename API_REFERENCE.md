# NeuroScan AI - API Reference

## Base URL

**Development:** `http://localhost:8000/api`  
**Production:** `https://your-domain.com/api`

---

## Authentication

Currently, no authentication is required. For production deployment, consider implementing:
- API Keys
- JWT tokens
- OAuth 2.0

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "NeuroScan AI"
}
```

---

### 2. Scan Status

**GET** `/scan/status`

Check if scan service is operational.

**Response:**
```json
{
  "status": "operational",
  "services": {
    "face_detection": "ready",
    "landmark_extraction": "ready",
    "mobilenet": "ready",
    "risk_model": "ready"
  }
}
```

---

### 3. Scan Image

**POST** `/scan/image`

Upload image for stroke risk assessment.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** 
  - `image` (file): Image file (JPG/PNG, max 10MB)

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/api/scan/image \
  -F "image=@/path/to/face.jpg"
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('image', imageFile);

const response = await axios.post('/api/scan/image', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

**Success Response (200):**
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
  "timestamp": "2025-01-01T12:00:00.000Z",
  "disclaimer": "This is a pre-diagnostic screening tool..."
}
```

**Error Response (400):**
```json
{
  "error": "No face detected",
  "message": "Please ensure your face is clearly visible...",
  "suggestions": [
    "Make sure there is adequate lighting",
    "Face the camera directly",
    "Remove any obstructions"
  ]
}
```

**Error Response (500):**
```json
{
  "detail": "Internal server error: ..."
}
```

---

### 4. Get History

**GET** `/history`

Retrieve all scan history records.

**Response (200):**
```json
[
  {
    "id": "uuid-string",
    "risk": "Low",
    "confidence": 0.85,
    "score": 0.21,
    "features": { ... },
    "timestamp": "2025-01-01T12:00:00.000Z",
    "disclaimer": "..."
  },
  ...
]
```

---

### 5. Get History by ID

**GET** `/history/{scan_id}`

Retrieve specific scan result.

**Parameters:**
- `scan_id` (path): Unique scan identifier

**Response (200):**
```json
{
  "id": "uuid-string",
  "risk": "Medium",
  "confidence": 0.72,
  "score": 0.43,
  "features": { ... },
  "timestamp": "2025-01-01T12:00:00.000Z"
}
```

**Error Response (404):**
```json
{
  "detail": "Scan with ID 'xxx' not found"
}
```

---

### 6. Get History Statistics

**GET** `/history/stats/summary`

Get statistical summary of scan history.

**Response (200):**
```json
{
  "total_scans": 25,
  "risk_distribution": {
    "low": 15,
    "medium": 8,
    "high": 2
  },
  "average_confidence": 0.78,
  "average_score": 0.32,
  "latest_scan": "2025-01-01T12:00:00.000Z"
}
```

---

### 7. Clear History

**DELETE** `/history`

Clear all scan history.

**Response (200):**
```json
{
  "message": "History cleared successfully",
  "status": "success"
}
```

---

## Data Models

### Scan Result

```typescript
{
  id: string;              // Unique identifier
  risk: "Low" | "Medium" | "High";  // Risk level
  confidence: number;      // 0.0 - 1.0
  score: number;          // 0.0 - 1.0
  features: {
    eye_asymmetry: number;
    mouth_asymmetry: number;
    nose_deviation: number;
    face_tilt: number;
    symmetry_ratio: number;
  };
  timestamp: string;      // ISO 8601 format
  disclaimer: string;
}
```

### Statistics

```typescript
{
  total_scans: number;
  risk_distribution: {
    low: number;
    medium: number;
    high: number;
  };
  average_confidence: number;
  average_score: number;
  latest_scan: string | null;
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid input, no face detected) |
| 404 | Not Found (scan ID not found) |
| 500 | Internal Server Error |

---

## Rate Limiting

**Current:** No rate limiting  
**Recommended for Production:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## CORS

**Allowed Origins:** 
- Development: `*` (all origins)
- Production: Specify your frontend domain

**Allowed Methods:** GET, POST, DELETE  
**Allowed Headers:** Content-Type, Authorization

---

## Best Practices

### Request Guidelines

1. **Image Quality:**
   - Resolution: At least 640x480
   - Format: JPG or PNG
   - Size: Under 10MB
   - Lighting: Well-lit, even lighting
   - Subject: Single face, front-facing

2. **Error Handling:**
   ```javascript
   try {
     const result = await scanImage(imageFile);
     // Handle success
   } catch (error) {
     // Handle error
     console.error(error.message);
   }
   ```

3. **Retry Logic:**
   ```javascript
   async function scanWithRetry(imageFile, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await scanImage(imageFile);
       } catch (error) {
         if (i === maxRetries - 1) throw error;
         await new Promise(r => setTimeout(r, 1000 * (i + 1)));
       }
     }
   }
   ```

---

## Examples

### Full Scan Workflow

```javascript
// 1. Check service status
const status = await fetch('http://localhost:8000/api/scan/status');
console.log(await status.json());

// 2. Upload image
const formData = new FormData();
formData.append('image', imageFile);

const scanResponse = await fetch('http://localhost:8000/api/scan/image', {
  method: 'POST',
  body: formData
});

const result = await scanResponse.json();
console.log('Risk Level:', result.risk);

// 3. Get history
const history = await fetch('http://localhost:8000/api/history');
console.log(await history.json());

// 4. Get statistics
const stats = await fetch('http://localhost:8000/api/history/stats/summary');
console.log(await stats.json());
```

### Python Client Example

```python
import requests

# Scan image
with open('face.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post(
        'http://localhost:8000/api/scan/image',
        files=files
    )
    result = response.json()
    print(f"Risk: {result['risk']}")

# Get history
response = requests.get('http://localhost:8000/api/history')
history = response.json()
print(f"Total scans: {len(history)}")
```

---

## WebSocket Support

**Status:** Not currently implemented  
**Future Enhancement:** Real-time scan updates via WebSocket

---

## Webhooks

**Status:** Not currently implemented  
**Future Enhancement:** Webhook notifications for high-risk scans

---

## SDK Libraries

### JavaScript/TypeScript
```javascript
import { NeuroScanClient } from 'neuroscan-client';

const client = new NeuroScanClient('http://localhost:8000/api');
const result = await client.scanImage(imageFile);
```

**Note:** Official SDK coming soon.

---

## Testing

### Unit Tests
```bash
cd backend
pytest tests/test_api.py
```

### Integration Tests
```bash
pytest tests/test_integration.py
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/scan/status
```

---

## Changelog

### v1.0.0 (2025-01-01)
- Initial release
- Basic scan functionality
- History management
- Statistics endpoint

---

## Support

For API issues or questions:
- GitHub Issues: [Link]
- Email: api-support@neuroscan.ai
- Documentation: [Link]

---

## License

MIT License - See LICENSE file for details

---

*Last Updated: December 29, 2025*  
*API Version: 1.0.0*
