from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import YouTubeRequest, YouTubeResponse, ErrorResponse
from app.services.youtube_service import YouTubeService
from app.services.gemini_service import GeminiService

router = APIRouter()

async def get_youtube_service():
    """Dependency for getting the YouTube service."""
    return YouTubeService()

async def get_gemini_service():
    """Dependency for getting the Gemini service."""
    return GeminiService()

@router.post(
    "/summarize", 
    response_model=YouTubeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def summarize_youtube_video(
    request: YouTubeRequest,
    youtube_service: YouTubeService = Depends(get_youtube_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    """
    Summarize a YouTube video by its URL.
    
    - **url**: The URL of the YouTube video to summarize
    
    Returns a summary of the video content.
    """
    try:
        # Extract video ID from URL
        video_id = await youtube_service.extract_video_id(str(request.url))
        
        # Get video title
        title = await youtube_service.get_video_title(video_id)
        
        # Get transcript
        transcript, _ = await youtube_service.get_transcript(video_id)
        
        # Summarize the transcript
        summary_points = await gemini_service.summarize_text(transcript)
        
        # Return the summarized data
        return YouTubeResponse(
            summary=summary_points,
            title=title,
            url=request.url
        )
        
    except ValueError as e:
        # Invalid URL or video ID
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        # Other errors
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 