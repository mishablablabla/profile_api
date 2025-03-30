from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from typing import List, Optional


class Profile(BaseModel):
    id: Optional[UUID] = Field(default=UUID("00000000-0000-0000-0000-000000000000"))
    user_id: UUID
    email: str
    nick: str
    education: str 
    city: str


class ProfileService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProfileService, cls).__new__(cls)
            cls._instance.profiles = [] 
        return cls._instance

    def create_profile(self, profile: Profile) -> Profile:
        if not profile.id or profile.id == UUID("00000000-0000-0000-0000-000000000000"):
            profile.id = uuid4()
        self.profiles.append(profile)
        return profile

    def get_profiles(self) -> List[Profile]:
        return self.profiles

    def get_profile(self, profile_id: UUID) -> Optional[Profile]:
        return next((profile for profile in self.profiles if profile.id == profile_id), None)

    def update_profile(self, profile_id: UUID, updated_profile: Profile) -> Optional[Profile]:
        for idx, profile in enumerate(self.profiles):
            if profile.id == profile_id:
                updated_profile.id = profile_id
                self.profiles[idx] = updated_profile
                return updated_profile
        return None

    def delete_profile(self, profile_id: UUID) -> bool:
        for idx, profile in enumerate(self.profiles):
            if profile.id == profile_id:
                del self.profiles[idx]
                return True
        return False

def get_profile_service() -> ProfileService:
    return ProfileService()
