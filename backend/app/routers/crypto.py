from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import CryptoRequest, CryptoResponse, CryptoData, ErrorResponse
from app.services.crypto_service import CryptoService

router = APIRouter()

async def get_crypto_service():
    """Dependency for getting the Cryptocurrency service."""
    return CryptoService()

@router.post(
    "/price", 
    response_model=CryptoResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_crypto_price(
    request: CryptoRequest,
    crypto_service: CryptoService = Depends(get_crypto_service)
):
    """
    Get current price and data for a cryptocurrency.
    
    - **symbol**: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
    
    Returns current price, market cap, and other data for the cryptocurrency.
    """
    try:
        # Validate input
        if not request.symbol or len(request.symbol) < 1:
            raise ValueError("Cryptocurrency symbol is required")
            
        # Get cryptocurrency data
        crypto_data, crypto_name = await crypto_service.get_crypto_price(request.symbol)
        
        # Return the crypto data
        return CryptoResponse(
            crypto=CryptoData(**crypto_data),
            symbol=request.symbol.upper(),
            name=crypto_name
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