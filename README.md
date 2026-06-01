# 🚀 AutoTrainer-Pipeline

A **semi-automatic model training tool** built in Python. This project automates the end-to-end ML lifecycle while enforcing human oversight at critical decision points (data approval, architecture selection).

## 🏗️ Core Features
- **Data Pipeline:** Automated collection, refinement, and central storage (Parquet).
- **Human-in-the-Loop:** Approve datasets and select hyperparameters before training.
- **Evaluation Engine:** Standard metrics (Accuracy, F1, Loss) + **Golden Dataset** validation.
- **Web Dashboard:** FastAPI-based UI for monitoring, approval, and control.
- **Modular Architecture:** Isolated, extensible components.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Async, High Performance)
- **ML Framework:** PyTorch + Hugging Face Transformers
- **Data Storage:** Parquet (Raw Data) + SQLite (Metadata/Logs)
- **Data Processing:** Polars (Fast DataFrame operations)
- **Deployment:** Pure Python (No Docker)

## 📂 Project Structure
```bash
AutoTrainer-Pipeline/
├── core/               # Base classes, storage interfaces, utils
├── pipeline/           # Collector, Refiner, Trainer, Evaluator modules
├── ui/                 # FastAPI endpoints and static HTML/JS
├── config/             # YAML configs for hyperparameters and paths
├── data/               # Parquet files, SQLite DB (GITIGNORED)
├── tests/              # Unit tests for pipeline logic
├── main.py             # FastAPI entry point
├── requirements.txt    # Dependencies
└── PROJECT_MEMORY.md   # Living memory for LLM context