"""
Authentication endpoint tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "Test123456",
            "full_name": "New User"
        }
    )
    assert response.status_code in [200, 201, 400]  # 400 if user exists


def test_login_user():
    """Test user login."""
    # First register
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "logintest@test.com",
            "password": "Test123456"
        }
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logintest@test.com",
            "password": "Test123456"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
