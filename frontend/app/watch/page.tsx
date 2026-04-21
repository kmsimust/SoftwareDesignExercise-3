'use client';
import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

interface Song {
  id: number;
  title: string;
  occasion: string;
  mood_tone: string;
  genre: string;
  singer_voice: string;
  meaning: string;
  song_durations: string;
  strategy: string;
  generation_status: string;
  task_id: string;
}

export default function WatchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const songId = searchParams.get('song_id');
  
  const [song, setSong] = useState<Song | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!songId) {
      setError('No song ID provided. Please use ?song_id=<id>');
      setLoading(false);
      return;
    }

    const fetchSong = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/song/${songId}/`);
        
        if (!response.ok) {
          setError('Song not found');
          setLoading(false);
          return;
        }

        const data = await response.json();
        setSong(data);
      } catch (err) {
        setError('Failed to load song');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSong();
  }, [songId]);

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading song...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <p style={{ color: 'red' }}>{error}</p>
        <button 
          onClick={() => router.push('/library')}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginTop: '10px'
          }}
        >
          Back to Library
        </button>
      </div>
    );
  }

  if (!song) {
    return <div style={{ padding: '20px' }}>Song not found</div>;
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', gap: '30px', marginBottom: '30px' }}>
        {/* Video Player Area */}
        <div style={{ flex: 1 }}>
          <div style={{
            backgroundColor: '#000',
            borderRadius: '8px',
            overflow: 'hidden',
            marginBottom: '16px'
          }}>
            <img
              src={`http://localhost:8000/storage/song/${song.id}/thumbnail.jpg`}
              alt={`${song.title} thumbnail`}
              style={{
                width: '100%',
                height: 'auto',
                display: 'block',
                minHeight: '300px',
                objectFit: 'cover'
              }}
              onError={(e) => {
                (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23333" width="100" height="100"/%3E%3C/svg%3E';
              }}
            />
          </div>

          {/* Audio Player */}
          <div style={{ marginBottom: '16px' }}>
            <audio
              controls
              style={{
                width: '100%',
                borderRadius: '4px'
              }}
            >
              <source
                src={`http://localhost:8000/storage/song/${song.id}/audio.mp3`}
                type="audio/mpeg"
              />
              <source
                src={`http://localhost:8000/storage/song/${song.id}/audio.mp4`}
                type="audio/mp4"
              />
              Your browser does not support the audio element.
            </audio>
          </div>
        </div>

        {/* Song Info Sidebar */}
        <div style={{ flex: 0.4, minWidth: '250px' }}>
          <h1 style={{ fontSize: '24px', marginBottom: '8px' }}>{song.title}</h1>
          
          <div style={{
            backgroundColor: '#f5f5f5',
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '16px'
          }}>
            <div style={{ marginBottom: '12px' }}>
              <strong>Status:</strong>
              <span style={{
                marginLeft: '8px',
                padding: '4px 8px',
                borderRadius: '4px',
                backgroundColor: song.generation_status === 'SUCCESS' ? '#d4edda' : '#fff3cd',
                color: song.generation_status === 'SUCCESS' ? '#155724' : '#856404'
              }}>
                {song.generation_status}
              </span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Duration:</strong>
              <span style={{ marginLeft: '8px' }}>{song.song_durations}</span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Genre:</strong>
              <span style={{ marginLeft: '8px' }}>{song.genre}</span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Mood/Tone:</strong>
              <span style={{ marginLeft: '8px' }}>{song.mood_tone}</span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Occasion:</strong>
              <span style={{ marginLeft: '8px' }}>{song.occasion}</span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Singer Voice:</strong>
              <span style={{ marginLeft: '8px', textTransform: 'capitalize' }}>
                {song.singer_voice}
              </span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Strategy:</strong>
              <span style={{ marginLeft: '8px', textTransform: 'capitalize' }}>
                {song.strategy}
              </span>
            </div>
          </div>

          <div style={{
            backgroundColor: '#f9f9f9',
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '16px'
          }}>
            <strong>Meaning:</strong>
            <p style={{ marginTop: '8px', lineHeight: '1.6' }}>{song.meaning}</p>
          </div>

          <button
            onClick={() => router.push('/library')}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            Back to Library
          </button>
        </div>
      </div>
    </div>
  );
}
