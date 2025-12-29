import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload, BarChart3, Shield, Zap, Heart } from 'lucide-react';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-semibold mb-6">
            🏆 Microsoft Imagine Cup 2025
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Early Stroke Risk <span className="text-primary-600">Screening</span>
            <br />
            Using Your <span className="text-primary-600">Smartphone</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            NeuroScan AI analyzes facial asymmetry in under 5 seconds to provide
            pre-diagnostic stroke risk assessment using advanced AI technology.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={() => navigate('/scan')}
              className="btn-primary flex items-center space-x-2 text-lg"
            >
              <Camera className="w-6 h-6" />
              <span>Start Scan Now</span>
            </button>
            
            <button
              onClick={() => navigate('/dashboard')}
              className="btn-secondary flex items-center space-x-2 text-lg"
            >
              <BarChart3 className="w-6 h-6" />
              <span>View Dashboard</span>
            </button>
          </div>

          {/* Trust indicators */}
          <div className="mt-12 flex flex-wrap justify-center gap-8 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-primary-600" />
              <span>Privacy Protected</span>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-primary-600" />
              <span>5-Second Scan</span>
            </div>
            <div className="flex items-center space-x-2">
              <Heart className="w-5 h-5 text-primary-600" />
              <span>Healthcare Innovation</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Camera className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                1. Capture
              </h3>
              <p className="text-gray-600">
                Take a quick photo using your webcam or upload an existing image
                of your face.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Activity className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                2. Analyze
              </h3>
              <p className="text-gray-600">
                AI analyzes facial asymmetry using MobileNet and facial landmark
                detection technology.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                3. Results
              </h3>
              <p className="text-gray-600">
                Get instant risk assessment (Low/Medium/High) with detailed
                feature analysis.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              Powered by Advanced AI
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="font-bold text-gray-900 mb-2">MobileNetV2</h3>
                <p className="text-gray-600 text-sm">
                  Transfer learning for efficient facial feature extraction
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="font-bold text-gray-900 mb-2">MediaPipe</h3>
                <p className="text-gray-600 text-sm">
                  468 facial landmarks for precise asymmetry detection
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="font-bold text-gray-900 mb-2">FastAPI Backend</h3>
                <p className="text-gray-600 text-sm">
                  High-performance Python API for real-time processing
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="font-bold text-gray-900 mb-2">React Frontend</h3>
                <p className="text-gray-600 text-sm">
                  Mobile-first responsive design for accessibility
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto">
          <div className="card bg-yellow-50 border-2 border-yellow-300">
            <div className="flex items-start space-x-4">
              <AlertCircle className="w-8 h-8 text-yellow-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-bold text-yellow-900 mb-3">
                  Important Medical Disclaimer
                </h3>
                <p className="text-gray-700 mb-4">
                  <strong>This application is a PRE-DIAGNOSTIC SCREENING TOOL ONLY.</strong>
                </p>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li>✓ Does NOT diagnose stroke or any medical condition</li>
                  <li>✓ Not a substitute for professional medical evaluation</li>
                  <li>✓ Designed for early awareness and screening purposes</li>
                  <li>✓ Always consult healthcare professionals for diagnosis</li>
                </ul>
                <p className="mt-4 text-sm font-semibold text-yellow-900">
                  If you experience stroke symptoms (sudden numbness, confusion,
                  vision problems, severe headache), seek emergency medical
                  attention immediately by calling emergency services.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Screen Your Stroke Risk?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Takes less than 5 seconds. Completely free.
          </p>
          <button
            onClick={() => navigate('/scan')}
            className="bg-white text-primary-600 hover:bg-gray-100 font-bold py-4 px-8 rounded-lg text-lg transition-colors duration-200 shadow-lg"
          >
            Start Your Scan Now
          </button>
        </div>
      </section>
    </div>
  );
};

// Import missing components
import { Activity, AlertCircle } from 'lucide-react';

export default Home;
