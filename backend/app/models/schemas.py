from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import List, Optional, Dict, Any, Union

class YouTubeRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL of the YouTube video to summarize")

class YouTubeResponse(BaseModel):
    summary: List[str] = Field(..., description="List of summary points about the video")
    title: str = Field(..., description="Title of the video")
    url: HttpUrl = Field(..., description="URL of the video that was summarized")

class WeatherRequest(BaseModel):
    location: str = Field(..., description="Location to get weather for (e.g., 'Tokyo, Japan')")

class WeatherData(BaseModel):
    temperature: float = Field(..., description="Current temperature in Celsius")
    temperature_fahrenheit: float = Field(..., description="Current temperature in Fahrenheit")
    conditions: str = Field(..., description="Current weather conditions (e.g., 'Partly Cloudy')")
    humidity: int = Field(..., description="Current humidity percentage")
    wind_speed: float = Field(..., description="Current wind speed in km/h")
    location: str = Field(..., description="Location the weather is for")

class WeatherResponse(BaseModel):
    weather: WeatherData
    location_coords: Dict[str, float] = Field(..., description="Latitude and longitude of the location")

class EVStationRequest(BaseModel):
    location: str = Field(..., description="Location to search for EV charging stations (e.g., 'Central Park, New York')")
    radius: Optional[int] = Field(5, description="Search radius in kilometers")

class EVStation(BaseModel):
    id: str
    name: str = Field(..., description="Name of the charging station")
    address: str = Field(..., description="Address of the charging station")
    latitude: float
    longitude: float
    available: int = Field(..., description="Number of available charging points")
    total: int = Field(..., description="Total number of charging points")

class EVStationResponse(BaseModel):
    location: str = Field(..., description="Location searched")
    stations: List[EVStation] = Field(..., description="List of EV charging stations")
    map_url: str = Field(..., description="URL to view stations on a map")

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")

class ImageGenerationResponse(BaseModel):
    image_url: str = Field(..., description="URL of the generated image")
    prompt: str = Field(..., description="Original prompt used to generate the image")

class CryptoRequest(BaseModel):
    symbol: str = Field(..., description="Cryptocurrency symbol (e.g., 'BTC', 'ETH')")

class CryptoData(BaseModel):
    price: float = Field(..., description="Current price in USD")
    change_24h: float = Field(..., description="24-hour price change percentage")
    market_cap: float = Field(..., description="Market capitalization in USD")
    volume_24h: float = Field(..., description="24-hour trading volume in USD")

class CryptoResponse(BaseModel):
    crypto: CryptoData
    symbol: str = Field(..., description="Cryptocurrency symbol")
    name: str = Field(..., description="Cryptocurrency name")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    success: bool = True

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str 