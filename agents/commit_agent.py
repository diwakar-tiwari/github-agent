import subprocess
import os

def extract_git_commits(repo_path, max_commits=50):

    try:
        result = subprocess.run(  ## subprocess used to run shell command inside python
            ["git", "log", f"--max-count={max_commits}", "--pretty=format:%H|||%an|||%ad|||%s", "--date=short"],
            # h -> hash, an -> author name, ad -> date, s -> commit message
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        lines = result.stdout.strip().split("\n")
        commits = []

        for line in lines:
            parts = line.strip().split("|||")
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "message": parts[3]
                })

        return commits

    except subprocess.CalledProcessError as e:
        print("Error running git log:", e.stderr)
        return []

def commit_agent(state):
    repo_path = state.get("local_repo_path")
    if not repo_path or not os.path.exists(repo_path):
        state["commit_history"] = []
        state["commit_status"] = "error"
        return state

    commits = extract_git_commits(repo_path)
    state["commit_history"] = commits
    state["commit_status"] = "success" if commits else "empty"
    return state
