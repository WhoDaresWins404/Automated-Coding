import os
import subprocess
import requests
import re
from pathlib import Path
from memory_manager import load_memory_context, update_memory_file, start_auto_save_timer

# --- Configuration ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e2b"
REPO_FULL_NAME = "WhoDaresWins404/Automated-Coding"
LOCAL_PATH = "./Automated-Coding"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN environment variable is missing.")

def clone_or_pull_repo():
    if not os.path.exists(LOCAL_PATH):
        print(f"📥 Cloning {REPO_FULL_NAME}...")
        clone_url = f"https://{GITHUB_TOKEN}@github.com/{REPO_FULL_NAME}.git"
        subprocess.run(["git", "clone", clone_url, LOCAL_PATH], check=True)
    else:
        print("🔄 Pulling latest changes...")
        subprocess.run(["git", "pull", "origin", "main"], cwd=LOCAL_PATH, check=True)

def generate_code(llm_context: str, task: str, filename: str) -> str:
    """Generates code based on the current Project Memory and user task."""
    system_prompt = (
        "You are an expert coding assistant. Your output must be RAW CODE ONLY. "
        "No markdown backticks, no explanations, no introductory text. "
        "Follow the project rules defined in the context strictly."
    )
    
    full_prompt = f"""
    {system_prompt}
    
    --- PROJECT MEMORY ---
    {llm_context}
    --- END MEMORY ---
    
    --- CURRENT TASK ---
    Task: {task}
    Target File: {filename}
    --- END TASK ---
    
    Output the raw code for '{filename}':
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 2048
        }
    }

    try:
        print(f"🤖 Querying {MODEL_NAME}...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        raw_output = response.json().get("response", "")
        
        # Clean markdown if model ignores instruction
        cleaned_code = re.sub(r"^```(?:python|py|txt)?\n?", "", raw_output, flags=re.MULTILINE)
        cleaned_code = re.sub(r"```$", "", cleaned_code, flags=re.MULTILINE)
        return cleaned_code.strip()

    except requests.exceptions.RequestException as e:
        print(f"❌ LLM Request Failed: {e}")
        return ""

def commit_and_push(filename: str, content: str, commit_msg: str):
    """Writes file, commits, pushes, and updates memory."""
    full_path = os.path.join(LOCAL_PATH, filename)
    
    if not os.path.exists(os.path.join(LOCAL_PATH, ".git")):
        print(f"❌ Error: No .git folder found in {LOCAL_PATH}.")
        return

    # Write File
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"📝 Wrote {filename} locally.")

    # Git Operations
    try:
        subprocess.run(["git", "add", filename], cwd=LOCAL_PATH, check=True)
        subprocess.run(["git", "commit", "-m", f"feat: {commit_msg}"], cwd=LOCAL_PATH, check=True)
        print("🚀 Pushing to GitHub...")
        subprocess.run(["git", "push", "origin", "main"], cwd=LOCAL_PATH, check=True)
        print("✅ Successfully pushed to GitHub!")
        
        # Update Memory
        update_memory_file("Code Commit", f"Added/Updated {filename}: {commit_msg}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        if "nothing to commit" in str(e.output):
            print("ℹ️  No changes to push.")
        else:
            raise e

def main():
    # Start Auto-Save Timer
    start_auto_save_timer(interval_minutes=15)
    
    # Ensure Repo exists
    clone_or_pull_repo()
    
    # Load Memory
    memory_context = load_memory_context()
    
    # Define Task (Example: Initialize Project Scope)
    # If memory is empty, this task will ask the LLM to define the project.
    task = "Initialize the project. Based on the memory, define the tech stack, objectives, and create a 'README.md' with the project scope. If the memory is empty, propose a generic Python CLI tool structure."
    filename = "README.md"
    commit_message = "Initialize project scope and README"

    # Generate
    print("🧠 Loading Project Memory...")
    print(memory_context)
    
    code = generate_code(memory_context, task, filename)
    
    if not code:
        print("No code generated. Aborting.")
        return

    # Push
    commit_and_push(filename, code, commit_message)

if __name__ == "__main__":
    main()