from passlib.context import CryptContext

# Create a CryptContext object for password hashing
# Using bcrypt as the hashing scheme and setting 'auto' for deprecated schemes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    Hash a plain password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)  # Hash the password and return the hashed value

def verify_hashed_password(plain_password: str, hashed_password: str):
    """
    Verify if a plain password matches a hashed password.
    
    Args:
        plain_password (str): The plain text password to check.
        hashed_password (str): The hashed password to compare against.
    
    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)  # Check if the plain password matches the hashed password
