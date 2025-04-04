import os
import httpx
import urllib.parse
from typing import Dict, Any, List, Tuple
from opencage.geocoder import OpenCageGeocode

class EVStationService:
    def __init__(self):
        self.geocoder = OpenCageGeocode(os.getenv("OPENCAGE_API_KEY"))
        # Note: Open Charge Map API key would normally go here,
        # but their API supports anonymous access
        
    async def geocode_location(self, location: str) -> Tuple[Dict[str, float], str]:
        """
        Geocode a location string to get coordinates.
        
        Args:
            location: Location string (e.g., "Central Park, New York")
            
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
    
    async def get_charging_stations(self, lat: float, lng: float, radius: int = 5) -> List[Dict[str, Any]]:
        """
        Find EV charging stations near the specified coordinates.
        
        Args:
            lat: Latitude
            lng: Longitude
            radius: Search radius in kilometers
            
        Returns:
            List of charging station dictionaries
            
        Raises:
            Exception: If station retrieval fails
        """
        # Open Charge Map API endpoint
        url = "https://api.openchargemap.io/v3/poi"
        
        params = {
            "latitude": lat,
            "longitude": lng,
            "distance": radius,
            "distanceunit": "km",
            "maxresults": 10,
            "compact": True,
            "verbose": False,
            "output": "json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                
                if response.status_code != 200:
                    raise Exception(f"Open Charge Map API error: {response.text}")
                    
                stations_data = response.json()
                
                # Process and format the stations data
                stations = []
                for station in stations_data:
                    # Extract connector types
                    connector_types = []
                    if "Connections" in station:
                        for connection in station["Connections"]:
                            if "ConnectionType" in connection and "Title" in connection["ConnectionType"]:
                                connector_types.append(connection["ConnectionType"]["Title"])
                    
                    # Extract address
                    address = ""
                    if "AddressInfo" in station:
                        address_parts = []
                        if "AddressLine1" in station["AddressInfo"] and station["AddressInfo"]["AddressLine1"]:
                            address_parts.append(station["AddressInfo"]["AddressLine1"])
                        if "Town" in station["AddressInfo"] and station["AddressInfo"]["Town"]:
                            address_parts.append(station["AddressInfo"]["Town"])
                        if "StateOrProvince" in station["AddressInfo"] and station["AddressInfo"]["StateOrProvince"]:
                            address_parts.append(station["AddressInfo"]["StateOrProvince"])
                        address = ", ".join(address_parts)
                    
                    # Get station name
                    name = ""
                    if "AddressInfo" in station and "Title" in station["AddressInfo"]:
                        name = station["AddressInfo"]["Title"]
                    else:
                        name = f"Charging Station {station.get('ID', '')}"
                    
                    # Get number of charging points
                    total_points = 0
                    if "NumberOfPoints" in station and station["NumberOfPoints"]:
                        total_points = station["NumberOfPoints"]
                    else:
                        # Estimate from connections
                        total_points = len(station.get("Connections", []))
                    
                    # Simulate availability (in a real app, this would come from a real-time API)
                    # For demo purposes, we'll just set a random number of available points
                    import random
                    available_points = random.randint(0, total_points)
                    
                    stations.append({
                        "name": name,
                        "address": address,
                        "available": available_points,
                        "total": total_points,
                        "connector_types": list(set(connector_types))  # Remove duplicates
                    })
                
                return stations
                
        except Exception as e:
            raise Exception(f"EV station retrieval error: {str(e)}")
    
    def generate_map_url(self, lat: float, lng: float, location: str) -> str:
        """
        Generate a URL to view the location on a map.
        
        Args:
            lat: Latitude
            lng: Longitude
            location: Location name
            
        Returns:
            Map URL
        """
        encoded_location = urllib.parse.quote(location)
        return f"https://www.google.com/maps/search/ev+charging+stations/@{lat},{lng},14z/data=!3m1!4b1" 