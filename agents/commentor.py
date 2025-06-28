import re

def extract_python_comment(code):

    #single line comment
    single_line_comments = re.findall(r'^\s*#.*', code, flags=re.MULTILINE)

    ## multiline docstring
    docstrings = re.findall(r'("""|\'\'\')(.*?)\1', code, flags=re.DOTALL)

    ## extract docstring from tuples
    docstrings = [ds[1].strip() for ds in docstrings]

    return single_line_comments, docstrings

def extract_js_comment(code):
    single_line_comments = re.findall(r'^\s*//.*', code, flags=re.MULTILINE)

    multiline_comments = re.findall(r'/\*(.*?)\*/', code, flags=re.DOTALL)

    multiline_comments = [c.strip() for c in multiline_comments]

    return single_line_comments, multiline_comments





def commentor_agent(state):
    parsed_files = state.get("parsed_files",[])
    comments_summary = []

    for file_info in parsed_files:
        file_path = file_info["file_path"]
        language = file_info["language"]

        try:
            with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                code = f.read()

            if language == "Python":
                single_comments, docstrings = extract_python_comment(code)
            elif language == "JavaScript":
                single_comments, docstrings = extract_js_comment(code)
            else:
                single_comments, docstrings = [], []
            
            comments_summary.append({
                "file_path":file_path,
                "language": language,
                "single_line_comments": single_comments,
                "docstrings": docstrings
            })
        
        except Exception as e:
            print(f"Error reading {file_path}:{e}")

    state["comments_summary"] = comments_summary
    state["commentor_status"] = "success"
    return state