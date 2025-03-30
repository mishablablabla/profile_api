from functools import lru_cache
from typing import Annotated
import fastapi
from fastapi.params import Depends
from src.api import profiles
from src.middlewares import error_handler
from dotenv import load_dotenv
from src.models.profile import ProfileService, Profile
import os
import uvicorn
import json
import config
import logging
import pytest

load_dotenv()
test_mode = os.getenv("TEST_MODE")

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler("src/logs/app.log")  
    ]
)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)

file_handler = logging.FileHandler("src/logs/structured_log.json")
file_handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(file_handler)

@lru_cache
def get_settings():
    return config.Settings()

app = fastapi.FastAPI(
    title="Profiles API",
    description="API for profile management",
    version="1.0.0",
    contact={"email": "polina.dmytrenko@hotmail.com"},
    openapi_tags=[{"name": "profiles", "description": "Operations with profiles"}]
)

app.include_router(profiles.router)
error_handler.setup_exception_handlers(app)
app.add_middleware(error_handler.ErrorHandlerMiddleware)

@app.get("/info", tags=["info"], description="Get info about the app")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }

if test_mode == "true":
    print("Running tests...")
    pytest.main(["-q", "--tb=short", "--disable-warnings"])
    profile_service = ProfileService()

static_profiles = [
    {"user_id": "123e4567-e89b-12d3-a456-426614174001", "email": "testuser@example.com", "nick": "testuser", "education": "Bachelor", "city": "New York"},
    {"user_id": "223e4567-e89b-12d3-a456-426614174002", "email": "exampleuser@example.com", "nick": "exampleuser", "education": "Master", "city": "Los Angeles"}
]

for profile_data in static_profiles:
    profile = Profile(**profile_data)  
    profile_service.create_profile(profile)  
    logging.info(f"Profile added: {profile}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
