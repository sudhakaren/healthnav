# FastMCP Patient Information Server

A FastMCP server that provides patient information retrieval functionality through the `get_patient` tool.

## Features

- **get_patient** tool: Retrieves comprehensive patient information including:
  - Personal details (name, DOB, contact info)
  - Insurance plans (Medical, Dental, Vision)
  - Employee information

## Prerequisites

- Docker and Docker Compose installed on your Ubuntu server
- Network access to the server from Watson Orchestrate

## Installation & Deployment

### 1. Transfer Files to Ubuntu Server

Copy the entire `fastmcp-server` directory to your Ubuntu server:

```bash
scp -r fastmcp-server/ user@your-ubuntu-server:/path/to/deployment/
```

### 2. Build and Run with Docker Compose

SSH into your Ubuntu server and navigate to the directory:

```bash
ssh user@your-ubuntu-server
cd /path/to/deployment/fastmcp-server
```

Build and start the container:

```bash
docker-compose up -d --build
```

### 3. Verify the Server is Running

Check container status:

```bash
docker-compose ps
```

View logs:

```bash
docker-compose logs -f
```

### 4. Test the Server Locally

```bash
curl http://localhost:8002/health
```

## Connecting to Watson Orchestrate

### Step 1: Get Your Server URL

Your MCP server will be accessible at:
```
http://your-ubuntu-server-ip:8002
```

Or if you have a domain:
```
https://your-domain.com:8002
```

**Important**: For production, use HTTPS with proper SSL certificates.

### Step 2: Access Watson Orchestrate Tools Page

1. Log in to your Watson Orchestrate instance
2. Navigate to **Skills** or **Tools** section
3. Click on **Add Tool** or **Connect Tool**

### Step 3: Configure MCP Connection

1. **Connection Type**: Select "MCP Server" or "Custom API"

2. **Server URL**: Enter your server endpoint
   ```
   http://your-ubuntu-server-ip:8002
   ```

3. **Authentication** (if required):
   - Type: None (for basic setup)
   - For production, implement OAuth2 or API key authentication

4. **Connection Name**: `Patient Information MCP Server`

5. **Description**: `Provides patient information retrieval capabilities`

### Step 4: Discover Tools

1. Click **Discover Tools** or **Test Connection**
2. Watson Orchestrate will query the MCP server for available tools
3. You should see the `get_patient` tool appear

### Step 5: Configure the get_patient Tool

The tool will be automatically configured with:

- **Tool Name**: `get_patient`
- **Description**: Retrieve patient information by contact ID
- **Parameters**:
  - `contact_id` (optional string): The unique contact identifier

### Step 6: Test the Tool

1. In Watson Orchestrate, select the `get_patient` tool
2. Test with the sample contact ID: `7c50f84d-62af-f011-bbd3-000d3a9b6dcb`
3. Or test without parameters to get default patient data
4. Verify the response matches the expected format

### Step 7: Create Skills Using the Tool

1. Navigate to **Skills Builder** in Watson Orchestrate
2. Create a new skill that uses the `get_patient` tool
3. Configure the skill flow and parameters
4. Test and publish the skill

## Watson Orchestrate Connection YAML Example

If Watson Orchestrate supports YAML configuration, create a connection file:

```yaml
apiVersion: v1
kind: Connection
metadata:
  name: patient-mcp-server
spec:
  type: mcp
  endpoint: http://your-ubuntu-server-ip:8002
  authentication:
    type: none
  tools:
    - name: get_patient
      enabled: true
```

## Security Considerations for Production

### 1. Enable HTTPS

Use a reverse proxy (nginx) with SSL:

```bash
# Install nginx
sudo apt-get update
sudo apt-get install nginx certbot python3-certbot-nginx

# Configure SSL
sudo certbot --nginx -d your-domain.com
```

### 2. Add Authentication

Update `server.py` to include API key authentication:

```python
from fastapi import Header, HTTPException

@mcp.tool()
def get_patient(contact_id: str = None, api_key: str = Header(None)) -> Dict[str, Any]:
    if api_key != "your-secret-api-key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... rest of the function
```

### 3. Network Security

- Use firewall rules to restrict access
- Consider VPN or private network connection
- Implement rate limiting

### 4. Update docker-compose.yml for Production

```yaml
version: '3.8'

services:
  fastmcp-server:
    build: .
    container_name: patient-mcp-server
    ports:
      - "127.0.0.1:8002:8002"  # Only bind to localhost
    environment:
      - PYTHONUNBUFFERED=1
      - API_KEY=${API_KEY}  # Use environment variable
    restart: unless-stopped
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

## Troubleshooting

### Server Not Starting

```bash
# Check logs
docker-compose logs

# Rebuild container
docker-compose down
docker-compose up -d --build
```

### Connection Refused from Watson Orchestrate

1. Verify firewall allows port 8002
2. Check server is listening on 0.0.0.0, not 127.0.0.1
3. Test with curl from another machine

### Tool Not Appearing in Watson Orchestrate

1. Verify MCP server is responding to tool discovery requests
2. Check Watson Orchestrate logs for connection errors
3. Ensure the server URL is correct and accessible

## Management Commands

```bash
# Start the server
docker-compose up -d

# Stop the server
docker-compose down

# View logs
docker-compose logs -f

# Restart the server
docker-compose restart

# Update the server
git pull  # or copy new files
docker-compose up -d --build
```

## Extending the Server

To add more tools, edit `server.py`:

```python
@mcp.tool()
def get_patient_appointments(patient_id: str) -> Dict[str, Any]:
    """Get patient appointments"""
    # Implementation here
    pass

@mcp.tool()
def get_patient_claims(patient_id: str) -> Dict[str, Any]:
    """Get patient insurance claims"""
    # Implementation here
    pass
```

Then rebuild and restart:

```bash
docker-compose up -d --build
```

## Support

For issues or questions:
- Check the logs: `docker-compose logs`
- Review FastMCP documentation: https://github.com/jlowin/fastmcp
- Review Watson Orchestrate MCP integration docs

## License

[Your License Here]