# NeuroScan AI - Frontend

React frontend for NeuroScan AI stroke risk screening application.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:8000/api
```

## Features

- 📸 Live camera capture
- 📤 Image upload
- 📊 Results visualization
- 📈 Scan history dashboard
- 📱 Mobile-responsive design
- 🎨 Tailwind CSS styling

## Project Structure

```
src/
├── components/       # Reusable components
├── pages/           # Page components
├── api.js           # API client
├── App.jsx          # Main app component
└── main.jsx         # Entry point
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Camera Permissions

Application requires camera permissions for live scanning. Ensure:
- HTTPS connection (or localhost for development)
- Camera access granted in browser
- Valid SSL certificate (production)
