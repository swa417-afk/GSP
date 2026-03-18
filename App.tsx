import React, { useState, useEffect, useRef } from 'react';
import { SLIDES } from './constants';
import { SlideRenderer } from './components/SlideRenderer';
import { VeoModal } from './components/VeoModal';
import { GoogleGenAI } from "@google/genai";

export default function App() {
  const [hasStarted, setHasStarted] = useState(false);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [isFinished, setIsFinished] = useState(false);
  const [isVeoModalOpen, setIsVeoModalOpen] = useState(false);
  const [introVideoUrl, setIntroVideoUrl] = useState<string | null>(null);
  
  const audioRef = useRef<HTMLAudioElement>(null);

  // Auto-advance logic: 10 seconds per slide
  useEffect(() => {
    if (!hasStarted || isFinished || isVeoModalOpen) return;

    // Reset progress bar animation when slide changes (handled by key prop in render)
    
    const timer = setInterval(() => {
      if (currentSlideIndex < SLIDES.length - 1) {
        setCurrentSlideIndex(prev => prev + 1);
      } else {
        setIsFinished(true);
        // Fade out audio
        if (audioRef.current) {
          let vol = 0.2;
          const fadeOut = setInterval(() => {
            if (vol > 0) {
              vol -= 0.02;
              audioRef.current!.volume = Math.max(0, vol);
            } else {
              clearInterval(fadeOut);
              audioRef.current!.pause();
            }
          }, 200);
        }
      }
    }, 10000); // 10 seconds

    return () => clearInterval(timer);
  }, [hasStarted, currentSlideIndex, isFinished, isVeoModalOpen]);

  const handleStart = () => {
    setHasStarted(true);
    if (audioRef.current) {
      audioRef.current.volume = 0.2; // "Softly" as requested
      audioRef.current.play().catch(e => console.log("Audio play failed (user interaction needed):", e));
    }
  };

  const handleReplay = () => {
    setCurrentSlideIndex(0);
    setIsFinished(false);
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.volume = 0.2;
      audioRef.current.play();
    }
  };

  return (
    <div className="relative w-screen h-screen bg-black overflow-hidden flex flex-col">
      {/* Background Music */}
      {/* Note: In a real environment, place 'stranger.mp3' in your public folder. 
          Using a generic ambient placeholder for functionality. */}
      <audio 
        ref={audioRef} 
        loop 
        src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=twilight-119999.mp3" 
      />

      {/* Main Content Area */}
      <div className="flex-grow relative">
        {hasStarted && !isFinished ? (
          <SlideRenderer slide={SLIDES[currentSlideIndex]} />
        ) : isFinished ? (
           <div className="h-full w-full flex flex-col items-center justify-center bg-black animate-fadeIn text-center">
             <h2 className="text-4xl text-white font-bold mb-4">Presentation Complete</h2>
             <button 
               onClick={handleReplay}
               className="px-8 py-3 bg-green-600 hover:bg-green-500 text-white rounded-full font-semibold transition-all transform hover:scale-105"
             >
               Replay Video
             </button>
           </div>
        ) : (
          // Start Screen / Intro
          <div className="h-full w-full flex flex-col items-center justify-center bg-slate-900 relative">
             <div className="absolute inset-0 opacity-30 bg-[url('https://picsum.photos/1920/1080?blur=5')] bg-cover"></div>
             <div className="z-10 text-center max-w-2xl px-4">
                <h1 className="text-5xl font-bold text-white mb-6 tracking-tight">Glass Substrate Protocol</h1>
                <p className="text-xl text-slate-300 mb-10">Automated Video Presentation • 10s per slide</p>
                
                <div className="flex gap-4 justify-center">
                  <button 
                    onClick={handleStart}
                    className="px-10 py-4 bg-white text-slate-900 rounded-full font-bold text-lg hover:bg-green-400 transition-all shadow-xl flex items-center gap-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                    Play Video
                  </button>

                  <button 
                    onClick={() => setIsVeoModalOpen(true)}
                    className="px-6 py-4 bg-slate-800/80 backdrop-blur text-white border border-slate-600 rounded-full font-medium hover:bg-slate-700 transition-all"
                  >
                    ✨ Generate AI Intro
                  </button>
                </div>
             </div>
          </div>
        )}

        {/* Veo Generated Video Overlay (Optional enhancement) */}
        {introVideoUrl && !hasStarted && (
           <div className="absolute inset-0 z-0">
             <video src={introVideoUrl} autoPlay loop muted className="w-full h-full object-cover opacity-50"></video>
           </div>
        )}
      </div>

      {/* Control Bar / Progress */}
      {hasStarted && !isFinished && (
        <div className="h-16 bg-zinc-900 border-t border-zinc-800 flex items-center px-8 justify-between relative z-20">
           <div className="flex items-center gap-4">
              <span className="text-green-500 font-mono text-sm">REC</span>
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
              <span className="text-slate-400 text-sm">
                Slide {currentSlideIndex + 1} / {SLIDES.length}
              </span>
           </div>

           {/* Current Slide Timer Bar */}
           <div className="absolute bottom-0 left-0 h-1 bg-green-600/30 w-full">
              <div key={currentSlideIndex} className="h-full bg-green-500 animate-progress origin-left"></div>
           </div>
           
           <div className="flex gap-2">
             <button onClick={() => setCurrentSlideIndex(Math.max(0, currentSlideIndex - 1))} className="p-2 text-slate-400 hover:text-white">Previous</button>
             <button onClick={() => setCurrentSlideIndex(Math.min(SLIDES.length - 1, currentSlideIndex + 1))} className="p-2 text-slate-400 hover:text-white">Next</button>
           </div>
        </div>
      )}

      {/* Veo Modal */}
      <VeoModal 
        isOpen={isVeoModalOpen} 
        onClose={() => setIsVeoModalOpen(false)} 
        slideTitle={SLIDES[0].title || "Presentation Intro"}
        onVideoGenerated={setIntroVideoUrl}
      />
    </div>
  );
}