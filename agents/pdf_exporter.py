import os
from datetime import datetime

def export_docs_as_pdf(state, output_dir="outputs"):
    """
    Convert generated documentation (with mermaid diagram) to PDF
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = state.get("project_docs", "")
    diagram = state.get("diagram_mermaid", "")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_filename = f"{output_dir}/final_docs_{timestamp}.md"
    pdf_filename = md_filename.replace(".md", ".pdf")

    # Final markdown content
    full_markdown = f"""
# 📝 Project Documentation

{doc}

---

## 🔍 Architecture Diagram (Mermaid)

```mermaid
{diagram}
"""
    # Save markdown file
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(full_markdown)

    # Convert using md-to-pdf
    print("📄 Converting markdown to PDF...")
    os.system(f"md-to-pdf {md_filename} --output {pdf_filename}")

    state["pdf_path"] = pdf_filename
    state["pdf_status"] = "success" if os.path.exists(pdf_filename) else "error"
    return state
