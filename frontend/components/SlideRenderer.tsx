import React from 'react';
import { SlideData } from '../types';

interface SlideRendererProps {
  slide: SlideData;
}

export const SlideRenderer: React.FC<SlideRendererProps> = ({ slide }) => {
  const commonClasses = "h-full w-full flex flex-col p-12 transition-all duration-500 animate-fadeIn";

  // Slide 1: Title Slide (Dark blue/matrix background theme)
  if (slide.type === 'title') {
    return (
      <div className={`${commonClasses} justify-center relative bg-gradient-to-br from-slate-900 to-slate-800 text-white overflow-hidden`}>
        {/* Abstract Background Effect */}
        <div className="absolute inset-0 opacity-20 bg-[url('https://picsum.photos/1920/1080?grayscale&blur=2')] bg-cover mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-grid-slate-700/[0.1] bg-[length:40px_40px]"></div>

        <div className="relative z-10 bg-slate-800/80 backdrop-blur-md p-10 rounded-r-xl border-l-4 border-green-500 shadow-2xl max-w-4xl">
          <h2 className="text-2xl font-light text-green-400 mb-4">{slide.title}</h2>
          <h1 className="text-5xl font-bold leading-tight mb-6">
            {slide.content[0]}
            <br />
            <span className="text-3xl font-medium text-slate-300 block mt-2">{slide.content[1]}</span>
          </h1>
        </div>
        
        <div className="absolute bottom-12 right-0 bg-slate-700/90 px-8 py-4 rounded-l-lg shadow-xl">
           <p className="text-xl font-semibold text-white">{slide.footer}</p>
        </div>
      </div>
    );
  }

  // Slide 11: End Slide
  if (slide.type === 'end') {
    return (
      <div className={`${commonClasses} items-center justify-center bg-zinc-900 text-center`}>
         <h1 className="text-6xl font-bold text-green-500 mb-12">{slide.title}</h1>
         <div className="space-y-4 text-xl text-slate-300">
            {slide.content.map((line, i) => (
              <p key={i} className={i === 0 ? "text-2xl font-bold text-white mb-4" : ""}>{line}</p>
            ))}
         </div>
         <div className="absolute bottom-10 right-10 opacity-50">
           <img src="https://picsum.photos/100/100?random=logo" alt="Logo" className="w-24 h-24 rounded-lg mix-blend-luminosity" />
         </div>
      </div>
    );
  }

  // Visual/Graphic Heavy Slide (Slide 5)
  if (slide.type === 'visual') {
    return (
      <div className={`${commonClasses} bg-slate-900 relative`}>
        <div className="absolute left-0 top-0 bottom-0 w-1/2 bg-gradient-to-r from-green-900/20 to-transparent"></div>
         {/* Simulate the Geometric shape */}
        <div className="absolute left-10 top-1/2 -translate-y-1/2 w-64 h-64 border-4 border-green-500/50 rotate-45 animate-pulse"></div>
        <div className="absolute left-10 top-1/2 -translate-y-1/2 w-64 h-64 border-2 border-cyan-500/30 rotate-12"></div>

        <div className="ml-auto w-1/2 flex flex-col justify-center h-full pl-10 z-10">
          <div className="border-2 border-green-500 p-4 inline-block mb-8 w-fit">
            <h2 className="text-3xl font-bold text-green-500 uppercase">{slide.title}</h2>
          </div>
          <div className="space-y-8">
            {slide.content.map((text, i) => (
              <p key={i} className="text-xl text-slate-200 leading-relaxed border-l-2 border-slate-600 pl-4">
                {text}
              </p>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Standard Content Slides
  return (
    <div className={`${commonClasses} bg-zinc-900`}>
      <div className="flex flex-col h-full relative z-10">
        {slide.title && (
            <div className="mb-8 border-l-4 border-green-500 pl-6 py-2">
                <h2 className="text-4xl font-bold text-white">{slide.title}</h2>
            </div>
        )}
        
        {/* Dynamic Layout based on content length */}
        <div className={`flex flex-col gap-6 justify-center flex-grow ${slide.type === 'references' ? 'text-sm' : 'text-2xl'}`}>
            {slide.content.map((text, i) => (
               <div key={i} className={`bg-slate-800/50 p-6 rounded-lg border border-slate-700 shadow-sm hover:border-green-500/50 transition-colors ${slide.content.length > 4 ? 'py-3' : 'py-6'}`}>
                 <p className="text-slate-200 leading-relaxed">
                   {slide.type === 'references' ? text : text}
                 </p>
               </div>
            ))}
        </div>
        
        {/* Visual Abstract Decor for Slide 2 etc */}
        {!slide.title && slide.content[0].includes("GLASS SUBSTRATE") && (
             <div className="absolute -right-20 -top-20 w-[40rem] h-[40rem] bg-green-500 rounded-full blur-3xl opacity-10 pointer-events-none"></div>
        )}
      </div>
      
      {/* Footer Page Number */}
      <div className="absolute bottom-4 right-6 text-slate-600 font-mono">
        {slide.id}
      </div>
    </div>
  );
};