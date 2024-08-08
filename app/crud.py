from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from . import database

class CRUDService:
    def __init__(self, db: Session = Depends(database.get_db)):
        """
        Initialize the CRUD service with a database session.
        
        Args:
            db (Session): The SQLAlchemy database session, provided by FastAPI dependency injection.
        """
        self.db = db

    def create(self, data_obj, model, current_user):
        """
        Create a new record in the database.
        
        Args:
            data_obj: Data object with values to be inserted into the database.
            model: SQLAlchemy model class representing the table.
            current_user: The currently authenticated user, used to set user_id in the record.
        
        Returns:
            model_obj: The created record object.
        """
        model_obj = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(model_obj)  # Add the record to the session
        self.db.commit()  # Commit the transaction
        self.db.refresh(model_obj)  # Refresh to get the updated record with any database defaults
        return model_obj

    def create_user(self, data_obj, model, hashed_password):
        """
        Create a new user record with hashed password.
        
        Args:
            data_obj: Data object with user details.
            model: SQLAlchemy model class representing the user table.
            hashed_password: The hashed password for the user.
        
        Returns:
            model_obj: The created user record object.
        """
        data_obj.password = hashed_password  # Set the hashed password
        model_obj = model(**data_obj.model_dump())
        self.db.add(model_obj)
        self.db.commit()
        self.db.refresh(model_obj)
        return model_obj

    def get_movie(self, model, limit, skip, search):
        """
        Retrieve a list of movies with optional search filter.
        
        Args:
            model: SQLAlchemy model class representing the movie table.
            limit: Number of records to retrieve.
            skip: Number of records to skip (for pagination).
            search: Search term to filter movies by genre.
        
        Returns:
            List: List of movie records matching the criteria.
        """
        movies = self.db.query(model).filter(model.genre.contains(search)).limit(limit).offset(skip).all()
        return movies

    def get(self, id, model):
        """
        Retrieve a single record by ID.
        
        Args:
            id: ID of the record to retrieve.
            model: SQLAlchemy model class representing the table.
        
        Returns:
            model_obj: The record object if found, otherwise None.
        """
        model_obj = self.db.query(model).filter(model.id == id).first()
        if not model_obj:
            return None
        return model_obj

    def get_query_by_id(self, id, model):
        """
        Retrieve a query object filtered by ID.
        
        Args:
            id: ID of the record to query.
            model: SQLAlchemy model class representing the table.
        
        Returns:
            query_result: Query object filtered by ID.
        """
        query_result = self.db.query(model).filter(model.id == id)
        return query_result

    def update(self, id, data_obj, model):
        """
        Update a record with new data.
        
        Args:
            id: ID of the record to update.
            data_obj: Data object with updated values.
            model: SQLAlchemy model class representing the table.
        """
        query = self.get_query_by_id(id, model)
        query.update(data_obj.model_dump(), synchronize_session=False)
        self.db.commit()

    def delete(self, id, model):
        """
        Delete a record by ID.
        
        Args:
            id: ID of the record to delete.
            model: SQLAlchemy model class representing the table.
        """
        query = self.get_query_by_id(id, model)
        query.delete(synchronize_session=False)
        self.db.commit()

    def get_user_by_email(self, email, model):
        """
        Retrieve a user record by email.
        
        Args:
            email: Email address to search for.
            model: SQLAlchemy model class representing the user table.
        
        Returns:
            user: The user record if found, otherwise None.
        """
        user = self.db.query(model).filter(model.email == email).first()
        if user:
            return user
        return None

    def get_ratings_for_movie(self, id, model):
        """
        Retrieve all ratings for a specific movie.
        
        Args:
            id: ID of the movie.
            model: SQLAlchemy model class representing the movie table.
        
        Returns:
            movie: The movie record with loaded ratings if found, otherwise None.
        """
        query = self.get_query_by_id(id, model)
        movie = query.options(joinedload(model.ratings)).first()
        if movie:
            return movie
        return None

    def get_existing_rating(self, data_obj, model, current_user):
        """
        Check if a user has already rated a specific movie.
        
        Args:
            data_obj: Data object containing the movie ID.
            model: SQLAlchemy model class representing the rating table.
            current_user: The currently authenticated user.
        
        Returns:
            existing_rating: The existing rating if found, otherwise None.
        """
        existing_rating = self.db.query(model).filter(
            model.movie_id == data_obj.movie_id,
            model.user_id == current_user.id
        ).first()
        if existing_rating:
            return existing_rating
        return None

    def rate_movie(self, data_obj, model, current_user):
        """
        Rate a movie.
        
        Args:
            data_obj: Data object containing the rating details.
            model: SQLAlchemy model class representing the rating table.
            current_user: The currently authenticated user.
        
        Returns:
            rating: The created rating record.
        """
        rating = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def comment_movie(self, data_obj, model, current_user):
        """
        Add a comment to a movie.
        
        Args:
            data_obj: Data object containing the comment details.
            model: SQLAlchemy model class representing the comment table.
            current_user: The currently authenticated user.
        
        Returns:
            comment: The created comment record.
        """
        comment = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments_for_movie(self, id, model):
        """
        Retrieve all comments for a specific movie.
        
        Args:
            id: ID of the movie.
            model: SQLAlchemy model class representing the movie table.
        
        Returns:
            movie: The movie record with loaded comments if found, otherwise None.
        """
        query = self.get_query_by_id(id, model)
        movie = query.options(joinedload(model.comments)).first()
        if movie:
            return movie
        return None

    def reply_comment(self, data_obj, model, current_user):
        """
        Add a reply to a comment.
        
        Args:
            data_obj: Data object containing the reply details.
            model: SQLAlchemy model class representing the reply table.
            current_user: The currently authenticated user.
        
        Returns:
            reply: The created reply record.
        """
        reply = model(user_id=current_user.id, **data_obj.model_dump())
        self.db.add(reply)
        self.db.commit()
        self.db.refresh(reply)
        return reply
