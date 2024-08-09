import pytest
from fastapi import status
from .. import schemas

@pytest.mark.parametrize("title, genre, director", [
    ("The Punisher", "Action thriller", "Marvel Studios"),
    ("The Awakening", "Horror", "AJS Studios"),
    ("Twilight series", "Mystery", "Universal Studios")
])
def test_create_movie(authorized_client, test_user, title, genre, director):
    """
    Test the creation of a new movie with various parameters.
    """
    # Send a POST request to create a new movie
    response = authorized_client.post("/movies", json={
        "title": title,
        "genre": genre,
        "director": director
    })

    # Parse the response into a MovieResponseModel object
    new_movie = schemas.MovieResponseModel(**response.json())
    
    # Check that the response status code is 201 Created
    assert response.status_code == status.HTTP_201_CREATED  
    assert new_movie.genre == genre
    assert new_movie.director == director
    # Ensure the movie is associated with the correct user
    assert new_movie.user_id == test_user['id']

def test_unauthorized_user_create_movie(client):
    """
    Test that an unauthorized user cannot create a movie.
    
    Args:
        client: A test client instance without authorization.
    """
    # Send a POST request to create a movie without authorization
    response = client.post("/movies", json={
        "title": "The Punisher", 
        "genre": "Action thriller", 
        "director": "Marvel Studios"
    })
    
    # Check that the response status code is 401 Unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_all_movies(client, test_movies):
    """
    Test retrieving all movies.
    
    Args:
        client: A test client instance without authorization.
        test_movies: Fixture providing a list of test movies.
    """
    # Send a GET request to retrieve all movies
    response = client.get("/movies") 

    # Validate the response data
    def validate(movie):
        return schemas.MovieResponseModel(**movie)
    
    # Map response data to MovieResponseModel objects
    movies_map = map(validate, response.json())
    movies_list = list(movies_map)
    
    # Check that the number of movies returned matches the number of test movies
    assert len(response.json()) == len(test_movies) 
    assert response.status_code == status.HTTP_200_OK   
    assert movies_list[0].id == test_movies[0].id

def test_get_one_movie(client, test_movies):
    """
    Test retrieving a single movie by ID.
    
    Args:
        client: A test client instance without authorization.
        test_movies: Fixture providing a list of test movies.
    """
    # Send a GET request to retrieve a specific movie by ID
    response = client.get(f"/movies/{test_movies[0].id}")
    movie = schemas.MovieResponseModel(**response.json())
    
    assert response.status_code == status.HTTP_200_OK
    assert movie.title == test_movies[0].title

def test_get_one_movie_not_exist(client):
    """
    Test retrieving a movie that does not exist.
    
    Args:
        client: A test client instance without authorization.
    """
    id = 223
    # Send a GET request for a movie with a non-existent ID
    response = client.get(f"/movies/{id}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == f"Movie with id:{id} not found"

def test_unauthorized_user_delete_movie(client, test_movies):
    """
    Test that an unauthorized user cannot delete a movie.
    
    Args:
        client: A test client instance without authorization.
        test_movies: Fixture providing a list of test movies.
    """
    # Send a DELETE request to remove a movie without authorization
    response = client.delete(f"/movies/{test_movies[0].id}")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_movie(authorized_client, test_movies):
    """
    Test deleting a movie by an authorized user.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_movies: Fixture providing a list of test movies.
    """
    # Send a DELETE request to remove a movie
    response = authorized_client.delete(f"/movies/{test_movies[0].id}")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_movie_non_exist(authorized_client):
    """
    Test deleting a movie that does not exist.
    
    Args:
        authorized_client: A test client instance with authorization.
    """
    # Send a DELETE request for a movie with a non-existent ID
    response = authorized_client.delete(f"/movies/8000")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_other_user_movie(authorized_client, test_movies, test_user_two):
    """
    Test that an authorized user cannot delete a movie owned by another user.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_movies: Fixture providing a list of test movies.
        test_user_two: Fixture providing a second test user.
    """
    # Send a DELETE request to remove a movie owned by a different user
    response = authorized_client.delete(f"/movies/{test_movies[3].id}")
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_movie(authorized_client, test_movies):
    """
    Test updating a movie's details by an authorized user.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_movies: Fixture providing a list of test movies.
    """
    data = {
        "title": "Man of Steel",
        "genre": "Superhero",
        "director": "DC Comics" 
    }
    # Send a PUT request to update a movie's details
    response = authorized_client.put(f"/movies/{test_movies[0].id}", json=data)

    # Parse the response into a MovieResponseModel object
    updated_movie = schemas.MovieResponseModel(**response.json())
    
    assert response.status_code == status.HTTP_200_OK
    assert updated_movie.title == data['title']
    assert updated_movie.genre == data['genre']

def test_update_other_user_movie(authorized_client, test_movies, test_user_two):
    """
    Test that an authorized user cannot update a movie owned by another user.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_movies: Fixture providing a list of test movies.
        test_user_two: Fixture providing a second test user.
    """
    data = {
        "title": "Man of Steel",
        "genre": "Superhero",
        "director": "DC Comics" 
    }
    # Send a PUT request to update a movie owned by a different user
    response = authorized_client.put(f"/movies/{test_movies[3].id}", json=data)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_unauthorized_user_update_movie(client, test_movies):
    """
    Test that an unauthorized user cannot update a movie.
    
    Args:
        client: A test client instance without authorization.
        test_movies: Fixture providing a list of test movies.
    """
    # Send a PUT request to update a movie without authorization
    response = client.put(f"/movies/{test_movies[0].id}")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_movie_non_exist(authorized_client):
    """
    Test updating a movie that does not exist.
    
    Args:
        authorized_client: A test client instance with authorization.
    """
    # Send a PUT request for a movie with a non-existent ID
    response = authorized_client.put(f"/movies/8000")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
