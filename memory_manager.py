import os
import time
import threading
from datetime import datetime
from pathlib import Path

MEMORY_FILE = "PROJECT_MEMORY.md"
LOCAL_PATH = "./Automated-Coding"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

def load_memory_context():
    """Reads the current state from PROJECT_MEMORY.md for the LLM prompt."""
    memory_path = os.path.join(LOCAL_PATH, MEMORY_FILE)
    if not os.path.exists(memory_path):
        # Return empty context if file doesn't exist
        return "No project memory found. Awaiting initial definition."
    
    with open(memory_path, "r", encoding="utf-8") as f:
        return f.read()

def update_memory_file(action: str, details: str, is_auto_save: bool = False):
    """
    Updates the memory file with a new log entry and timestamp.
    If is_auto_save, it just updates the timestamp without adding a log entry.
    """
    memory_path = os.path.join(LOCAL_PATH, MEMORY_FILE)
    now = get_timestamp()
    
    # Create file if it doesn't exist
    if not os.path.exists(memory_path):
        with open(memory_path, "w", encoding="utf-8") as f:
            f.write(f"""# 🧠 Automated Coding Project Memory
**Last Updated:** {now}
**Status:** Active

## 🎯 Project Objectives & Rules of Engagement
- **Primary Goal:** [To be defined]
- **Tech Stack:** [To be defined]
- **Rules:**
  - [To be defined]

## 📂 Current State & History
- **v0.0 ({now}):** Project initialized.

## 🚧 Active Roadmap
1. [ ] Define project scope.

## 📝 Recent Changes Log
- {now}: Project initialized.
""")
        print(f"✅ Created new memory file: {MEMORY_FILE}")
        return

    # Read existing content
    with open(memory_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update Timestamp in Header
    # Simple regex to replace the first "Last Updated" line
    import re
    content = re.sub(r"\*\*Last Updated:\*\* .+", f"**Last Updated:** {now}", content, count=1)

    # Add Log Entry if not auto-save
    if not is_auto_save:
        log_entry = f"- {now}: {action} - {details}\n"
        # Find "## 📝 Recent Changes Log" and insert after
        if "## 📝 Recent Changes Log" in content:
            content = content.replace(
                "## 📝 Recent Changes Log", 
                f"## 📝 Recent Changes Log\n{log_entry}"
            )
        else:
            content += f"\n## 📝 Recent Changes Log\n{log_entry}"

    # Write back
    with open(memory_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    if is_auto_save:
        print(f"💾 Auto-saved memory state (no changes).")
    else:
        print(f"📝 Updated memory: {action}")

def start_auto_save_timer(interval_minutes=15):
    """Starts a background thread to auto-save memory every X minutes."""
    def save_loop():
        while True:
            time.sleep(interval_minutes * 60)
            update_memory_file("Auto-Save", "Periodic state update", is_auto_save=True)
    
    thread = threading.Thread(target=save_loop, daemon=True)
    thread.start()
    print(f"⏱️  Auto-save timer started (every {interval_minutes} minutes).")