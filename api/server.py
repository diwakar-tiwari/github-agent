from fastapi import FastAPI, HTTPException
from api.models import AnalysisRequest, AnalysisResponse, StatusResponse
import uvicorn

# import background functions
from api.background import start_analysis, get_job_status

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

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "github-analyzer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000, reload = True)