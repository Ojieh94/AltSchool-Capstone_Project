from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Base model for user data used in requests and responses
class UserBase(BaseModel):
    email: EmailStr  

    class Config:
        from_attributes = True  # Allows using attributes directly from SQLAlchemy models

# Model for representing a user in responses with additional fields
class UserResponseModel(BaseModel):
    id: int  
    email: EmailStr  
    created_at: datetime  

    class Config:
        from_attributes = True

# Model for creating a new user, including password
class UserCreate(UserBase):
    password: str 

    class Config:
        from_attributes = True

# Base model for movie data used in requests
class MovieBase(BaseModel):
    title: str 
    genre: str 
    director: str  

# Model for representing a movie in responses with additional fields
class MovieResponseModel(BaseModel):
    id: int  
    title: str  
    genre: str  
    director: str  
    created_at: datetime  
    user_id: int  
    user: UserResponseModel  

    class Config:
        from_attributes = True

# Model for creating a new movie
class MovieCreate(MovieBase):
    pass  # Inherits all fields from MovieBase, no additional fields

# Model for updating movie information
class MovieUpdate(MovieBase):
    pass  # Inherits all fields from MovieBase, no additional fields

# Base model for rating data used in requests
class RatingBase(BaseModel):
    movie_id: int  
    rating: int  

# Model for representing a rating in responses with additional fields
class RatingResponseModel(BaseModel):
    id: int  
    rating: float  
    movie_id: int  
    movie: MovieResponseModel  
    user_id: int 

    class Config:
        from_attributes = True

# Model for creating a new rating
class RatingCreate(RatingBase):
    pass  # Inherits all fields from RatingBase, no additional fields

# Model for holding token data, typically used after authentication
class TokenData(BaseModel):
    id: Optional[str] = None  

# Model for representing an authentication token
class Token(BaseModel):
    access_token: str  
    token_type: str  

# Base model for comment data used in requests
class CommentBase(BaseModel):
    movie_id: int  
    content: str 

# Model for representing a comment in responses with additional fields
class CommentResponseModel(BaseModel):
    id: int  
    content: str  
    user_id: int  
    movie_id: int 
    movie: MovieResponseModel  # Movie being commented on, represented as a MovieResponseModel
    created_at: datetime  # Timestamp for when the comment was created

    class Config:
        from_attributes = True

# Model for creating a new comment
class CommentCreate(CommentBase):
    pass  # Inherits all fields from CommentBase, no additional fields

# Model for representing a rating without any additional details
class Rating(BaseModel):
    id: int  
    rating: float 
    user_id: int 

    class Config:
        from_attributes = True

# Model for representing a movie with its associated ratings
class MovieRatingResponseModel(BaseModel):
    id: int  
    title: str  
    genre: str  
    director: str  
    user_id: int  
    ratings: List[Rating]  

    class Config:
        from_attributes = True

# Model for representing a comment without any additional details
class Comment(BaseModel):
    id: int  
    content: str  
    user_id: int  

    class Config:
        from_attributes = True

# Model for representing a movie with its associated comments
class MovieCommentResponseModel(BaseModel):
    id: int  
    title: str  
    genre: str  
    director: str  
    user_id: int  
    comments: List[Comment] 

    class Config:
        from_attributes = True

# Model for creating a reply to a comment
class ReplyCreate(BaseModel):
    comment_id: int  
    content: str  
