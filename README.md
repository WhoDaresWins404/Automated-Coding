# AutoTrainer-Pipeline

AutoTrainer-Pipeline is a semi-automatic framework designed to streamline the machine learning workflow, automating data collection, model training, and evaluation. It provides a structured backend using FastAPI, leveraging Polars for efficient data handling and SQLite for metadata storage.

## 🎯 Project Objectives

The primary goal of this project is to create a robust, semi-automatic system that minimizes manual intervention while maintaining human oversight at critical decision points.

1.  **Automated Data Management:** Implement modules for auto-collecting and refining data, requiring human approval before proceeding.
2.  **Automated Training:** Facilitate the training process automatically, allowing human selection of hyperparameters and architecture.
3.  **Standardized Evaluation:** Ensure rigorous evaluation of trained models against both standard metrics and a defined Golden Dataset.
4.  **Efficient Storage:** Utilize Parquet (via Polars) for large dataset storage and SQLite for managing pipeline metadata.

## 🛠️ Tech Stack

*   **Language:** Python 3.11+
*   **Backend Framework:** FastAPI
*   **Data Processing:** Polars (for high-performance data manipulation)
*   **Database:** SQLite (for metadata and configuration)
*   **Machine Learning:** PyTorch (for model training)
*   **Data Storage Format:** Parquet
*   **Compatibility:** Designed for Windows 11 compatibility.

## ⚙️ Architecture & Workflow

The system follows a modular, pipeline-based approach:

1.  **Data Ingestion & Refinement:** Modules handle data collection and refinement, requiring explicit human approval before data is committed to the training queue.
2.  **Training Engine:** The core engine automatically initiates training based on approved data and user-defined parameters.
3.  **Evaluation Layer:** Models are automatically evaluated against predefined standards and the Golden Dataset.
4.  **API Interface:** FastAPI provides a RESTful interface for managing the pipeline state, triggering actions, and viewing results.

## 🚀 Getting Started

### Prerequisites

*   Python 3.11+
*   Git

### Installation

Clone the repository and install dependencies:

bash
git clone [repository-url]
cd AutoTrainer-Pipeline
pip install -r requirements.txt

### Running the Application

The FastAPI backend can be started using:

bash
python main.py

The system is designed to be run in a modular fashion, allowing individual components (Collector, Trainer, Evaluator) to be invoked via the API.