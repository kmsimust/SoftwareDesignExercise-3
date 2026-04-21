'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { User, Song, Library } from './interface';

export default function LibraryPage() {
  const router = useRouter();
  const [library, setLibrary] = useState<Library | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLibrary = async () => {
      try {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          setError('User not found. Please login first.');
          setLoading(false);
          return;
        }

        const user = JSON.parse(userStr);
        const response = await fetch(`http://127.0.0.1:8000/library/${user.id}/`);
        
        if (!response.ok) {
          setError('Failed to load library');
          setLoading(false);
          return;
        }

        const data = await response.json();
        setLibrary(data);
      } catch (err) {
        setError('An error occurred while loading library');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchLibrary();
  }, []);

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading library...</div>;
  }

  if (error) {
    return <div style={{ padding: '20px', color: 'red' }}>{error}</div>;
  }

  if (!library) {
    return <div style={{ padding: '20px' }}>No library found</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Back Button */}
      <button
        onClick={() => router.push('/create-song')}
        style={{
          top: '20px',
          left: '20px',
          padding: '10px 20px',
          backgroundColor: '#0088ff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        ← Create
      </button>

      <div style={{ marginBottom: '20px' }}>
        <h2>Songs ({library.total_songs})</h2>
        {library.total_songs === 0 ? (
          <p>No songs in your library yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f0f0f0', borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '10px', textAlign: 'left' }}> </th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Title</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Genre</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Mood/Tone</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Duration</th>
              </tr>
            </thead>
            <tbody>
              {library.songs.map((song) => (
                <tr 
                  key={song.id}
                  onClick={() => router.push(`/watch?song_id=${song.id}`)}
                  style={{ 
                    borderBottom: '1px solid #ddd',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f5f5f5'}
                  onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                >
                  <td style={{ padding: '10px' }}>
                    <img
                      src={`http://localhost:8000/storage/song/${song.id}/thumbnail.jpg`}
                      alt={`${song.title} thumbnail`}
                      style={{ width: '80px', height: '80px', objectFit: 'cover' }}
                    />
                  </td>
                  <td style={{ padding: '10px' }}>{song.title}</td>
                  <td style={{ padding: '10px' }}>{song.genre}</td>
                  <td style={{ padding: '10px' }}>{song.mood_tone}</td>
                  <td style={{ padding: '10px' }}>{song.song_durations}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}