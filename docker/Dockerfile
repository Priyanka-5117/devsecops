FROM python:3.12-slim

WORKDIR /app

# ✅ Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# ✅ Create non-root user
RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app

# ✅ Switch to non-root user
USER appuser

EXPOSE 5000

# ✅ Fixed healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
