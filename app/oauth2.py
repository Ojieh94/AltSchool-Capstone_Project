from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError 
from . import database, schemas, models, config

# OAuth2PasswordBearer is a class that provides the mechanism to retrieve the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key and algorithm for encoding and decoding JWT tokens, retrieved from configuration
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict) -> str:
    """
    Create a new JWT access token with an expiration time.
    
    Args:
        data (dict): The data to include in the token payload.
    
    Returns:
        str: The encoded JWT token as a string.
    """
    encoded_data = data.copy()  # Create a copy of the input data
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set expiration time
    encoded_data.update({"exp": expiry_time})  # Add expiration time to the payload

    # Encode the data into a JWT token using the secret key and specified algorithm
    jwt_access_token = jwt.encode(encoded_data, SECRET_KEY, ALGORITHM)
    return jwt_access_token

def verify_access_token(token: str, credentials_exception):
    """
    Verify a JWT token and return the token data if valid.
    
    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.
    
    Returns:
        schemas.TokenData: The token data extracted from the token.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # Extract user ID from the token payload
        if not id:
            raise credentials_exception  # Raise exception if user ID is not found
        token_data = schemas.TokenData(id=str(id))  # Create TokenData object with the user ID

    except JWTError:
        # Raise credentials exception if JWTError occurs
        raise credentials_exception
    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database.get_db)):
    """
    Get the current user based on the provided JWT token.
    
    Args:
        token (str): The JWT token provided in the request.
        db (Session): The SQLAlchemy database session dependency.
    
    Returns:
        models.User: The user object corresponding to the token ID.
    
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    # Define the exception to be raised for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    # Verify the token and extract token data
    token = verify_access_token(token, credentials_exception)
    # Query the database to find the user by ID from the token data
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
