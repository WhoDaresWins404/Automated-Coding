# 🧠 Project Memory: AutoTrainer-Pipeline
**Last Updated:** 2026-06-01 15:00:00 UTC
**Status:** Initialization Phase

## 🎯 Project Objectives & Rules of Engagement
- **Primary Goal:** Build a semi-automatic model training tool that automates data collection, refinement, and training, while enforcing human approval at critical checkpoints.
- **Tech Stack:** Python 3.11+, FastAPI, PyTorch, Polars, SQLite, Hugging Face Transformers.
- **Rules:**
  - **Isolation:** This project is completely standalone. No dependencies on external EverQuest, Proxy, or Scanner code.
  - **Data Format:** Raw data stored in **Parquet** for speed. Metadata and logs in **SQLite**.
  - **Semi-Automatic Workflow:**
    1. System auto-collects/refines data -> **Human Approval Required** before training.
    2. System auto-trains -> **Human Selection** of Hyperparameters/Architecture required.
    3. Evaluation against **Standard Metrics** AND **Golden Dataset** thresholds.
  - **Code Quality:** All code must be type-hinted, modular, and documented.
  - **No Docker:** Pure Python deployment (no containerization for this phase).

## 📂 Current State & History
- **v0.0 (2026-06-01):** Project initialized. No code committed yet.
- **v0.1 (2026-06-01):** Defined architecture (FastAPI + PyTorch + Parquet/SQLite).

## 🚧 Active Roadmap
1. [ ] **Phase 1:** Setup project structure, FastAPI backend, and storage (Parquet/SQLite).
2. [ ] **Phase 2:** Build Data Collector & Refiner modules with approval workflow.
3. [ ] **Phase 3:** Implement Training Pipeline with Human-in-the-Loop hyperparameter selection.
4. [ ] **Phase 4:** Build Evaluation Engine (Metrics + Golden Dataset comparison).
5. [ ] **Phase 5:** Create Web Dashboard for monitoring and approval.

## 📝 Recent Changes Log
- 2026-06-01 15:00: Project initialized with memory definition.