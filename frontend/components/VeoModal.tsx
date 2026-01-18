import React, { useState } from 'react';
import { generateIntroVideo } from '../services/geminiService';

interface VeoModalProps {
  isOpen: boolean;
  onClose: () => void;
  slideTitle: string;
  onVideoGenerated?: (url: string) => void;
}

export const VeoModal: React.FC<VeoModalProps> = ({ isOpen, onClose, slideTitle, onVideoGenerated }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const prompt = `Cinematic, futuristic abstract glass substrate background with data streams, high quality, 4k, suitable for title slide: ${slideTitle}`;
      const videoUrl = await generateIntroVideo(prompt);
      if (videoUrl && onVideoGenerated) {
        onVideoGenerated(videoUrl);
        onClose();
      } else {
        setError("Failed to generate video. Please try again.");
      }
    } catch (err) {
      setError("An error occurred during generation.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl relative overflow-hidden">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <span className="text-2xl">✨</span> Veo Video Generator
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="space-y-4">
          <p className="text-slate-300">
            Generate a custom AI video background for your title slide using Google's Veo model.
          </p>
          
          <div className="bg-slate-800 p-4 rounded-lg border border-slate-700">
            <label className="text-xs text-slate-400 uppercase font-semibold mb-2 block">Prompt</label>
            <p className="text-sm text-green-400 font-mono">
              "Cinematic, futuristic abstract glass substrate background..."
            </p>
          </div>

          {error && (
            <div className="p-3 bg-red-900/50 border border-red-500/50 text-red-200 text-sm rounded">
              {error}
            </div>
          )}

          <button
            onClick={handleGenerate}
            disabled={loading}
            className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${
              loading 
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-lg hover:shadow-purple-500/25'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating (takes ~1 min)...
              </span>
            ) : (
              "Generate Video"
            )}
          </button>
        </div>
        
        {/* Background glow */}
        <div className="absolute -top-20 -right-20 w-64 h-64 bg-purple-600/20 rounded-full blur-3xl pointer-events-none"></div>
      </div>
    </div>
  );
};