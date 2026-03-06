# ==============================
# 1. Builder stage
# ==============================
FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# System dependencies để build packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade toolchain
RUN pip install --upgrade pip setuptools wheel

# Copy dependency trước để tận dụng docker cache
COPY src/backend/requirements.txt .

# Build wheels
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


# ==============================
# 2. Runtime stage
# ==============================
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Chỉ cài runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels từ builder
COPY --from=builder /build/wheels /wheels

# Install python packages
RUN pip install --no-cache-dir /wheels/*

# Copy source code
COPY src/backend/ocomme/ $APP_HOME

# Copy entrypoint
COPY infra/container/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Non-root user (security best practice)
RUN useradd -m django
USER django

# Port
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]