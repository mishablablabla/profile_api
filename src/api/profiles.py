from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
import logging
from src.models.profile import Profile, ProfileService, get_profile_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/profiles", response_model=List[Profile], tags=["profiles"], description="Get all profiles")
def get_profiles(service: ProfileService = Depends(get_profile_service)):
    profiles = service.get_profiles()
    if not profiles:
        logger.info("Fetching all profiles")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profiles not found"
        )
    logger.info(f"Fetched {len(profiles)} profiles")
    return profiles

@router.get("/profiles/{profile_id}", response_model=Profile, tags=["profiles"], description="Get profile by ID")
def get_profile(profile_id: UUID, service: ProfileService = Depends(get_profile_service)):
    logger.info(f"Fetching profile with ID: {profile_id}")
    profile = service.get_profile(profile_id)
    if not profile:
        logger.warning(f"Profile {profile_id} not found")
        raise HTTPException(status_code=404, detail="Profile not found")
    logger.info(f"Profile found: {profile}")
    return profile

@router.post("/profiles", response_model=Profile, tags=["profiles"], description="Create a new profile")
def create_profile(profile: Profile, service: ProfileService = Depends(get_profile_service)):
    logger.info(f"Creating profile: {profile}")
    try:
        created_profile = service.create_profile(profile)
        if not created_profile:
            logger.warning("Failed to create profile")
            raise HTTPException(status_code=400, detail="Failed to create profile")
        logger.info(f"Profile created successfully: {created_profile}")
        return created_profile
    except Exception as e:
        logger.error(f"Error while creating profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/profiles/{profile_id}", response_model=Profile, tags=["profiles"], description="Update profile's data")
def update_profile(profile_id: UUID, updated_profile: Profile, service: ProfileService = Depends(get_profile_service)):
    logger.info(f"Updating profile {profile_id} with data: {updated_profile}")
    existing_profile = service.get_profile(profile_id)
    if not existing_profile:
        logger.warning(f"Profile {profile_id} not found")
        raise HTTPException(status_code=404, detail="Profile not found")
    try:
        # Сохраняем id из URL, перезаписывая его в обновлённом профиле
        updated_profile_with_id = updated_profile.copy(update={"id": profile_id})
        updated_profile_data = service.update_profile(profile_id, updated_profile_with_id)
        logger.info(f"Profile {profile_id} updated successfully")
        return updated_profile_data
    except Exception as e:
        logger.error(f"Error while updating profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/profiles/{profile_id}", tags=["profiles"], description="Delete profile by ID")
def delete_profile(profile_id: UUID, service: ProfileService = Depends(get_profile_service)):
    logger.info(f"Deleting profile with ID: {profile_id}")
    existing_profile = service.get_profile(profile_id)
    if not existing_profile:
        logger.warning(f"Profile {profile_id} not found")
        raise HTTPException(status_code=404, detail="Profile not found")
    try:
        service.delete_profile(profile_id)
        logger.info(f"Profile {profile_id} deleted successfully")
        return {"message": "Profile deleted successfully"}
    except Exception as e:
        logger.error(f"Error while deleting profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
