# Use a slim Python base image for smaller image size
FROM python:3.12-slim-bookworm

ENV USER=book-order \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash $USER

# Copy the uv binary from its official image
# Pinning to a specific version (e.g., 0.8.14) is recommended for reproducibility
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV APP_DIR=/home/$USER
WORKDIR $APP_DIR
# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install project dependencies using uv sync
# This command ensures your environment is up-to-date with uv.lock
RUN uv sync --locked

# Expose the port your application listens on (if applicable, e.g., for a web app)
EXPOSE 8000

# Command to run your application
# Replace 'your_module:app' with the actual entry point of your application
CMD ["uv", "run", "uvicorn", "book-order:src", "--host", "0.0.0.0", "--port", "8000"]