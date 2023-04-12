@echo off
rem Run tests and generate coverage report (Windows)
pytest --cov-report html --cov=reddit_to_video tests/ -n auto
echo Linting...
ruff src/
