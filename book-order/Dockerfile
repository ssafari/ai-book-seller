# Use a slim Python base image for smaller image size
FROM python:3.13-slim-bookworm

ENV USER=book-order

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash $USER

# Copy the uv binary from its official image
# Pinning to a specific version (e.g., 0.8.14) is recommended for reproducibility
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_PROJECT_ENVIRONMENT=/app

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY uv.lock pyproject.toml /app/
COPY main.py /app
COPY src /app/src

RUN --mount=type=cache,target=/root/.cache \
    uv sync \
        --locked \
        --no-dev \
        --no-editable

# Expose the port your application listens on (if applicable, e.g., for a web app)
EXPOSE 8000

# Command to run your application
# Replace 'your_module:app' with the actual entry point of your application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]