# hello-cicd

Session 16 practice repo — CI/CD with GitHub Actions.

A small Python calculator app with tests, wired up to a GitHub Actions pipeline that
runs the tests on every push and then builds an artifact.

## What is in here

| Path | What it is |
|---|---|
| `app/calculator.py` | The application — add, subtract, multiply, divide |
| `tests/test_calculator.py` | 5 pytest tests, including divide-by-zero |
| `build.sh` | Build script — copies the app into `build/` and writes build info |
| `requirements.txt` | Dependencies (pytest) |
| `.github/workflows/` | The workflows (below) |

## Workflows

| Workflow | Trigger | What it does |
|---|---|---|
| `hello-actions.yml` | manual | Prints a message, the date, and the OS — the simplest possible workflow |
| `workflow-demo.yml` | manual | Four steps in one job, to show step order |
| `jobs-steps.yml` | manual | Two jobs running in parallel, to show jobs vs steps |
| `ci.yml` | push / PR to main, manual | The real pipeline: test job, then build job |

`ci.yml` is the one that matters. It has two jobs:

1. **test** — checks out the code, sets up Python 3.12, installs dependencies, runs `pytest -v`
2. **build** — `needs: test`, so it only runs if the tests pass. Runs `build.sh` and uploads
   `build/` as a downloadable artifact.

## Running it locally

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
bash build.sh
```

Expected test output:

```
tests/test_calculator.py::test_add PASSED                                [ 20%]
tests/test_calculator.py::test_subtract PASSED                           [ 40%]
tests/test_calculator.py::test_multiply PASSED                           [ 60%]
tests/test_calculator.py::test_divide PASSED                             [ 80%]
tests/test_calculator.py::test_divide_by_zero PASSED                     [100%]

============================== 5 passed ==============================
```

## Running it on GitHub

`ci.yml` runs automatically on every push to `main`. The other three are manual — open the
**Actions** tab, pick the workflow, and press **Run workflow** (that is what `workflow_dispatch`
means).
