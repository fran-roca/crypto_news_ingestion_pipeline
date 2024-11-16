# Use the official Python slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY poetry.lock pyproject.toml ./

# Install dependencies (production only, excluding dev dependencies)
RUN poetry install --no-root --only main

# Copy all project files, preserving directory structure
COPY . .

# Set executable permissions for health check
RUN chmod +x /app/src/monitoring/health_check.py

# Health check command with the correct path
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD poetry run python /app/src/monitoring/health_check.py || exit 1

# Run the main application
CMD ["poetry", "run", "python", "-m", "main"]
