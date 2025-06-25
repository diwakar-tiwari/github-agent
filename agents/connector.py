import os
import shutil
from git import Repo
from dotenv import load_dotenv

load_dotenv()

def connector_agent(state):
    print("🚀 Connector Agent Started")
    repo_url = state.get("repo_url")
    local_path = "cloned_repo"

    print("Repo_URL", repo_url)

    if not repo_url:
        state["clone_status"] = "error"
        state["error"] = "Missing 'repo_url' in state."
        return state

    print(f"📦 Cloning repo: {repo_url}")


    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    ## handle private repo
    token = os.getenv("GITHUB_TOKEN")
    if token and "github.com" in repo_url:
        if "@" not in repo_url:
            repo_url = repo_url.replace("https://", f"https://{token}@")
    
    try:
        print(f"Cloning repo from {repo_url}")
        Repo.clone_from(repo_url, local_path)
        state["local_repo_path"] = local_path
        state["clone_status"] = "success"
    except Exception as e:
        state["clone_status"] = "error"
        state["error"] = str(e)
    
    return state
