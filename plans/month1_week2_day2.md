**Month 1 – Week 2 – Day 2** corresponds to **Core Backend Coding** in your cadence and follows the roadmap for Week 2 in your Month 1 plan.

---

### **Objective**

Implement backend logic for **document storage and retrieval** in FastAPI.

---

### **Tasks**

1. **Add Document Endpoint**

   * Create `/documents` endpoint:

     * `POST /documents` → store document (title, text, optional metadata).
     * `GET /documents/{id}` → retrieve document.

2. **Data Model**

   * Define Pydantic model:

     ```python
     from pydantic import BaseModel
     class Document(BaseModel):
         id: str | None = None
         title: str
         text: str
         metadata: dict | None = None
     ```

   * Use in-memory store for now (e.g., `dict` or `list`).

3. **Persistence (Optional)**

   * Prepare for switch to PostgreSQL with pgvector in future.
   * Abstract CRUD functions (e.g., `save_document`, `get_document`).

4. **FastAPI Integration**

   * Update app structure:

     ```
     app/
       ├── main.py
       ├── models.py
       ├── routes/
       │    └── documents.py
       ├── services/
       │    └── storage.py
     ```

5. **Test**

   * Run locally with:

     ```
     uvicorn app.main:app --reload
     ```

   * Verify POST and GET endpoints in browser or Postman.

---

### **Expected Output**

* Functional backend storing documents in-memory.
* Clean folder structure for modular scaling.
* Prep for embeddings integration (next session).

Would you like the exact code implementation for this FastAPI day?
