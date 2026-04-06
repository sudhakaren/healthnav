# Horizon MCP Server

MCP server exposing **`get_medical_plan`** and **`get_patient`** tools for the Horizon healthcare platform.  
Designed for deployment on **horizon.prefect.io**.

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | Production server — calls live Horizon REST API |
| `server_mock.py` | Local dev/test — returns hard-coded sample payloads |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container for SSE-mode deployment |

---

## Local development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run in mock mode (stdio, no live API needed)
python server_mock.py

# 3. Or run the real server in SSE mode locally
HORIZON_BASE_URL=https://api.yourdomain.com \
HORIZON_API_KEY=your_key_here \
MCP_TRANSPORT=sse \
python server.py
```

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HORIZON_BASE_URL` | `https://horizon.prefect.io/api` | Base URL of the Horizon REST API |
| `HORIZON_API_KEY` | _(empty)_ | Bearer token / API key for auth |
| `MCP_TRANSPORT` | `stdio` | `stdio` for local, `sse` for HTTP hosting |
| `MCP_HOST` | `0.0.0.0` | Bind host (SSE mode only) |
| `MCP_PORT` | `8000` | Bind port (SSE mode only) |

---

## Docker deployment

```bash
docker build -t horizon-mcp .

docker run -p 8000:8000 \
  -e HORIZON_BASE_URL=https://api.yourdomain.com \
  -e HORIZON_API_KEY=your_key_here \
  horizon-mcp
```

The MCP SSE endpoint is available at:  
`http://localhost:8000/sse`

---

## Tools

### `get_medical_plan`

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `account_id` | `str` | ✅ | Account UUID |
| `medical_plan_id` | `str` | ⬜ | Full composite plan ID (e.g. `...M10412`) |
| `auto_id` | `int` | ⬜ | Numeric plan key (e.g. `10412`) |

Returns a full plan object with deductible, OOP, office visit, physician, facility, diagnostic, DME, emergency care, PT, mental health details, and network records.

---

### `get_patient`

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `contact_id` | `str` | ✅ | Patient contact UUID |
| `account_id` | `str` | ⬜ | Account UUID (recommended) |

Returns demographic data (name, DOB, email, phone) plus an embedded `employee` object with medical, dental, and vision plan summaries.

---

## Claude Desktop / Cursor config (`stdio` mode)

```json
{
  "mcpServers": {
    "horizon": {
      "command": "python",
      "args": ["/path/to/horizon_mcp/server.py"],
      "env": {
        "HORIZON_BASE_URL": "https://api.yourdomain.com",
        "HORIZON_API_KEY": "your_key_here"
      }
    }
  }
}
```

## Claude Desktop / Cursor config (`sse` mode — after Docker deploy)

```json
{
  "mcpServers": {
    "horizon": {
      "url": "http://horizon.prefect.io:8000/sse"
    }
  }
}
```
