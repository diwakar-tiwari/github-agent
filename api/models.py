from pydantic import BaseModel
from typing import Optional

class AnalysisRequest(BaseModel):
    repo_url: str
    user_id: str

class AnalysisResponse(BaseModel):
    task_id: str
    status: str
    message: str
    check_status_url: str

class StatusResponse(BaseModel):
    task_id: str
    status: str  # "processing", "completed", "failed"
    progress: Optional[str] = None
    pdf_url: Optional[str] = None
    error: Optional[str] = None
    processing_time: Optional[str] = None
