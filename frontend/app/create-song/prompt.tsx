'use client';
import { useState } from 'react';

interface PromptFormProps {
  mode: 'mock' | 'suno';
  onSubmit: (data: {
    title: string;
    occasion: string;
    mood_tone: string;
    genre: string;
    singer_voice: 'male' | 'female';
    meaning: string;
    song_durations: string;
  }) => void;
}

export default function PromptForm({ mode, onSubmit }: PromptFormProps) {
  const [title, setTitle] = useState('');
  const [occasion, setOccasion] = useState('');
  const [moodTone, setMoodTone] = useState('');
  const [genre, setGenre] = useState('');
  const [singerVoice, setSingerVoice] = useState<'male' | 'female'>('male');
  const [meaning, setMeaning] = useState('');
  const [songDurations, setSongDurations] = useState('3');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim() || !occasion.trim() || !moodTone.trim() || !genre.trim() || !meaning.trim() || !songDurations) {
      alert('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      onSubmit({ 
        title, 
        occasion, 
        mood_tone: moodTone, 
        genre, 
        singer_voice: singerVoice, 
        meaning, 
        song_durations: songDurations 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="title" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Song Title
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter song title"
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="occasion" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Occasion
        </label>
        <input
          id="occasion"
          type="text"
          value={occasion}
          onChange={(e) => setOccasion(e.target.value)}
          placeholder="e.g., Birthday, Wedding, Graduation"
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="moodTone" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Mood / Tone
        </label>
        <input
          id="moodTone"
          type="text"
          value={moodTone}
          onChange={(e) => setMoodTone(e.target.value)}
          placeholder="e.g., Happy, Sad, Energetic, Romantic"
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="genre" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Genre
        </label>
        <input
          id="genre"
          type="text"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          placeholder="e.g., Pop, Rock, Jazz, Hip-Hop"
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="meaning" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Meaning / Message
        </label>
        <textarea
          id="meaning"
          value={meaning}
          onChange={(e) => setMeaning(e.target.value)}
          placeholder="What is the song about? What message or story should it convey?"
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
            minHeight: '100px',
            fontFamily: 'Arial, sans-serif',
            resize: 'vertical',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="songDurations" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Duration (minutes)
        </label>
        <input
          id="songDurations"
          type="number"
          min="1"
          max="10"
          step="0.5"
          value={songDurations}
          onChange={(e) => setSongDurations(e.target.value)}
          required
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="singerVoice" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          Singer Voice
        </label>
        <select
          id="singerVoice"
          value={singerVoice}
          onChange={(e) => setSingerVoice(e.target.value as 'male' | 'female')}
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '14px',
            boxSizing: 'border-box',
            backgroundColor: 'white',
            cursor: 'pointer',
          }}
        >
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={loading}
        style={{
          width: '100%',
          padding: '12px',
          backgroundColor: mode === 'mock' ? '#007bff' : '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
          fontSize: '16px',
          fontWeight: 'bold',
          opacity: loading ? 0.7 : 1,
          transition: 'opacity 0.2s ease',
        }}
      >
        {loading ? 'Creating...' : `Create with ${mode === 'mock' ? 'Mock' : 'Suno'}`}
      </button>
    </form>
  );
}
