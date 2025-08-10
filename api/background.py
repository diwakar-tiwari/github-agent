import threading
import uuid
import time
from datetime import datetime
from main import build_graph, RepoState

jobs = {}  ## global job storage, later use database

## background worker function
def run_analysis_background(task_id: str, repo_url: str):
    """This will run in separate thread"""
    try:
        jobs[task_id]["status"] = "processing"

        graph = build_graph()
        initial_state = RepoState({"repo_url":repo_url})
        final_state = graph.invoke(initial_state)

        print(f"README found: {bool(final_state.get('readme_content'))}")
        print(f"Commits found: {len(final_state.get('commit_history', []))}")
        print(f"Comments found: {len(final_state.get('comments_summary', []))}")
        print(f"Doc content length: {len(final_state.get('project_docs', ''))}")


        jobs[task_id]["status"] = "completed"
        jobs[task_id]["pdf_path"] = final_state.get("pdf_path")
    
    except Exception as e:
        jobs[task_id]["status"] = "failed"
        jobs[task_id]["error"] = str(e)


## job starter function
def start_analysis(repo_url:str, user_id: str):
    """create job and start background function(worker)"""

    # unique id for each job
    task_id = str(uuid.uuid4())[:8]

    # create job entry
    jobs[task_id] = {
        "task_id": task_id,
        "repo_url": repo_url,
        "user_id": user_id,
        "status" : "started",
        "created_at": datetime.now().isoformat()
    }

    # now start the background work
    thread = threading.Thread(target=run_analysis_background, args=(task_id, repo_url))
    thread.start()

    return task_id

def get_job_status(task_id: str):
    return jobs.get(task_id, {"status":"not_found"})


