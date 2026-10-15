FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN python -m tada ingest fixtures/synthetic.json
# The explorer binds loopback. Use the CLI inside a container; local Python is recommended for the UI.
ENTRYPOINT ["python", "-m", "tada"]
CMD ["export", "--output", "/tmp/normalized.json"]
