FROM python:3.13-slim

WORKDIR /app
COPY . /app
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser
CMD ["python", "run_security_checks.py", "--root", ".", "--report", "/tmp/security-report.json"]
