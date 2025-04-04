from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ImageGenerationRequest, ImageGenerationResponse, ErrorResponse
from app.services.flux_service import FluxService

router = APIRouter()

async def get_image_service():
    """Dependency for getting the Image Generation service."""
    return FluxService()

@router.post(
    "/generate", 
    response_model=ImageGenerationResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def generate_image(
    request: ImageGenerationRequest,
    image_service: FluxService = Depends(get_image_service)
):
    """
    Generate an image based on a text prompt.
    
    - **prompt**: Text prompt describing the image to generate
    
    Returns the URL of the generated image.
    """
    try:
        # Validate input
        if not request.prompt or len(request.prompt) < 3:
            raise ValueError("Prompt must be at least 3 characters long")
            
        # Generate the image
        image_url = await image_service.generate_image(request.prompt)
        
        if not image_url:
            raise Exception("Failed to generate image")
            
        # Return the image URL
        return ImageGenerationResponse(
            image_url=image_url,
            prompt=request.prompt
        )
        
    except ValueError as e:
        # Invalid input
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