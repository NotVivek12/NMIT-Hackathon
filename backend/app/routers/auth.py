from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse, ErrorResponse
from app.services.auth_service import AuthService

router = APIRouter()

# Dependency for getting the auth service
async def get_auth_service():
    return AuthService()

# OAuth2 scheme for handling bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

@router.post(
    "/login", 
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse}}
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns an access token for authenticated requests.
    """
    user = auth_service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    token_data = {"sub": user["id"], "email": user["email"]}
    access_token = auth_service.create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)

@router.post(
    "/token",
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse}}
)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Get token using form-based authentication.
    This endpoint is used by the OAuth2 flow.
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    token_data = {"sub": user["id"], "email": user["email"]}
    access_token = auth_service.create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)

@router.post(
    "/register", 
    response_model=UserResponse,
    responses={400: {"model": ErrorResponse}}
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user.
    
    - **name**: User's name
    - **email**: User's email address
    - **password**: User's password
    
    Returns the newly created user.
    """
    # Check if user already exists
    existing_user = auth_service.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = auth_service.register_user(request.name, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )
    
    return UserResponse(**user)

# Dependency for getting the current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get the current user from the access token."""
    payload = auth_service.decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = payload.get("sub")
    if user_id not in auth_service.users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return auth_service.users[user_id] 