from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn
import os

# Use relative imports (remove sys.path stuff)
from .models import AnalysisRequest, AnalysisResponse
from .background import start_analysis, get_job_status, jobs

app = FastAPI(title = "Github Repo Analyzer", version = "1.0.0")

@app.get("/")
def root():
    return {"message":"Server is running..."}

@app.post("/analyze")
def analyze_repo(request: AnalysisRequest):
    repo_url = request.repo_url
    user_id = request.user_id

    try:
        task_id = start_analysis(repo_url, user_id)

        return AnalysisResponse(
            task_id=task_id,
            status= "processing",
            message= "Analysis started! Check status using task_id",
            check_status_url= f"/status/{task_id}"
        )
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Failed to start analysis: {str(e)}")
    
@app.get("/status/{task_id}")
def check_status(task_id:str):
    job_info = get_job_status(task_id)

    if job_info.get("status") == "not_found":
        raise HTTPException(status_code = 404, detail = "Task Not Found!!")
    
    return job_info

@app.get("/download/{task_id}")
def download_analysis_result(task_id: str):
    # Step 1: Check if task exists
    job_info = jobs.get(task_id)
    if job_info is None:  
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Step 2: Check if analysis is completed
    if job_info.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed yet")
    
    # Step 3: Get file path
    pdf_path = job_info.get("pdf_path")
    if not pdf_path:
        raise HTTPException(status_code=404, detail="PDF file path not found")
    
    # Step 4: Check if file exists on disk
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found on server")
    
    # Step 5: Return file
    filename = os.path.basename(pdf_path)  # Extract filename from path
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename
    )    

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "github-analyzer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000, reload = True)