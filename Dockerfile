# Use official Python slim image (much lighter ~150MB vs ~1GB)
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRPC_POLL_STRATEGY=epoll \
    GRPC_VERBOSITY=INFO \
    ADK_WEB_HOST=0.0.0.0 \
    ADK_WEB_PORT=8080

# Set working directory
WORKDIR /app

# Install system dependencies needed for gRPC and protobuf
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    pkg-config \
    net-tools \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies (including your specified packages)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    grpcio==1.66.2 \
    grpcio-tools==1.66.2 \
    protobuf==5.29.5 \
    mypy-protobuf==3.6.0 \
    -r requirements.txt

# Copy protobuf definition for compilation
COPY demo.proto /app/

# Create proto output directory
RUN mkdir -p /app/green_next_shopping_agent/sub_agents/mcp_server

# Generate protobuf Python files
RUN python -m grpc_tools.protoc \
    --proto_path=. \
    --python_out=./green_next_shopping_agent/sub_agents/mcp_server \
    --grpc_python_out=./green_next_shopping_agent/sub_agents/mcp_server \
    --mypy_out=./green_next_shopping_agent/sub_agents/mcp_server \
    demo.proto

# Copy application code
COPY green_next_shopping_agent/ /app/green_next_shopping_agent/
COPY readme.md /app/

# Set up proper Python path
ENV PYTHONPATH="/app:$PYTHONPATH"

# Copy startup script and make it executable (BEFORE switching to non-root)
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check for Kubernetes - using netstat to check if port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD netstat -an | grep :8080 | grep LISTEN || exit 1

# Expose port for ADK web interface
EXPOSE 8080

# Use the startup script
CMD ["/app/start.sh"]