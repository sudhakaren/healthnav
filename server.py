"""
FastMCP Server with get_patient tool
This server provides patient information retrieval functionality via HTTP
Includes API Key authentication for security
"""

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from typing import Dict, Any, Optional
import uvicorn
import os
import secrets

# Initialize FastAPI app
app = FastAPI(title="Patient Information Server")

# API Key configuration
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify API key from request header
    """
    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API Key is missing. Include X-API-Key header."
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key


# Sample patient data (in production, this would come from a database)
PATIENT_DATA = {
    "contactId": "7c50f84d-62af-f011-bbd3-000d3a9b6dcb",
    "accountId": "a1d502bb-59af-f011-bbd3-6045bdda3fa7",
    "firstName": "Jackson",
    "middleName": None,
    "lastName": "Thomas",
    "fullName": "Jackson Thomas",
    "last4Soc": "1973",
    "memberId": None,
    "relationshipType": "Primary",
    "dob": "1995-10-29T00:00:00",
    "age": 30,
    "email": "jackson.thomas@yahoo.com",
    "emailAddress2": "jackson.thomas@yahoo.com",
    "emailAddress3": "jackson.thomas@yahoo.com",
    "phone": "(858) 327-4753",
    "preferredContactMethod": "Any",
    "personalPhoneTimezone": "35",
    "workPhoneTimezone": None,
    "nickName": None,
    "employeeId": "eb3ee149-5faf-f011-bbd3-000d3a9b6dcb",
    "employee": {
        "dentalPlan": {
            "cphsPlanName": "Buy Up Dental Plan",
            "id": 1039,
            "censusName": "17001 Met Buy-up Dntl",
            "planName": "a1d502bb-59af-f011-bbd3-6045bdda3fa7D1039",
            "subnetworkId": 2414,
            "specialPlanConsiderations": None
        },
        "medicalPlan": {
            "id": 10412,
            "censusName": "BCBS HDHP 1",
            "planName": "BCBS HDHP 1 Medical Plan",
            "subnetworkId": 2517,
            "specialPlanConsiderations": None
        },
        "visionPlan": {
            "cphsPlanName": "Buy Up Vision Plan",
            "id": 1027,
            "censusName": "EyeMed Buy-up Vision",
            "planName": "a1d502bb-59af-f011-bbd3-6045bdda3fa7V1027",
            "subnetworkId": 435,
            "specialPlanConsiderations": None
        }
    }
}


@app.get("/")
async def root():
    """Root endpoint - No authentication required"""
    return {
        "service": "Patient Information Server",
        "status": "running",
        "version": "1.0.0",
        "authentication": "API Key required (X-API-Key header)",
        "endpoints": {
            "health": "/health (no auth)",
            "get_patient": "/get_patient (requires auth)",
            "tools": "/tools (no auth)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint - No authentication required"""
    return {"status": "healthy"}


@app.get("/tools")
async def list_tools():
    """List available tools (MCP-compatible) - No authentication required"""
    return {
        "tools": [
            {
                "name": "get_patient",
                "description": "Retrieve patient information by contact ID",
                "authentication": "API Key required in X-API-Key header",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "contact_id": {
                            "type": "string",
                            "description": "The unique contact identifier for the patient"
                        }
                    }
                }
            }
        ]
    }


@app.get("/get_patient")
async def get_patient(
    contact_id: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve patient information by contact ID.
    Requires API Key authentication.
    
    Args:
        contact_id: The unique contact identifier for the patient. 
                   If not provided, returns default patient data.
        api_key: API Key for authentication (from X-API-Key header)
    
    Returns:
        Dictionary containing patient information including personal details,
        contact information, and insurance plan details.
    """
    # In production, you would query a database using the contact_id
    # For now, we return the sample data
    if contact_id and contact_id != PATIENT_DATA["contactId"]:
        return JSONResponse(
            status_code=404,
            content={
                "error": f"Patient with contact_id {contact_id} not found",
                "contactId": contact_id
            }
        )
    
    return {
        "content": [
            {
                "type": "text",
                "text": str(PATIENT_DATA)
            }
        ],
        "isError": False
    }


@app.post("/get_patient")
async def get_patient_post(
    request: Dict[str, Any],
    api_key: str = Depends(verify_api_key)
):
    """
    POST version of get_patient for MCP compatibility
    Requires API Key authentication.
    """
    contact_id = request.get("contact_id")
    return await get_patient(contact_id, api_key)


@app.get("/generate-api-key")
async def generate_api_key():
    """
    Generate a new API key (for development/testing only)
    In production, remove this endpoint or add admin authentication
    """
    new_key = secrets.token_urlsafe(32)
    return {
        "api_key": new_key,
        "note": "Save this key securely. Set it as API_KEY environment variable.",
        "usage": f"Include in requests as header: X-API-Key: {new_key}"
    }


if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8002"))
    
    # Print API key info on startup
    print(f"\n{'='*60}")
    print(f"Patient Information Server Starting")
    print(f"{'='*60}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"API Key: {API_KEY}")
    print(f"{'='*60}\n")
    
    if API_KEY == "your-secret-api-key-change-this":
        print("⚠️  WARNING: Using default API key!")
        print("   Set API_KEY environment variable for production")
        print(f"   Visit http://localhost:{port}/generate-api-key to generate a new key\n")
    
    # Run the server
    uvicorn.run(app, host=host, port=port)

# Made with Bob
