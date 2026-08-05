# Flask CI Practice App

A tiny Flask app built specifically for practicing continuous integration with
GitHub Actions. It has just enough surface area (a few routes, some edge
cases, a test suite, and a linter) to make CI meaningful without being
overwhelming.

## Project structure

```
flask-ci-practice/
├── app.py                      # The Flask application
├── requirements.txt             # Runtime dependency (Flask)
├── requirements-dev.txt         # Test/lint dependencies (pytest, flake8, etc.)
├── .flake8                      # Linter config
├── .gitignore
├── tests/
│   └── test_app.py              # Pytest test suite
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions workflow
```

## Endpoints

| Method | Path                  | Description                          |
|--------|------------------------|---------------------------------------|
| GET    | `/`                    | Welcome message                       |
| GET    | `/health`              | Health check, returns `{"status":"ok"}` |
| GET    | `/api/greet/<name>`    | Returns a greeting; 400 if name is blank |
| POST   | `/api/calculate`       | Body: `{"operation": "add\|subtract\|multiply\|divide", "a": num, "b": num}` |

## Running locally

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt

# Run the app
python app.py                  # Visit http://127.0.0.1:5000

# Run the tests
pytest --cov=app --cov-report=term-missing

# Run the linter
flake8 .
```

## Setting up the CI practice

1. Create a new repo on GitHub (don't initialize it with a README).
2. From this folder, push it up:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Flask app with CI"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
3. Go to the **Actions** tab on GitHub. Pushing to `main` (or opening a PR
   against it) will automatically trigger the `CI` workflow defined in
   `.github/workflows/ci.yml`. It runs on Python 3.10, 3.11, and 3.12, and
   for each version it:
   - installs dependencies
   - lints the code with `flake8`
   - runs the test suite with `pytest` (with coverage)

## Things to try, to get a feel for CI

- **Break a test** (e.g., change `test_health` to expect the wrong status
  code) and push — watch the workflow go red.
- **Introduce a lint error** (e.g., an unused import, or a line over 100
  chars) and push — see the lint step fail before tests even run.
- **Open a pull request** instead of pushing to `main` directly — CI runs on
  PRs too, and you can require it to pass before merging (Settings →
  Branches → Branch protection rules).
- **Add a new endpoint and test** — extend `app.py` and `tests/test_app.py`,
  then push to see CI validate your addition.
- **Add a badge** to this README once you have a repo:
  ```markdown
  ![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)
  ```
