from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Retrieve the database URL from the configuration settings
DATABASE_URL = settings.sqlalchemy_database_url

# Create a new SQLAlchemy engine instance, connecting to the specified database URL
engine = create_engine(DATABASE_URL)

# Create a new sessionmaker instance bound to the engine
# SessionLocal is a factory for new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency function that provides a database session to FastAPI routes.
    
    Yields:
        Session: A SQLAlchemy Session object for database operations.
    
    Closes the session when done.
    """
    db = SessionLocal()  
    try:
        yield db  
    finally:
        db.close() 