# How to Run the Backend

## Option 1: Docker (Recommended)
This runs the Backend, Database (Postgres), and Redis together.

1.  Navigate to the project root (parent directory):
    ```bash
    cd ..
    ```
2.  Start the services:
    ```bash
    docker compose up --build
    ```

## Option 2: Manual (Local Python)
*Requires Postgres and Redis to be running separately.*

1.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```
