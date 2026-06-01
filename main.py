
#### **`main.py`**
```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from pathlib import Path

app = FastAPI(title="AutoTrainer-Pipeline", version="0.1.0")

# Mount static files (if you add a frontend later)
# app.mount("/static", StaticFiles(directory="ui/static"), name="static")

@app.get("/")
async def root():
    return {"message": "AutoTrainer-Pipeline is running. Check /docs for API."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/api/status")
async def get_status():
    """Returns the current project status from memory."""
    try:
        memory_path = Path("PROJECT_MEMORY.md")
        if memory_path.exists():
            return {"memory_loaded": True, "last_updated": "2026-06-01"}
        else:
            return {"memory_loaded": False, "message": "Memory file not found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)