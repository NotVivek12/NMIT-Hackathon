from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import EVStationRequest, EVStationResponse, EVStation, ErrorResponse
from app.services.ev_service import EVStationService

router = APIRouter()

async def get_ev_service():
    """Dependency for getting the EV Station service."""
    return EVStationService()

@router.post(
    "/nearby", 
    response_model=EVStationResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def find_nearby_ev_stations(
    request: EVStationRequest,
    ev_service: EVStationService = Depends(get_ev_service)
):
    """
    Find nearby EV charging stations for a location.
    
    - **location**: The location to search around (e.g., 'Central Park, New York')
    - **radius**: Search radius in kilometers (default: 5)
    
    Returns a list of nearby EV charging stations and a map URL.
    """
    try:
        # Geocode the location
        coords, formatted_location = await ev_service.geocode_location(request.location)
        
        # Get nearby charging stations
        stations_data = await ev_service.get_charging_stations(
            coords["lat"], 
            coords["lng"], 
            request.radius
        )
        
        # Generate map URL
        map_url = ev_service.generate_map_url(
            coords["lat"], 
            coords["lng"], 
            formatted_location
        )
        
        # Create station objects
        stations = [EVStation(**station) for station in stations_data]
        
        # Return the stations data
        return EVStationResponse(
            stations=stations,
            location=formatted_location,
            map_url=map_url
        )
        
    except Exception as e:
        # Handle errors
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 