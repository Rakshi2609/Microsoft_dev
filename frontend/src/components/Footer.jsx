import React from 'react';
import { Heart, Github, Mail } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-3">
              NeuroScan AI
            </h3>
            <p className="text-sm text-gray-400">
              Smartphone-based early stroke risk screening using facial
              asymmetry analysis. A pre-diagnostic screening tool for better
              health awareness.
            </p>
          </div>

          {/* Disclaimer */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-3">
              Important Notice
            </h3>
            <p className="text-sm text-gray-400">
              This application does not diagnose stroke. It is a screening tool
              only. Always consult healthcare professionals for medical advice.
            </p>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-3">
              Imagine Cup 2025
            </h3>
            <div className="flex items-center space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-primary-400 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="mailto:contact@neuroscan.ai"
                className="hover:text-primary-400 transition-colors"
              >
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800 mt-8 pt-6 text-center">
          <p className="text-sm text-gray-400">
            Made with <Heart className="inline w-4 h-4 text-red-500" /> for
            Microsoft Imagine Cup 2025
          </p>
          <p className="text-xs text-gray-500 mt-2">
            © 2025 NeuroScan AI. Healthcare Innovation Project.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
