from sqlalchemy import Column, Integer, String, FLOAT, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from .database import Base

# Define the User model
class User(Base):
    __tablename__ = "users"  # Table name in the database
    id = Column(Integer, primary_key=True, nullable=False)  # Primary key for the User table
    email = Column(String, nullable=False, unique=True)  # User email, must be unique
    password = Column(String, nullable=False)  # User password
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Timestamp for when the user was created

# Define the Movie model
class Movie(Base):
    __tablename__ = "movies"  # Table name in the database
    id = Column(Integer, primary_key=True, nullable=False)  # Primary key for the Movie table
    title = Column(String, nullable=False)  # Title of the movie
    genre = Column(String, nullable=False)  # Genre of the movie
    director = Column(String, nullable=False)  # Director of the movie
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Timestamp for when the movie was created
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the User who added the movie
    user = relationship("User")  # Relationship to the User model
    ratings = relationship("Rating", back_populates="movie")  # Relationship to the Rating model
    comments = relationship("Comment", back_populates="movie")  # Relationship to the Comment model

# Define the Rating model
class Rating(Base):
    __tablename__ = "ratings"  # Table name in the database
    id = Column(Integer, primary_key=True, nullable=False)  # Primary key for the Rating table
    rating = Column(FLOAT, nullable=False)  # Rating value
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Timestamp for when the rating was created
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the Movie being rated
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the User who made the rating
    movie = relationship("Movie", back_populates="ratings")  # Relationship to the Movie model
    user = relationship("User")  # Relationship to the User model

# Define the Comment model
class Comment(Base):
    __tablename__ = "comments"  # Table name in the database
    id = Column(Integer, primary_key=True, nullable=False)  # Primary key for the Comment table
    content = Column(String, nullable=False)  # Content of the comment
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Timestamp for when the comment was created
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the User who made the comment
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the Movie being commented on
    movie = relationship("Movie", back_populates="comments")  # Relationship to the Movie model
    user = relationship("User")  # Relationship to the User model

# Define the Reply model
class Reply(Base):
    __tablename__ = "replies"  # Table name in the database
    id = Column(Integer, primary_key=True, nullable=False)  # Primary key for the Reply table
    reply = Column(String, nullable=False)  # Content of the reply
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Timestamp for when the reply was created
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the Comment being replied to
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Foreign key linking to the User who made the reply
    user = relationship("User")  # Relationship to the User model
    comment = relationship("Comment")  # Relationship to the Comment model
