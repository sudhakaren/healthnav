FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# SSE transport for HTTP-based hosting
ENV MCP_TRANSPORT=sse
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

# HORIZON_BASE_URL and HORIZON_API_KEY are injected at runtime
# e.g. via Prefect secrets / environment block

EXPOSE 8000

CMD ["python", "server.py"]
