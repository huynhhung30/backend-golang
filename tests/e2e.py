import requests
import json
import pytest

# Define the base URL
BASE_URL = "http://localhost:8001/api/v1"

API_KEY = "cJGZ8L1sDcPezjOy1zacPJZxzZxrPObm2Ggs1U0V+fE=INSECURE"  # Replace with your actual API key
headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

# Register a new user and log in to get a JWT token
def get_jwt_token():
    # User registration (assuming it doesn't need authentication)
    register_url = f"{BASE_URL}/register"
    register_data = json.dumps({"username": "user1", "password": "securepassword"})
    register_response = requests.post(register_url, headers=headers, data=register_data)
    
    assert register_response.status_code in [200, 201], f"User registration failed: {register_response.status_code}"
    
    # User login
    login_url = f"{BASE_URL}/login"
    login_data = json.dumps({"username": "user1", "password": "securepassword"})
    login_response = requests.post(login_url, headers=headers, data=login_data)
    
    assert login_response.status_code == 200, f"User login failed: {login_response.status_code}"
    
    # Extracting JWT token from login response
    jwt_token = login_response.json().get('token')  
    assert jwt_token is not None, "JWT token not found in login response"
    
    return jwt_token

# Create a new book
def create_book(jwt_token):
    url = f"{BASE_URL}/books"
    auth_headers = {**headers, "Authorization": f"Bearer {jwt_token}"}
    data = json.dumps({"author": "Jane Doe", "title": "New Book Title"})
    response = requests.post(url, headers=auth_headers, data=data)
    
    assert response.status_code == 201, f"Failed to create book: {response.status_code}"
    return response.json()

# Get all books
def get_books(jwt_token):
    url = f"{BASE_URL}/books"
    auth_headers = {**headers, "Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=auth_headers)
    
    assert response.status_code == 200, f"Failed to get books: {response.status_code}"
    return response.json()

# Get a specific book by ID
def get_book(book_id, jwt_token):
    url = f"{BASE_URL}/books/{book_id}"
    auth_headers = {**headers, "Authorization": f"Bearer {jwt_token}"}
    response = requests.get(url, headers=auth_headers)
    
    assert response.status_code == 200, f"Failed to get book: {response.status_code}"
    return response.json()

# Update a book
def update_book(book_id, jwt_token):
    url = f"{BASE_URL}/books/{book_id}"
    auth_headers = {**headers, "Authorization": f"Bearer {jwt_token}"}
    data = json.dumps({"author": "John Smith", "title": "Updated Book Title"})
    response = requests.put(url, headers=auth_headers, data=data)
    
    assert response.status_code == 200, f"Failed to update book: {response.status_code}"
    return response.json()

# Delete a book
def delete_book(book_id, jwt_token):
    url = f"{BASE_URL}/books/{book_id}"
    auth_headers = {**headers, "Authorization": f"Bearer {jwt_token}"}
    response = requests.delete(url, headers=auth_headers)
    
    assert response.status_code == 204, f"Failed to delete book: {response.status_code}"

# Tests using pytest
@pytest.fixture(scope="module")
def jwt_token():
    return get_jwt_token()

def test_create_book(jwt_token):
    book = create_book(jwt_token)
    assert book['data']['author'] == "Jane Doe"
    assert book['data']['title'] == "New Book Title"
    return book

def test_get_books(jwt_token):
    books = get_books(jwt_token)
    assert isinstance(books, dict), "Books response is not a dictionary"
    assert 'data' in books, "Books data not found in response"

def test_get_book(jwt_token):
    book = create_book(jwt_token)
    book_id = book['data']['id']
    fetched_book = get_book(book_id, jwt_token)
    assert fetched_book['data']['id'] == book_id, "Fetched book ID does not match created book ID"

def test_update_book(jwt_token):
    book = create_book(jwt_token)
    book_id = book['data']['id']
    updated_book = update_book(book_id, jwt_token)
    assert updated_book['data']['author'] == "John Smith", "Book author not updated"
    assert updated_book['data']['title'] == "Updated Book Title", "Book title not updated"

def test_delete_book(jwt_token):
    book = create_book(jwt_token)
    book_id = book['data']['id']
    delete_book(book_id, jwt_token)
    with pytest.raises(AssertionError):
        get_book(book_id, jwt_token)  # This should raise an error since the book is deleted
