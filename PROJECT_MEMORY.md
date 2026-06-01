# 🧠 Project Memory: AutoTrainer-Pipeline
**Last Updated:** 2026-06-01 15:30:00 UTC
**Status:** Phase 1 Complete - Structure & Storage

## 🎯 Project Objectives & Rules of Engagement
- **Primary Goal:** Build a semi-automatic model training tool in Python.
- **Tech Stack:** Python 3.11+, FastAPI, Polars, SQLite. (ML Framework: PyTorch - to be installed separately).
- **Rules:**
  - **Isolation:** Standalone project. No dependencies on EverQuest, Proxy, or Scanner code.
  - **Data Format:** Raw data stored in **Parquet** (Polars) + **SQLite** for metadata.
  - **Semi-Automatic Workflow:**
    1. Auto-collect/refine data -> **Human Approval** required.
    2. Auto-train -> **Human Selection** of hyperparameters/architecture required.
    3. Evaluate against **Standard Metrics** AND **Golden Dataset**.
  - **Code Quality:** Type-hinted, modular, documented.
  - **Windows 11 Compatibility:** Ensure all dependencies work on Windows 11.

## 📂 Current State & History
- **v0.0 (2026-06-01):** Project initialized.
- **v0.1 (2026-06-01):** Defined architecture (FastAPI + Polars + SQLite).
- **v0.2 (2026-06-01):** **COMMITTED.** Initial structure, storage logic, and FastAPI skeleton created.
- **v0.3 (2026-06-01):** Created `pipeline/collector.py` with data ingestion and approval workflow.

## 🚧 Active Roadmap
1. [x] **Phase 1:** Setup project structure, FastAPI backend, and storage.
2. [ ] **Phase 2:** Build Data Collector & Refiner modules with approval workflow.
3. [ ] **Phase 3:** Implement Training Pipeline (PyTorch integration pending).
4. [ ] **Phase 4:** Build Evaluation Engine.
5. [ ] **Phase 5:** Create Web Dashboard.

## 📝 Recent Changes Log
- 2026-06-01 15:00: Project initialized.
- 2026-06-01 15:30: Committed initial files (main.py, storage.py, requirements.txt).