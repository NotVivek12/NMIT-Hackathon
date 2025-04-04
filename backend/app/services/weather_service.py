import os
import httpx
from typing import Dict, Any, Tuple
from opencage.geocoder import OpenCageGeocode

class WeatherService:
    def __init__(self):
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
        
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
            results = self.geocoder.geocode(location)
            
            if not results or len(results) == 0:
                raise Exception(f"Could not geocode location: {location}")
                
            top_result = results[0]
            coords = {
                "lat": top_result["geometry"]["lat"],
                "lng": top_result["geometry"]["lng"]
            }
            
            # Get formatted location name
            formatted_location = top_result.get("formatted", location)
            
            return coords, formatted_location
            
        except Exception as e:
            raise Exception(f"Geocoding error: {str(e)}")
    
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
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                
                if response.status_code != 200:
                    raise Exception(f"Weather API error: {response.text}")
                    
                data = response.json()
                
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
            raise Exception(f"Weather retrieval error: {str(e)}") 