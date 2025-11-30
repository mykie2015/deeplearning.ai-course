import os
import argparse

# Configuration defaults
DEFAULT_OUTPUT_FILE = "codebase_context.md"
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', 'env', '.idea', '.vscode', 'dist', 'build', '.DS_Store', '.venv'}
IGNORE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pyc', '.exe', '.bin', '.dll', '.so', '.dylib', '.class', '.jar', '.DS_Store'}

def get_repo_content(root_path, output_file_name):
    output = []
    output.append(f"# Codebase Dump for: {os.path.basename(os.path.abspath(root_path))}\n\n")
    
    # 1. Generate Tree Structure
    output.append("## Project Structure\n```\n")
    for root, dirs, files in os.walk(root_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(root_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output.append(f"{indent}{os.path.basename(root)}/\n")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not any(f.endswith(ext) for ext in IGNORE_EXTS) and f != output_file_name:
                output.append(f"{subindent}{f}\n")
    output.append("```\n\n")

    # 2. Dump File Contents
    output.append("## File Contents\n")
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTS):
                continue
            
            # Skip the output file itself if it's in the path
            if file == output_file_name:
                continue
                
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_path)
            
            output.append(f"\n### File: `{relative_path}`\n")
            # Determine language for markdown code block
            ext = file.split('.')[-1] if '.' in file else ''
            output.append(f"```{ext}\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    output.append(f.read())
            except Exception as e:
                output.append(f"Error reading file: {e}")
            
            output.append("\n```\n")
            
    return "".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a markdown file containing the codebase context.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the project folder (default: current directory)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_FILE, help=f"Output markdown file name (default: {DEFAULT_OUTPUT_FILE})")
    
    args = parser.parse_args()
    
    target_folder = args.path
    output_file = args.output
    
    if not os.path.exists(target_folder):
        print(f"Error: Target folder '{target_folder}' does not exist.")
        exit(1)
        
    print(f"Scanning {os.path.abspath(target_folder)}...")
    full_text = get_repo_content(target_folder, output_file)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"✅ Generated {output_file} ({len(full_text)} characters)")
    print("👉 Now upload this file to your LLM for context.")
