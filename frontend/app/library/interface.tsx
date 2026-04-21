export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Song {
  id: number;
  title: string;
  occasion: string;
  mood_tone: string;
  genre: string;
  singer_voice: string;
  meaning: string;
  song_durations: string;
}

export interface Library {
  id: number;
  user: User;
  songs: Song[];
  total_songs: number;
}