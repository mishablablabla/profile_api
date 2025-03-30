import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
import logging
import json

load_dotenv()

client = TestClient(app)

test_mode = os.getenv("TEST_MODE")
if test_mode == "true":
    print("TEST_MODE is enabled, running tests...")

@pytest.fixture(scope="module")
def profile_data():
    return {
        "user_id": str(uuid4()), # Изменено на строку
        "email": "testuser@example.com",
        "nick": "testuser",
        "education": "Bachelor",
        "city": "New York",
    }

def test_get_profiles():
    response = client.get("/profiles")
    if response.status_code == 404:
        assert response.json() == {"error": "Profiles not found"}
    else:
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_get_profile(profile_data):
    response = client.post("/profiles", json=profile_data)
    assert response.status_code == 200
    profile = response.json()
    response = client.get(f"/profiles/{profile['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == profile["id"]

def test_create_profile(profile_data):
    response = client.post("/profiles", json=profile_data)
    assert response.status_code == 200
    created_profile = response.json()
    
    logging.info(f"Profile created: {created_profile}")
    
    assert created_profile["email"] == profile_data["email"]
    assert created_profile["nick"] == profile_data["nick"]
    assert created_profile["education"] == profile_data["education"]
    assert created_profile["city"] == profile_data["city"]

def test_update_profile(profile_data):
    response = client.post("/profiles", json=profile_data)
    assert response.status_code == 200
    profile = response.json()
    updated_data = {
        "user_id": profile_data["user_id"], 
        "email": "updateduser@example.com",
        "nick": "updateduser",
        "education": "Master",
        "city": "Los Angeles",
    }
    response = client.put(f"/profiles/{profile['id']}", json=updated_data)
    assert response.status_code == 200
    updated_profile = response.json()
    assert updated_profile["email"] == updated_data["email"]
    assert updated_profile["nick"] == updated_data["nick"]
    assert updated_profile["education"] == updated_data["education"]
    assert updated_profile["city"] == updated_data["city"]

def test_delete_profile(profile_data):
    response = client.post("/profiles", json=profile_data)
    assert response.status_code == 200
    profile = response.json()
    response = client.delete(f"/profiles/{profile['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "Profile deleted successfully"}
    response = client.get(f"/profiles/{profile['id']}")
    assert response.status_code == 404

def test_get_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert "application_version" in response.json()
    assert "test_mode" in response.json()