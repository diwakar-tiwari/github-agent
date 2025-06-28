import os

def readme_agent(state):
    repo_path = state("repo_path"," ")

    # Possible file names for README
    readme_files = ["README.md", "README.txt", "README.rst", "README"]

    readme_content = None

    for fname in readme_files:
        fpath = os.path.join(repo_path, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    readme_content = f.read()
                break

            except Exception as e:
                print(f"Error reading {fpath}: {e}")
    
    if readme_content:
        state["readme_content"] = readme_content
        state["readme_status"] = "success"
    else:
        state["readme_content"] = None
        state["readme_status"] = "not_found"

    return state
