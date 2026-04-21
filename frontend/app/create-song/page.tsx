'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import PromptForm from './prompt';

export default function SongCreatePage() {
  const router = useRouter();
  const [selectedMode, setSelectedMode] = useState<'mock' | 'suno' | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Convert minutes to HH:MM:SS format
  const convertDurationToTimeField = (minutes: string): string => {
    const totalSeconds = Math.round(parseFloat(minutes) * 60);
    const hours = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;
    return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const handleFormSubmit = async (data: {
    title: string;
    occasion: string;
    mood_tone: string;
    genre: string;
    singer_voice: 'male' | 'female';
    meaning: string;
    song_durations: string;
  }) => {
    if (!selectedMode) return;
    
    setError('');
    setLoading(true);

    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      if (!user.id) {
        setError('User not found. Please login first.');
        setLoading(false);
        return;
      }

      // Convert minutes to HH:MM:SS if needed
      let duration = data.song_durations;
      if (!duration.includes(':')) {
        duration = convertDurationToTimeField(data.song_durations);
      }

      // Map form data directly to backend Song model
      const songData = {
        title: data.title,
        occasion: data.occasion,
        mood_tone: data.mood_tone,
        genre: data.genre,
        singer_voice: data.singer_voice,
        meaning: data.meaning,
        song_durations: duration,
        strategy: selectedMode,
      };

      const response = await fetch('http://127.0.0.1:8000/song/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(songData),
      });

      const result = await response.json();

      if (!response.ok) {
        setError(result.error || 'Failed to create song');
        setLoading(false);
        return;
      }

      // Add song to library
      const libraryResponse = await fetch(`http://127.0.0.1:8000/library/${user.id}/songs/add/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ song_id: result.id }),
      });

      if (!libraryResponse.ok) {
        setError('Song created but failed to add to library');
        setLoading(false);
        return;
      }

      // Success - redirect to library
      router.push('/library');
    } catch (err) {
      setError('An error occurred while creating the song');
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      {/* Back Button */}
      <button
        onClick={() => router.push('/library')}
        style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          padding: '10px 20px',
          backgroundColor: '#6c757d',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        ← Back to Library
      </button>

      {/* Main Content */}
      <div style={{ maxWidth: '600px', margin: '80px auto 0' }}>
        <h1 style={{ marginBottom: '30px' }}>Create a Song</h1>

        {error && <div style={{ padding: '15px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '20px' }}>{error}</div>}

        {/* Mode Selection */}
        <div style={{ marginBottom: '40px' }}>
          <h2 style={{ marginBottom: '20px' }}>Choose Generation Method:</h2>
          <div style={{ display: 'flex', gap: '15px' }}>
            <button
              onClick={() => setSelectedMode('mock')}
              disabled={loading}
              style={{
                flex: 1,
                padding: '20px',
                backgroundColor: selectedMode === 'mock' ? '#007bff' : '#e9ecef',
                color: selectedMode === 'mock' ? 'white' : '#333',
                border: selectedMode === 'mock' ? '2px solid #0056b3' : '2px solid #dee2e6',
                borderRadius: '8px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: selectedMode === 'mock' ? 'bold' : 'normal',
                transition: 'all 0.3s ease',
                opacity: loading ? 0.6 : 1,
              }}
            >
              Mock (Test)
            </button>
            <button
              onClick={() => setSelectedMode('suno')}
              disabled={loading}
              style={{
                flex: 1,
                padding: '20px',
                backgroundColor: selectedMode === 'suno' ? '#28a745' : '#e9ecef',
                color: selectedMode === 'suno' ? 'white' : '#333',
                border: selectedMode === 'suno' ? '2px solid #1e7e34' : '2px solid #dee2e6',
                borderRadius: '8px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: selectedMode === 'suno' ? 'bold' : 'normal',
                transition: 'all 0.3s ease',
                opacity: loading ? 0.6 : 1,
              }}
            >
              Suno (Real)
            </button>
          </div>
        </div>

        {/* Prompt Form */}
        {selectedMode && (
          <div
            style={{
              padding: '30px',
              backgroundColor: '#f8f9fa',
              borderRadius: '8px',
              border: `2px solid ${selectedMode === 'mock' ? '#007bff' : '#28a745'}`,
              marginTop: '20px',
            }}
          >
            <p style={{ margin: '0 0 20px 0', fontSize: '16px', fontWeight: 'bold' }}>
              {selectedMode === 'mock' ? 'Mock (Test) Mode' : 'Suno (Real) Mode'}
            </p>
            <PromptForm mode={selectedMode} onSubmit={handleFormSubmit} />
          </div>
        )}
      </div>
    </div>
  );
}
