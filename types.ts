export interface SlideData {
  id: number;
  title?: string;
  content: string[];
  footer?: string;
  type: 'title' | 'content' | 'visual' | 'references' | 'end';
  imagePlaceholder?: string;
}

export enum PlayState {
  PAUSED,
  PLAYING,
  ENDED
}
