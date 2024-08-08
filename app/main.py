# Import necessary modules and classes from FastAPI and other components
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ratings, user, auth, movie, comment
from . import models
from .database import engine 

# Create an instance of the FastAPI class
app = FastAPI()

# Define CORS (Cross-Origin Resource Sharing) settings
origins = ["*"]  # Allow requests from any origin

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify the allowed origins (here, all origins are allowed)
    allow_credentials=True,  # Allow credentials to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Create all tables in the database based on the models defined
models.Base.metadata.create_all(bind=engine)

# Include routers for different parts of the application
app.include_router(user.router)  # User-related endpoints
app.include_router(auth.router)  # Authentication-related endpoints
app.include_router(movie.router)  # Movie-related endpoints
app.include_router(ratings.router)  # Ratings-related endpoints
app.include_router(comment.router)  # Comment-related endpoints
