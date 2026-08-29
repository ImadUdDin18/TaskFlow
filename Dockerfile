# =========================================================
# TaskFlow — Multi-stage Dockerfile (Flask + SQLAlchemy + SQLite)
# =========================================================

# -------- Stage 1: Builder --------
# Compiles/downloads all Python dependencies into wheels.
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

# Build wheels for all dependencies (including gunicorn, added for production).
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt gunicorn==22.0.0


# -------- Stage 2: Runtime --------
# Clean, minimal image — no build tools, non-root user, explicit port/env.
FROM python:3.12-slim AS runtime

LABEL maintainer="Imad Ud Din" \
      description="TaskFlow production runtime image"

# Non-root user to run the app
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

WORKDIR /app

# Install Python packages from the pre-built wheels (no compiler needed here)
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt gunicorn==22.0.0 \
    && rm -rf /wheels requirements.txt

# Copy application code last, so dependency layers stay cached across builds
COPY --chown=appuser:appgroup . .

# The /app directory itself was created while still root (by WORKDIR),
# so even though the copied files above are chowned to appuser, appuser
# couldn't create *new* files (like app_errors.log, tasks.db) in it.
# Fix: give appuser ownership of the directory too.
RUN chown appuser:appgroup /app

# ---- Environment variables ----
# SECRET_KEY is left empty here on purpose — inject the real value at
# runtime (docker run -e / Compose env file), never bake it into the image.
# (Note: app.py currently hardcodes a default SECRET_KEY — worth updating
# it to read from os.environ.get('SECRET_KEY') so this actually takes effect.)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    PORT=5000 \
    SECRET_KEY=""

# SQLite database file (tasks.db) and app_errors.log are created inside
# /app at runtime. No VOLUME instruction here on purpose — Docker resets
# ownership on anonymous volumes, which breaks appuser's write permission.
# For persistence across restarts, bind-mount a host folder instead:
#   docker run -v %cd%/data:/app/data -p 8080:5000 taskflow:latest
# (and update app.py's DB path accordingly if you do this)

# ---- Port routing ----
# Container listens on 5000. Map to any host port at run time:
#   docker run -p 8080:5000 taskflow:latest
EXPOSE 5000

USER appuser

# Uses the app's own /health endpoint, which checks DB connectivity too.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Production WSGI server instead of Flask's built-in dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
