from utils.llm_client import get_llm

def doc_agent(state):

    llm = get_llm()

    readme = state.get("readme_content", "")
    commits = state.get("commit_history", [])
    comments = state.get("comments_summary", [])

    commit_text = "\n".join([f"- {c['date']} by {c['author']}: {c['message']}" for c in commits[:10]])
    comment_text = "\n".join([
        f"{c.get('file_path', 'unknown file')} → Single-line: {len(c.get('single_line_comments', []))} | Docstrings: {len(c.get('docstrings', []))}"
        for c in comments
    ])

    full_prompt = f"""
You are an expert software documenter.

Create a comprehensive technical documentation for this codebase using the following data:

---

README:
{readme}

Code Comments Summary:
{comment_text}

Recent Commit History:
{commit_text}

---

The documentation should be:
- Easy to follow
- Include overview, usage, architecture summary
- Markdown formatted
- Avoid repeating raw commit messages or comments

Start below:
"""
    response = llm.invoke(full_prompt)
    state["project_docs"] = response.content
    return state
