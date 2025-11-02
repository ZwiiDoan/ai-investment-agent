# Month 1 - Week 1 - Day 2

## Backend Setup (Python + FastAPI)

### Goal

Stand up a working **FastAPI project** that will serve as the API backbone for the AI Investment Agent.

### Tasks

1. **Project Initialization**
   - Create a new project folder `ai_investment_agent/`.
   - Set up a virtual environment:  

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - Install FastAPI and Uvicorn:  

     ```bash
     pip install fastapi uvicorn
     ```

2. **Hello World Endpoint**
   - Create `main.py`:

     ```python
     from fastapi import FastAPI

     app = FastAPI()

     @app.get("/")
     def read_root():
         return {"message": "AI Investment Agent API is running"}
     ```

   - Run server:  

     ```bash
     uvicorn main:app --reload
     ```

3. **Basic Project Structure**

   ```plaintext
   ai_investment_agent/
   ├── main.py
   ├── app/
   │   ├── __init__.py
   │   ├── routes/
   │   │   └── __init__.py
   │   └── services/
   │       └── __init__.py
   └── requirements.txt
   ```

4. **Version Control**
   - Initialize Git repo.
   - Add `.gitignore` for Python/venv.
   - First commit with base FastAPI project.

5. **Stretch Goal**
   - Add `/health` endpoint returning status, version, and timestamp.  
   - Example:  

     ```json
     {"status": "ok", "version": "0.1.0", "timestamp": "2025-09-30T10:00:00Z"}
     ```

---

✅ **Output for Day 2:**  
A running FastAPI backend with root and health endpoints, committed to GitHub/GitLab.
