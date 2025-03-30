from unittest import mock
import uuid
import pytest
from src.models.profile import Profile, ProfileService
import logging

@pytest.fixture
def mock_profile_service():
    return mock.create_autospec(ProfileService)

def test_get_profiles(mock_profile_service):
    mock_profile_service.get_profiles.return_value = [
        Profile(id=uuid.uuid4(), user_id=uuid.uuid4(), email="john@example.com", nick="john", education="Bachelor", city="New York")
    ]
    profiles = mock_profile_service.get_profiles()
    assert len(profiles) == 1
    assert profiles[0].email == "john@example.com"

def test_create_profile(mock_profile_service):
    profile_data = {
        "user_id": uuid.uuid4(),
        "email": "jane@example.com",
        "nick": "jane",
        "education": "Master",
        "city": "Los Angeles",
    }
    mock_profile_service.create_profile.return_value = Profile(
        id=uuid.uuid4(), **profile_data
    )
    
    logging.info(f"Creating profile with data: {profile_data}")
    
    created_profile = mock_profile_service.create_profile(Profile(**profile_data))
    assert created_profile.email == "jane@example.com"
    assert created_profile.nick == "jane"
    assert created_profile.education == "Master"
    assert created_profile.city == "Los Angeles"

def test_get_profile(mock_profile_service):
    profile_id = uuid.uuid4()
    mock_profile_service.get_profile.return_value = Profile(
        id=profile_id, user_id=uuid.uuid4(), email="test@example.com", nick="test", education="PhD", city="Chicago"
    )
    profile = mock_profile_service.get_profile(profile_id)
    assert profile.id == profile_id

def test_update_profile(mock_profile_service):
    profile_id = uuid.uuid4()
    updated_data = {
        "user_id": uuid.uuid4(),
        "email": "updated@example.com",
        "nick": "updated",
        "education": "Associate",
        "city": "Houston",
    }
    mock_profile_service.update_profile.return_value = Profile(
        id=profile_id, **updated_data
    )
    updated_profile = mock_profile_service.update_profile(profile_id, Profile(**updated_data))
    assert updated_profile.email == "updated@example.com"
    assert updated_profile.city == "Houston"

def test_delete_profile(mock_profile_service):
    profile_id = uuid.uuid4()
    mock_profile_service.delete_profile.return_value = True
    result = mock_profile_service.delete_profile(profile_id)
    assert result is True