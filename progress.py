
from fastapi import APIRouter
from fastapi import HTTPException, status
from pydantic import BaseModel
import databutton as db
import traceback

# Router for endpoints
router = APIRouter()

class UserProgress(BaseModel):
    user_id: str
    level: int
    score: int
    completed_tasks: list[str]

class ProgressResponse(BaseModel):
    success: bool
    message: str
    data: UserProgress | None = None

@router.post("/save-progress")
def save_progress(progress: UserProgress) -> ProgressResponse:
    try:
        db.storage.json.put(f"user_progress_{progress.user_id}", progress.dict())
        return ProgressResponse(
            success=True,
            message="Progress saved successfully",
            data=progress
        )
    except Exception as e:
        print(f"Error saving progress: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save progress")

@router.get("/get-progress/{user_id}")
def get_progress(user_id: str) -> ProgressResponse:
    print(f"Attempting to retrieve progress for user_id: {user_id}")
    try:
        progress_key = f"user_progress_{user_id}"
        print(f"Fetching data with key: {progress_key}")
        progress_data = db.storage.json.get(progress_key)
        print(f"Retrieved progress data: {progress_data}")
        
        if progress_data:
            print("Progress data found, creating UserProgress object")
            user_progress = UserProgress(**progress_data)
        else:
            print("No progress data found, creating default UserProgress")
            # Return default progress for new users
            user_progress = UserProgress(user_id=user_id, level=1, score=0, completed_tasks=[])
        
        print(f"Returning progress for user {user_id}: {user_progress}")
        return ProgressResponse(
            success=True,
            message="Progress retrieved successfully",
            data=user_progress
        )
    except ValueError as ve:
        print(f"Validation error for user {user_id}: {str(ve)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid progress data format")
    except Exception as e:
        print(f"Unexpected error retrieving progress for user {user_id}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve progress")
