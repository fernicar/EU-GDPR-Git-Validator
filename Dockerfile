# EU GDPR Git Validator Docker Image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="EU GDPR Git Validator Contributors"
LABEL description="A compliance testing tool that analyses Git repositories for GDPR violations"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd -r gdpruser && useradd -r -g gdpruser gdpruser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md LICENSE ./

# Install the package
RUN pip install -e .

# Create directories for reports and data
RUN mkdir -p /app/reports /app/data && \
    chown -R gdpruser:gdpruser /app

# Switch to non-root user
USER gdpruser

# Set default command
ENTRYPOINT ["gdpr-validator"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD gdpr-validator --version || exit 1

# Expose volume for mounting repositories
VOLUME ["/app/data"]

# Expose volume for output reports
VOLUME ["/app/reports"]
