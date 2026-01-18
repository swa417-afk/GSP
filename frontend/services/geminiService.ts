import { GoogleGenAI } from "@google/genai";

// Define a local interface for the aistudio object to ensure type safety when casting
interface AIStudio {
  hasSelectedApiKey: () => Promise<boolean>;
  openSelectKey: () => Promise<void>;
}

/**
 * Ensures the user has selected an API key via AI Studio.
 */
export const ensureApiKey = async (): Promise<string | undefined> => {
  // Use type assertion to avoid conflicts with global type definitions of window.aistudio
  const win = window as any;
  
  if (win.aistudio) {
    const aistudio = win.aistudio as AIStudio;
    const hasKey = await aistudio.hasSelectedApiKey();
    if (!hasKey) {
      await aistudio.openSelectKey();
    }
    // We assume the key is injected into process.env.API_KEY by the environment
    // after selection.
    return process.env.API_KEY; 
  }
  return process.env.API_KEY;
};

export const generateIntroVideo = async (prompt: string): Promise<string | null> => {
  try {
    await ensureApiKey();
    
    // Create instance immediately before use to ensure key is fresh
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    
    // We use Veo 3.1 Fast for quick preview generation
    let operation = await ai.models.generateVideos({
      model: 'veo-3.1-fast-generate-preview',
      prompt: prompt,
      config: {
        numberOfVideos: 1,
        resolution: '720p',
        aspectRatio: '16:9' 
      }
    });

    // Poll for completion
    while (!operation.done) {
      await new Promise(resolve => setTimeout(resolve, 5000));
      operation = await ai.operations.getVideosOperation({ operation: operation });
      console.log('Generating video...');
    }

    const videoUri = operation.response?.generatedVideos?.[0]?.video?.uri;
    
    if (videoUri) {
        // Append API key for download access as per docs
        return `${videoUri}&key=${process.env.API_KEY}`;
    }
    
    return null;

  } catch (error) {
    console.error("Video generation failed:", error);
    throw error;
  }
};