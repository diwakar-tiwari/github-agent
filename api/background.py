import threading
import uuid
from datetime import datetime
import sys
import os
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import build_graph, RepoState

jobs = {}  ## global job storage, later use database

## background worker function
def run_analysis_background(task_id: str, repo_url: str):
    """This will run in separate thread"""
    start_time = datetime.now()


    try:
        jobs[task_id]["status"] = "processing"

        graph = build_graph()
        initial_state = RepoState({"repo_url":repo_url})
        final_state = graph.invoke(initial_state)

        print(f"README found: {bool(final_state.get('readme_content'))}")
        print(f"Commits found: {len(final_state.get('commit_history', []))}")
        print(f"Comments found: {len(final_state.get('comments_summary', []))}")
        print(f"Doc content length: {len(final_state.get('project_docs', ''))}")

         # Calculate processing time
        end_time = datetime.now()
        processing_time = str(end_time - start_time)



        jobs[task_id]["status"] = "completed"
        jobs[task_id]["pdf_path"] = final_state.get("pdf_path")
        jobs[task_id]["processing_time"] = processing_time

    
    except Exception as e:
        jobs[task_id]["status"] = "failed"
        jobs[task_id]["error"] = str(e)


## job starter function
def start_analysis(repo_url:str, user_id: str):
    """create job and start background function(worker)"""

    # unique id for each job
    task_id = str(uuid.uuid4())[:8]
    logger.info(f"Starting analysis for {repo_url} with task ID {task_id}")
    logger.debug(f"Jobs before starting: {jobs}")
    # create job entry
    jobs[task_id] = {
        "task_id": task_id,
        "repo_url": repo_url,
        "user_id": user_id,
        "status" : "started",
        "created_at": datetime.now().isoformat(),
        "pdf_path": None,        
        "error": None,           
        "processing_time": None 
    }
    logger.info(f"Job created: {jobs[task_id]}")
    logger.debug(f"Jobs after creating: {jobs}")

    # now start the background work
    thread = threading.Thread(target=run_analysis_background, args=(task_id, repo_url))
    thread.start()

    return task_id

def get_job_status(task_id: str):
    return jobs.get(task_id, {"status":"not_found"})


