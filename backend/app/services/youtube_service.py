import re
from typing import Tuple, List, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import httpx
from bs4 import BeautifulSoup

class YouTubeService:
    def __init__(self):
        pass
        
    async def extract_video_id(self, url: str) -> str:
        """
        Extract the YouTube video ID from a URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video ID string
            
        Raises:
            ValueError: If the URL is not a valid YouTube URL
        """
        # Pattern for YouTube video IDs in various URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/e\/|youtube\.com\/watch\?.*v=|youtube\.com\/watch\?.*&v=)([^&\n?#]+)',
            r'(?:youtube\.com\/shorts\/)([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("Invalid YouTube URL. Could not extract video ID.")
    
    async def get_video_title(self, video_id: str) -> str:
        """
        Get the title of a YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video title
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://www.youtube.com/watch?v={video_id}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title_tag = soup.find('title')
                    if title_tag:
                        # Remove " - YouTube" from the title
                        title = title_tag.text.replace(' - YouTube', '')
                        return title
                        
            # Fallback
            return f"YouTube Video {video_id}"
        except Exception as e:
            print(f"Error fetching video title: {str(e)}")
            return f"YouTube Video {video_id}"
    
    async def get_transcript(self, video_id: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Get the transcript of a YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Tuple of (full transcript text, raw transcript data)
            
        Raises:
            Exception: If there's an error fetching the transcript
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get English transcript first
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                # If English not available, get the first available transcript
                transcript = transcript_list.find_transcript(['en-US', 'en-GB'])
                
            transcript_data = transcript.fetch()
            
            # Combine text from transcript segments
            full_text = " ".join([segment['text'] for segment in transcript_data])
            
            return full_text, transcript_data
            
        except NoTranscriptFound:
            raise Exception("No transcript found for this video.")
        except TranscriptsDisabled:
            raise Exception("Transcripts are disabled for this video.")
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}") 