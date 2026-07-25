
# CodeMatch - Live Claude Rerank Integration

This repository is a standalone submission snapshot of the CodeMatch
full-stack system with the tested Claude reranker integrated into its live
search path. The original shared CodeMatch repository was not modified.

## What the integration adds

1. The existing embedding model retrieves eight candidates.
2. Claude reviews and reranks only the top five.
3. Results 6-8 retain their embedding-search order.
4. The UI defaults to the AI-reranked order and marks reviewed results.
5. Provider, network, timeout, malformed-output, and other handled rerank
   failures degrade to the original embedding order.
6. Results without retrievable source content are retained rather than
   disappearing from the response.

### Runtime model distinction

- The recorded full-stack demo uses `microsoft/codebert-base` for embedding
  retrieval.
- Claude is the second-stage judge over the retrieved top five.
- Qwen2.5-Coder-0.5B-pe was the preferred embedding model in the separate
  benchmark comparison; it is not the active embedding runtime in this
  snapshot.

### Focused safeguard tests

The lightweight live-rerank tests do not download an embedding model:

```bash
cd backend
python -m pytest -q tests/test_live_rerank.py
```

They verify provider-failure fallback, preservation of partial missing-content
results, and duplicate-label handling.

## Original system context

The system workflow covers retrieving open-source code, embedding and storing
it in Qdrant, and returning similar projects through a FastAPI backend and Vue
frontend.

## 🖥️ User Interface Overview

- **Main Page**: Enter the desired code snippet to find existing GitHub projects with similar code.  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/43bc9da3-689d-4077-8194-0daf9de8ea92" alt="Inputted Code" width="1000">
  </div>

- **Similar GitHub Projects Page**: Displays all the GitHub projects with code similar to the input.  
  <div align="center">
    <img src="https://github.com/user-attachments/assets/21bae129-d765-4246-ae6e-2861ba02d685" alt="Search Results" width="1000">
  </div>


## ⚙️ General Components

The system consists of two main components essential for its operation:

### System Workflow
This includes the structure of the backend and frontend, along with their integration with the database.

<img src="https://github.com/user-attachments/assets/5232c3ac-cc52-42fa-b7b5-8dbecb11dc2a" alt="Workflow" width="500">

<br>

### Populate Database
This step involves retrieving code projects from GitHub to populate the database with data.

<img src="https://github.com/user-attachments/assets/d6656be1-762f-4a78-978d-8db500746e4a" alt="Workflow" width="700">

(This step is implemented in
[`backend/app/populate_database.py`](backend/app/populate_database.py).)


## 📦🛠️ Installation and Run

### 📥 **Prerequisites**:

1. **Python**: 3.9+  
2. **Docker Desktop**:  
   [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

3. **Qdrant**:  
   [Download and Run Qdrant](https://qdrant.tech/documentation/quickstart/) – Follow the **Download and Run** section for installation.

4. **Node.js and npm**:  
   a. Install from [Node.js](https://nodejs.org/en) – Keep the option checked to install necessary tools.  
   b. Verify installation:  
   ```bash
   npm -v
   ```

5. **Clone the Repository**:
   ```bash
   git clone https://github.com/YuvalBakirov/codematch-system.git
   ```

6. **Acquire Access to The-Stack-V2 Dataset**:   
   a. [Get access to The-Stack-V2 dataset](https://huggingface.co/datasets/bigcode/the-stack-v2-train-smol-ids)  
   b. [Create a Hugging Face personal access token](https://huggingface.co/settings/tokens/new?tokenType=read)  
   c. Add the token to the `.env` file in the root directory:  
   ```plaintext
   HUGGING_FACE_TOKEN=<paste your token here>
   ```

---

### 🐳 **Running with Docker**

1. **Ensure you are in the project root directory (`system`)**.

2. **Start all services**:
   ```bash
   docker-compose up
   ```
   - This launches:
     - Backend API at [http://localhost:8000](http://localhost:8000)
     - Frontend at [http://localhost:8080](http://localhost:8080)
     - Qdrant Dashboard at [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

3. **Populate the Database**:
   ```bash
   cd backend
   $env:PYTHONPATH = (Get-Location).Path  # Ensure the path ends with 'backend' (check with `Write-Output $env:PYTHONPATH`)
   python populate_database.py
   ```

---
   
### 💻 **Running Locally**

#### **Installation**

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   ```
   

#### **Run**

1. **Ensure you are in the project root directory (ends with `system`)**.

2. **Terminal 1**: Start the frontend:
   ```bash
   cd frontend
   npm run serve
   ```
   - Access the Vue.js frontend at [http://localhost:8080](http://localhost:8080).

3. **Terminal 2**: Start the backend:
   ```bash
   $env:PYTHONPATH = (Get-Location).Path  # Ensure the path ends with 'backend' (check with `Write-Output $env:PYTHONPATH`)
   cd backend
   uvicorn backend.main:app --reload
   ```
   - The backend API will be available at [http://localhost:8000](http://localhost:8000).

4. **Terminal 3**: Start the Qdrant database:  
   If installed separately, run Qdrant per its documentation. If a script (`qdrant_server.py`) is included in this project:
   ```bash
   cd backend
   python qdrant_server.py
   ```

5. **Populate the Vector Database**:
   ```bash
   cd backend
   python populate_database.py
   ```
   - Verify the database is populated by checking the Qdrant dashboard at [http://localhost:6333/dashboard](http://localhost:6333/dashboard).
