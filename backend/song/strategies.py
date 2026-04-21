from abc import ABC, abstractmethod
import requests
from django.conf import settings
import json
import os
from random import choices

audio_choices = ["honse_drift.mp4", "suckanegad.mp3"]

class SongGeneratorStrategy(ABC):
    def _get_storage_dir(self, song):
        """Get storage directory path outside of backend folder"""
        # Get the parent directory of backend (project root)
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)
        song_dir = os.path.join(project_root, "storage", "song", str(song.id))
        return song_dir
    
    def _set_song_path(self, song):
        """Helper method to set the song storage path"""
        song.song_path = f"storage/song/{song.id}"
    
    def _download_and_save_audio(self, song, audio_url):
        """
        Download audio from URL and save it to storage/song/{song_id}/
        Supports both mp3 and mp4 formats.
        
        Args:
            song: Song instance
            audio_url: URL to download audio from
        """
        # Try to determine format from URL or default to mp3
        if audio_url.endswith('.mp4') or 'mp4' in audio_url.lower():
            return self._download_and_save_file(song, audio_url, "audio.mp4")
        else:
            return self._download_and_save_file(song, audio_url, "audio.mp3")
    
    def _download_and_save_thumbnail(self, song, thumbnail_url):
        """
        Download thumbnail from URL and save it to storage/song/{song_id}/thumbnail.jpg
        
        Args:
            song: Song instance
            thumbnail_url: URL to download thumbnail from
        """
        return self._download_and_save_file(song, thumbnail_url, "thumbnail.jpg")
    
    def _download_and_save_file(self, song, file_url, filename):
        """
        Generic method to download any file and save it to storage/song/{song_id}/
        
        Args:
            song: Song instance
            file_url: URL to download file from
            filename: Filename to save as (e.g., 'audio.mp3', 'thumbnail.jpg')
        """
        try:
            # Create storage directory if it doesn't exist (outside backend folder)
            song_dir = self._get_storage_dir(song)
            os.makedirs(song_dir, exist_ok=True)
            
            # Download the file
            response = requests.get(file_url, timeout=30)
            response.raise_for_status()
            
            # Save to file
            file_path = os.path.join(song_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return file_path
        except Exception as e:
            print(f"Error downloading and saving {filename}: {e}")
            return None
    
    @abstractmethod
    def generate_song(self, song):
        """
        Generate a song for the given song instance.
        Should update song.task_id, song.generation_status, and song.audio_url as appropriate.
        """
        pass

    @abstractmethod
    def check_status(self, song):
        """
        Check the status of song generation.
        Should update song.generation_status and song.audio_url if complete.
        """
        pass


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    def __init__(self):
        # Get mockup files from storage/mockup
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(backend_dir)
        self.MOCKUP_AUDIO = os.path.join(project_root, "storage", "mockup", "audio", f"{str(choices(audio_choices)[0])}")
        self.MOCKUP_THUMBNAIL = os.path.join(project_root, "storage", "mockup", "thumbnail", "mockup_thumbnail.png")

    def generate_song(self, song):
        # Mock implementation - no external API call
        self._set_song_path(song)
        song.task_id = "mock-task-123"
        song.generation_status = "SUCCESS"
        
        # Copy mockup files to storage (outside backend folder)
        song_dir = self._get_storage_dir(song)
        os.makedirs(song_dir, exist_ok=True)
        
        try:
            # Copy mock audio file - preserve the original format
            if os.path.exists(self.MOCKUP_AUDIO):
                # Get the file extension from mockup audio
                _, file_ext = os.path.splitext(self.MOCKUP_AUDIO)
                if not file_ext:
                    file_ext = ".mp3"  # Default to mp3 if no extension
                
                audio_dest = os.path.join(song_dir, f"audio{file_ext}")
                with open(self.MOCKUP_AUDIO, 'rb') as src:
                    with open(audio_dest, 'wb') as dst:
                        dst.write(src.read())
                song.audio_url = audio_dest
            
            # Copy mock thumbnail file
            if os.path.exists(self.MOCKUP_THUMBNAIL):
                # Get the file extension from mockup thumbnail
                _, thumb_ext = os.path.splitext(self.MOCKUP_THUMBNAIL)
                if not thumb_ext:
                    thumb_ext = ".jpg"  # Default to jpg if no extension
                    
                thumbnail_dest = os.path.join(song_dir, f"thumbnail{thumb_ext}")
                with open(self.MOCKUP_THUMBNAIL, 'rb') as src:
                    with open(thumbnail_dest, 'wb') as dst:
                        dst.write(src.read())
        except Exception as e:
            print(f"Error copying mockup files: {e}")
        
        song.save()

    def check_status(self, song):
        # Mock is always successful
        if song.generation_status != "SUCCESS":
            self._set_song_path(song)
            song.generation_status = "SUCCESS"
            song_dir = self._get_storage_dir(song)
            
            # Determine audio file extension from mockup
            _, file_ext = os.path.splitext(self.MOCKUP_AUDIO)
            if not file_ext:
                file_ext = ".mp3"  # Default to mp3 if no extension
            
            song.audio_url = os.path.join(song_dir, f"audio{file_ext}")
            song.save()


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    API_BASE_URL = "https://api.sunoapi.org/api/v1"
    GENERATE_ENDPOINT = f"{API_BASE_URL}/generate"
    STATUS_ENDPOINT = f"{API_BASE_URL}/generate/record-info"

    def __init__(self):
        # Get token from settings
        self.token = getattr(settings, 'SUNO_API_TOKEN', None)
        if not self.token:
            raise ValueError("SUNO_API_TOKEN not configured in settings")

    def generate_song(self, song):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # Prepare the payload based on song fields
        payload = {
            "prompt": f"Create a song titled '{song.title}' for {song.occasion} with {song.mood_tone} mood in {song.genre} genre. Singer voice: {song.singer_voice}. Meaning: {song.meaning}",
            "duration": str(song.song_durations),  # Assuming it's in HH:MM:SS format, but API might expect seconds
            # Add other required fields as per API docs
        }

        response = requests.post(self.GENERATE_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            self._set_song_path(song)
            song.task_id = data.get('taskId')  # Assuming the response has 'taskId'
            song.generation_status = "PENDING"
            song.save()
        else:
            raise Exception(f"Failed to start generation: {response.text}")

    def check_status(self, song):
        if not song.task_id:
            return

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        params = {
            'taskId': song.task_id
        }

        response = requests.get(self.STATUS_ENDPOINT, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            song.generation_status = status

            # Set song_path if not already set
            if not song.song_path:
                self._set_song_path(song)

            if status == "SUCCESS":
                # Download audio file
                audio_url = data.get('audio_url')
                if audio_url:
                    audio_path = self._download_and_save_audio(song, audio_url)
                    if audio_path:
                        song.audio_url = audio_path
                
                # Download thumbnail/image
                thumbnail_url = data.get('image_url') or data.get('thumbnail_url')
                if thumbnail_url:
                    self._download_and_save_thumbnail(song, thumbnail_url)

            song.save()
        else:
            raise Exception(f"Failed to check status: {response.text}")


def get_song_generator_strategy(strategy_name=None):
    """
    Factory function to get the active song generator strategy.
    
    Args:
        strategy_name: Optional strategy name ('mock' or 'suno'). 
                      If None, uses GENERATOR_STRATEGY setting.
    """
    if strategy_name is None:
        strategy_name = getattr(settings, 'GENERATOR_STRATEGY', 'mock').lower()
    else:
        strategy_name = strategy_name.lower()

    if strategy_name == 'mock':
        return MockSongGeneratorStrategy()
    elif strategy_name == 'suno':
        return SunoSongGeneratorStrategy()
    else:
        raise ValueError(f"Invalid strategy: {strategy_name}. Must be 'mock' or 'suno'.")
