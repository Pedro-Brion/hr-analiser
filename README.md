# hr-analyzer

> **Work in progress.** Only part of the API exists so far, and anything here may change.

An API that receives a resume (PDF), extracts the candidate's data, and returns the total years of experience and a 0–5 score for each technology.

## How it works

The AI only extracts **facts**: name, email, birth date, and each job with its start date, end date and technologies. All calculations are deterministic, tested code:

1. Technology names are normalized with an alias map (`ReactJS` → `React`, `Node` → `Node.js`).
2. For each technology, overlapping date ranges are merged, so two simultaneous jobs using React don't count twice. The merged ranges are then summed. A job with no end date runs until today.
3. The score depends on years of experience:

   | Experience                       | Score |
   | -------------------------------- | ----- |
   | Mentioned, but no dated usage    | 0     |
   | Under 1 year                     | 1     |
   | 1–2 years                        | 2     |
   | 2–4 years                        | 3     |
   | 4–6 years                        | 4     |
   | 6+ years                         | 5     |

   The score drops by 1 (minimum 1) if the technology wasn't used in the last 3 years.

Target output:

```json
{
  "name": "string",
  "age": 0,
  "email": "string",
  "stack": [
    { "name": "string", "experienceYears": 0.0, "score": 0 }
  ]
}
```

`age` is `null` unless the resume contains a birth date. It is never guessed.

## Status

| Area                                                | State   |
| --------------------------------------------------- | ------- |
| Data models (`Resume`, `Candidate`, `Experience`, `StackItem`) and admin | Done    |
| `GET /api/health/`                                  | Done    |
| `GET /api/resumes/{id}/` (status and error message) | Done    |
| `POST /api/resumes/` (PDF upload and validation)    | Planned |
| PDF text extraction                                 | Planned |
| AI extraction agent                                 | Planned |
| Experience merging, alias normalization and scoring | Planned |
| Background processing (`PENDING` → `PROCESSING` → `DONE` / `FAILED`) | Planned |
| Tests                                               | Planned |

## Tech stack

- Python 3.12+
- Django 6.1 and Django REST Framework
- SQLite for now, with PostgreSQL planned

Planned: Celery and Redis, pdfplumber, PydanticAI, pytest-django.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then try `http://localhost:8000/api/health/`.

To use the admin, create a user with `python manage.py createsuperuser` and open `/admin/`.

## Project layout

```
config/    Django project settings and root URLs
resumes/   Main app: models, serializers, views, admin
```
