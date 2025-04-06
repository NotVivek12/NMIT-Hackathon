import os
import httpx
from typing import Dict, Any, Tuple
from opencage.geocoder import OpenCageGeocode
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
        
        # Log API key status for debugging (don't log actual keys)
        logger.info(f"Weather API key configured: {bool(self.weather_api_key)}")
        logger.info(f"Geocoder API key configured: {bool(self.geocoder.key)}")
        
    async def geocode_location(self, location: str) -> Tuple[Dict[str, float], str]:
        """
        Geocode a location string to get coordinates.
        
        Args:
            location: Location string (e.g., "Tokyo, Japan")
            
        Returns:
            Tuple of (coordinates dict with lat/lng, formatted location name)
            
        Raises:
            Exception: If geocoding fails
        """
        try:
            logger.info(f"Geocoding location: {location}")
            results = self.geocoder.geocode(location)
            
            if not results or len(results) == 0:
                logger.error(f"No geocoding results found for: {location}")
                raise Exception(f"Could not geocode location: {location}")
                
            top_result = results[0]
            coords = {
                "lat": top_result["geometry"]["lat"],
                "lng": top_result["geometry"]["lng"]
            }
            
            # Get formatted location name
            formatted_location = top_result.get("formatted", location)
            logger.info(f"Successfully geocoded {location} to {coords} ({formatted_location})")
            
            return coords, formatted_location
            
        except Exception as e:
            error_msg = f"Geocoding error: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            raise Exception(error_msg)
    
    async def get_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get current weather for coordinates.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Weather data dictionary
            
        Raises:
            Exception: If weather retrieval fails
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={self.weather_api_key}&units=metric"
        
        try:
            logger.info(f"Fetching weather data for coordinates: {lat}, {lng}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                
                if response.status_code != 200:
                    error_msg = f"Weather API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
                data = response.json()
                logger.info(f"Successfully retrieved weather data for {lat}, {lng}")
                
                # Extract relevant weather information
                weather_data = {
                    "temperature": data["main"]["temp"],
                    "temperature_fahrenheit": (data["main"]["temp"] * 9/5) + 32,
                    "conditions": data["weather"][0]["main"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "location": data["name"]
                }
                
                return weather_data
                
        except Exception as e:
            error_msg = f"Weather retrieval error: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            raise Exception(error_msg) 