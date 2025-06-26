import os
import re
from tqdm import tqdm

SOURCE_EXTENSIONS = ['.py', '.js', '.ts', '.java', '.go', '.cpp', '.c', '.rb']

def is_source_file(filename):
    for ext in SOURCE_EXTENSIONS:
        if filename.endswith(ext):
            return True
    return False

def count_func_classes(content):
    func_matches = re.findall(r'\bdef\b|\bfunction\b|\bfn\b|\bfunc\b', content)
    class_matches = re.findall(r'\bclass\b', content)
    return len(func_matches), len(class_matches)

def detect_language(filename):
    ext = os.path.splitext(filename)[1]
    return {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.go': 'Go',
        '.cpp': 'C++',
        '.c': 'C',
        '.rb': 'Ruby'
    }.get(ext, 'Unknown')




def parser_agent(state):
    repo_path = state.get("local_repo_path")
    if not repo_path or not os.path.exists(repo_path):
        state["parser_status"] = "error"
        state["parser_error"] = "Invalid repo path"
        return state
    
    parsed_files = []

    for root, dirs, files in tqdm(os.walk(repo_path), desc="Parsing codebase"):
        for file in files:
            filepath = os.path.join(root, file)
            if is_source_file(file):
                try:
                    with open(filepath, 'r', encoding="utf-8", errors= 'ignore') as f:
                        content = f.read()
                        num_lines = len(content.splitlines())
                        num_func, num_classes = count_func_classes(content)
                        language = detect_language(file)

                        parsed_files.append({
                            "file_path": filepath,
                            "language": language,
                            "lines": num_lines,
                            "functions": num_func,
                            "classes": num_classes
                        })
                
                except Exception as e:
                    print(f"Failed to read {filepath}: {e}")

    print("Setting state....")
    state["parsed_files"] = parsed_files
    state["parsed_status"] = "success"

    for file in parsed_files:
        print("Parsed data from Parser file..")
        print(f"File: {file['file_path']}")
        print(f"Language: {file['language']}")
        print(f"Lines: {file['lines']}")
        print(f"Functions: {file['functions']}")
        print(f"Classes: {file['classes']}")
    return state

