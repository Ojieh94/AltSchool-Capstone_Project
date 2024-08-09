# Import necessary modules and classes from FastAPI and other components
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ratings, user, auth, movie, comment
from . import models
from .database import engine 

# Create an instance of the FastAPI class
app = FastAPI()

# Define CORS (Cross-Origin Resource Sharing) settings
origins = ["*"] 

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Create all tables in the database based on the models defined
models.Base.metadata.create_all(bind=engine)

# Include routers for different parts of the application
app.include_router(user.router) 
app.include_router(auth.router)  
app.include_router(movie.router)  
app.include_router(ratings.router)  
app.include_router(comment.router)  
