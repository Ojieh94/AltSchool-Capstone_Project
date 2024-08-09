from fastapi import status
from .. import schemas 

def test_create_user(client):
    """
    Test the creation of a new user.
    
    Args:
        client: A test client instance to make requests to the FastAPI application.
    """
    # Define the user data to be sent in the POST request
    user_data = {
        "email": "jengreat94@gmail.com",
        "password": "514500"
    }
    # Send a POST request to the /users endpoint with the user data
    response = client.post("/users", json=user_data)

    # Parse the JSON response into a UserResponseModel object
    new_user = schemas.UserResponseModel(**response.json())

    # Check if the email of the created user matches the expected email
    assert new_user.email == "jengreat94@gmail.com" 
    assert response.status_code == status.HTTP_201_CREATED

def test_get_user(client, test_user):
    """
    Test retrieving an existing user by ID.
    
    Args:
        client: A test client instance to make requests to the FastAPI application.
        test_user: A fixture that provides a test user with a known ID.
    """
    # Send a GET request to retrieve the user by ID
    response = client.get(f"/users/{test_user['id']}") 
    new_user = schemas.UserResponseModel(**response.json())    
    assert response.status_code == status.HTTP_200_OK
    assert new_user.email == "jengreat94@gmail.com"

def test_user_not_found(client):
    """
    Test retrieving a user that does not exist.
    
    Args:
        client: A test client instance to make requests to the FastAPI application.
    """
    # Send a GET request for a user with an ID that does not exist
    response = client.get("/users/2")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND