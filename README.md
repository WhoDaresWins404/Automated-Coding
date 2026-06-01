# AutoTrainer-Pipeline

A semi-automatic system designed to automate the entire machine learning training pipeline, incorporating human approval checkpoints for critical decisions (data refinement, hyperparameter selection).

## 🎯 Project Objectives

The primary goal of the AutoTrainer-Pipeline is to create an efficient, reproducible, and human-in-the-loop system for training machine learning models.

1.  **Automation:** Automate data collection, refinement, and model training.
2.  **Human Oversight:** Enforce mandatory human approval at critical checkpoints (data approval, hyperparameter selection).
3.  **Evaluation:** Implement robust evaluation against both standard metrics and a Golden Dataset.

## 🛠️ Tech Stack

*   **Language:** Python 3.11+
*   **Web Framework:** FastAPI (for API and workflow management)
*   **Deep Learning:** PyTorch, Hugging Face Transformers
*   **Data Processing:** Polars (for high-speed data manipulation)
*   **Database:** SQLite (for metadata, logs, and approval states)
*   **Data Storage:** Parquet (for raw data storage)

## ⚙️ Data & Storage Strategy

*   **Raw Data:** Stored in **Parquet** files for fast I/O operations.
*   **Metadata & Logs:** Stored in **SQLite** for tracking workflow status, user approvals, and training logs.

## 🔄 Semi-Automatic Workflow

The system follows a structured, human-in-the-loop workflow:

1.  **Data Collection & Refinement:** System auto-collects and refines raw data.
    *   **Checkpoint:** **Human Approval Required** before proceeding to training.
2.  **Model Training:** System auto-trains the model based on approved data.
    *   **Checkpoint:** **Human Selection** of Hyperparameters/Architecture required.
3.  **Evaluation:** Model performance is evaluated against **Standard Metrics** and the **Golden Dataset** thresholds.

## 🗺️ Active Roadmap

The project is currently in the Initialization Phase, with the following planned phases:

1.  [ ] **Phase 1:** Setup project structure, FastAPI backend, and storage (Parquet/SQLite).
2.  [ ] **Phase 2:** Build Data Collector & Refiner modules with approval workflow.
3.  [ ] **Phase 3:** Implement Training Pipeline with Human-in-the-Loop hyperparameter selection.
4.  [ ] **Phase 4:** Build Evaluation Engine (Metrics + Golden Dataset comparison).
5.  [ ] **Phase 5:** Create Web Dashboard for monitoring and approval.