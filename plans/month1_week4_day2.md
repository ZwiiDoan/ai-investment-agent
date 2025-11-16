**Month 1 – Week 4, Day 2: Core Backend Coding (1h)**

Focus:
Implement lightweight authentication for your FastAPI backend.

### Tasks

1. **Add JWT or API key authentication**

   * Use `fastapi.security.APIKeyHeader` or `HTTPBearer` for quick protection of endpoints.
   * Store valid tokens in `.env` or a config file.

2. **Integrate auth with existing routes**

   * Apply `Depends(auth_dependency)` to routes that query or update the vector DB.
   * Test that unauthorized requests get HTTP 401.

3. **Refactor for clean modular design**

   * Create `auth.py` module under `core/` or `utils/`.
   * Keep token verification logic isolated.

4. **Optional:** Add pytest for one auth-protected endpoint.

### Output

* Updated FastAPI project with working JWT/API key auth.
* One test verifying endpoint access control.
* Note in your journal how this fits with the scaling ADR (monolith vs microservice).

Reference: this aligns with Week 4 backend objective in the Month 1 plan and cadence schedule for Day 2 backend work.
