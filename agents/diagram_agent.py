from utils.llm_client import get_llm

def diagram_agent(state):
    llm = get_llm()
    parsed_files = state.get("parsed_files", [])

    # Prepare file structure overview
    file_lines = []
    for f in parsed_files:
        file_lines.append(f"{f['language']} -> {f['path']}")

    file_text = "\n".join(file_lines)

    prompt = f"""
You are a software architect assistant.

Based on the following project file structure, generate a high-level architecture diagram in **Mermaid format**:

---

📁 File Structure:
{file_text}

---

Requirements:
- Use `graph TD` or `graph LR`
- Show main modules, submodules, and key files
- Group related components together
- Make it clear and readable

Only return the mermaid code block. Do NOT explain anything.
"""

    result = llm.invoke(prompt)
    diagram_md = result.content.strip()

    state["diagram_mermaid"] = diagram_md
    state["diagram_status"] = "success" if diagram_md else "empty"
    return state
