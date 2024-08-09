import pytest
from fastapi import status

def test_rate_movie(authorized_client, test_movies):
    """
    Test rating a movie successfully.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_movies: Fixture providing test movies data.
    """
    # Define the rating data for the movie
    response = authorized_client.post("/ratings", json= {
        "movie_id": 1,  # Assume movie with ID 1 exists
        "rating": 3
    })
    # Verify that the response status code is 201 Created
    assert response.status_code == status.HTTP_201_CREATED

def test_rate_movie_not_found(authorized_client):
    """
    Test rating a movie that does not exist.
    
    Args:
        authorized_client: A test client instance with authorization.
    """
    rating_data = {
        "movie_id": 1444,  # Assume movie with ID 1444 does not exist
        "rating": 3
    }
    # Send a POST request with non-existent movie ID
    response = authorized_client.post("/ratings", json=rating_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND    
    assert response.json()['detail'] == f"Movie with id:{rating_data['movie_id']} not found"

def test_rate_movie_user_exists(authorized_client, test_ratings):
    """
    Test rating a movie when the user has already rated it.
    
    Args:
        authorized_client: A test client instance with authorization.
        test_ratings: Fixture providing test ratings data.
    """
    # Send a POST request to rate a movie that the user has already rated
    response = authorized_client.post("/ratings", json= {
        "movie_id": test_ratings[0].movie_id,
        "rating": test_ratings[0].rating
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST  
    assert response.json()['detail'] == "User has already rated this movie"

def test_get_ratings_for_movie(client, test_ratings):
    """
    Test retrieving ratings for a movie.
    
    Args:
        client: A test client instance without authorization.
        test_ratings: Fixture providing test ratings data.
    """
    response = client.get(f"/ratings/{test_ratings[0].movie_id}")
    assert response.status_code == status.HTTP_200_OK