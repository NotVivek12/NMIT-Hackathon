from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import WeatherRequest, WeatherResponse, WeatherData, ErrorResponse
from app.services.weather_service import WeatherService
import logging
import traceback

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_weather_service():
    """Dependency for getting the Weather service."""
    return WeatherService()

@router.post(
    "/current", 
    response_model=WeatherResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_current_weather(
    request: WeatherRequest,
    weather_service: WeatherService = Depends(get_weather_service)
):
    """
    Get current weather for a location.
    
    - **location**: The location to get weather for (e.g., 'Tokyo, Japan')
    
    Returns current weather data and location coordinates.
    """
    try:
        # Geocode the location
        logger.info(f"Processing weather request for location: {request.location}")
        coords, formatted_location = await weather_service.geocode_location(request.location)
        
        # Get weather data
        logger.info(f"Geocoded to coordinates: {coords}")
        weather_data = await weather_service.get_weather(coords["lat"], coords["lng"])
        
        # Update location from formatted geocoded result
        weather_data["location"] = formatted_location
        
        # Return the weather data
        return WeatherResponse(
            weather=WeatherData(**weather_data),
            location_coords=coords
        )
        
    except Exception as e:
        # Enhanced error logging
        error_detail = f"Error processing weather request: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_detail)
        
        # Handle errors with more details
        raise HTTPException(
            status_code=500,
            detail=error_detail
        ) 