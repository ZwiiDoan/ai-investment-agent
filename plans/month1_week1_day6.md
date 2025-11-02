**month1_week1_day6.md**

---

# Month 1 — Week 1 — Day 6

**Focus: Frontend Literacy (Next.js Basics)**

## Objective

Create a minimal Next.js page and connect it to the FastAPI backend to confirm frontend-backend communication.

---

## Tasks

1. **Initialize Next.js project**

   * Run `npx create-next-app@latest ai-investment-agent-ui`
   * Enable TypeScript when prompted.
   * Start the dev server:

     ```bash
     cd ai-investment-agent-ui
     npm run dev
     ```

2. **Create simple page and layout**

   * Add `pages/index.tsx` that renders:

     ```tsx
     export default function Home() {
       return (
         <main className="p-6">
           <h1 className="text-2xl font-bold">AI Investment Agent</h1>
           <p className="mt-2 text-gray-600">Frontend connected successfully.</p>
         </main>
       )
     }
     ```

3. **Test API connectivity**

   * Create `/pages/api/test.ts`:

     ```ts
     export default async function handler(req, res) {
       const response = await fetch('http://localhost:8000/health');
       const data = await response.json();
       res.status(200).json(data);
     }
     ```

   * Ensure `http://localhost:8000/health` endpoint exists in FastAPI backend.

4. **Add minimal styling**

   * Install Tailwind CSS:

     ```bash
     npm install -D tailwindcss postcss autoprefixer
     npx tailwindcss init -p
     ```

   * Update `tailwind.config.js` and import CSS in `_app.tsx`.

---


## Learning Notes

- Gained hands-on experience with Next.js App Router, React components, and Tailwind CSS for rapid UI development.
- Learned to connect a Next.js frontend to a FastAPI backend, including live health polling and error handling.
- Understood the importance of CORS and how to configure FastAPI CORSMiddleware for secure frontend-backend communication.
- Explored best practices for API route proxying in Next.js to simplify frontend code and improve security.
- Practiced environment-based configuration (e.g., CORS origins) for production readiness.
- Used TypeScript interfaces to ensure type safety in React components.
- Documented architectural decisions and technical rationale using ADRs for maintainability.
- Compared client-side polling, SSR, and API proxying patterns for backend connectivity.
- Validated end-to-end integration: Next.js frontend → FastAPI backend → (future) LLM.

---

## Output

* “Hello World” page with working backend connectivity.
* Confirmed local end-to-end setup: **Next.js → FastAPI → LLM (placeholder)**.

---

## Reference

Based on **Week 1 frontend literacy plan** from the Month 1 roadmap.
