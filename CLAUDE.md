# hr-analyzer: project context

## Who I am
Full stack dev (5+ years), strong in JS/TS (Vue, React, Angular, Node) and Laravel. I'm rusty in Python and using this project to get back into Python/Django, preparing for jobs that use Django. Explain Python/Django concepts with Laravel or Node analogies when helpful.

## How I want you to help
- I'm writing the code myself to practice. Guide me step by step, review what I write, point out mistakes and Pythonic improvements.
- Write full code only when I ask. Small snippets to illustrate a concept are fine.
- Keep explanations short. Before starting, inspect the repo to see where I am.
- Suggest a commit at the end of each step.

## Environment
- Django 6.1 (requires Python 3.12+)
- pip + venv in `.venv/` at the project root (gitignored), dependencies pinned with `pip freeze > requirements.txt`. Not using uv for now.
- Project created with `django-admin startproject config .` (settings package is `config`), main app is `resumes`.
- SQLite to start; move to PostgreSQL (Docker) later.

## What the project does
An API that receives a resume PDF, extracts the candidate's data, and returns, for each technology, total years of experience and a score from 0 to 5.

Output contract:
```json
{
  "name": "string",
  "age": 0,
  "email": "string (validated)",
  "stack": [
    { "name": "string", "experienceYears": 0.0, "score": 0 }
  ]
}
```
- `score`: integer, 0 to 5 inclusive.
- `age`: optional (null). Computed from birth date only if the resume has one; never guessed.
- `experienceYears`: one decimal place.
- Output in camelCase.

## Core design decision
The AI only extracts FACTS (name, email, birth date, and each job with start date, end date and technologies). All math is deterministic, tested code:
1. Normalize tech names with an alias map ("ReactJS" → "React", "Node" → "Node.js").
2. For each tech, merge overlapping date intervals (two simultaneous jobs using React don't count twice), then sum the years. A job with no end date runs until today.
3. Score by years: tech mentioned with no dated experience = 0, <1 = 1, 1–2 = 2, 2–4 = 3, 4–6 = 4, 6+ = 5. Minus 1 if not used in the last 3 years (minimum 1).

## Target stack
Django, Django REST Framework, Celery + Redis, PostgreSQL, pdfplumber, PydanticAI (Pydantic models as the structured output of the extraction agent), pytest-django.

## Models (planned)
- `Resume`: file, status (PENDING / PROCESSING / DONE / FAILED), error message, created_at
- `Candidate`: name, email, birth_date (nullable), FK to Resume
- `Experience`: company, role, start, end (nullable = current), technologies, FK to Resume (kept so every number is auditable)
- `StackItem`: name, experience_years, score (validators 0–5), FK to Resume

## Plan: following the official Django tutorial, adapted to this project
I'm following https://docs.djangoproject.com/en/6.1/intro/ part by part. Map each part to this project instead of the polls app:

1. **Part 1 (requests and responses):** `config` project + `resumes` app, a first view (e.g. `/api/health/`), app URLconf included under `api/`.
2. **Part 2 (models, database, admin):** the four models above, migrations, register them in the admin, play with them in `manage.py shell`.
3. **Part 3 (views and templates):** skip templates. Return JSON, first with `JsonResponse`, then install DRF and use serializers.
4. **Part 4 (forms and generic views):** upload endpoint `POST /api/resumes/` (multipart; validate extension, size limit and `%PDF` magic bytes; respond 202 with the id) and `GET /api/resumes/{id}/` (status + result). Use DRF generic views / ViewSets.
5. **Part 5 (testing):** unit tests for interval merging, alias normalization and each score band; API tests (non-PDF → 400, valid → 202, unknown id → 404).
6. **Part 6 (static files):** skip, or a minimal upload page later.
7. **Part 7 (customizing the admin):** Resume admin with Experience and StackItem inlines, status in `list_display`, filters.
8. **Part 8 (third-party packages):** after the tutorial, add the pipeline:
   - PDF → text with pdfplumber (empty text = scanned PDF → FAILED with a clear message)
   - Extraction agent with PydanticAI, built first as a FAKE function returning a fixed result so the rest works without the AI. Check the current PydanticAI docs for exact API names.
   - Celery task orchestrating it: PENDING → PROCESSING → DONE/FAILED, retry with backoff only for AI errors, idempotent, saved inside `transaction.atomic`.

## Bonus (later)
LGPD care (delete the PDF after processing, don't log resume text, endpoint to delete a resume and its data), Swagger with drf-spectacular, `GET /api/candidates/?tech=React&min_score=3`, Postgres + Redis via docker-compose, README.
