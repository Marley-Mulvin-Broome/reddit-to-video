# Run tests and generate coverage report
# Usage: test.ps1
# Requires: pytest, pytest-cov, pytest-xdist, ruff

Write-Host "Running tests..."
pytest --cov-report html --cov=reddit_to_video tests/ -n auto
Write-Host "Linting..."
ruff src/
Write-Host "Done linting."
Write-Host "Opening coverage report..."
Invoke-Item .\htmlcov\index.html
Write-Host "Done."