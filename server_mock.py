"""
server_mock.py  –  drop-in replacement for server.py during local dev/testing.
Returns hard-coded sample payloads so you can validate MCP tool wiring
without a live Horizon API.

Usage:
    MCP_TRANSPORT=sse python server_mock.py
  or (stdio for Claude Desktop):
    python server_mock.py
"""

import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="horizon-mcp-mock",
    description="Mock Horizon MCP server – returns sample data",
)

# ── Sample payloads (derived from spec) ──────────────────────────────────────

MEDICAL_PLAN_SAMPLE = {
    "result": {
        "autoId": 10412,
        "medicalPlanId": "a1d502bb-59af-f011-bbd3-6045bdda3fa7M10412",
        "accountId": "a1d502bb-59af-f011-bbd3-6045bdda3fa7",
        "medicalCphsPlanName": "BCBS HDHP 1 Medical Plan",
        "medicalErPlanName": None,
        "medicalComment": "",
        "payerSubnetworkKey": 2517,
        "insuranceName": "BCBS",
        "payerKey": 2,
        "insurancePlanType": "HDHP",
        "insuranceNetwork": "BCBS - BCBS BlueCard PPO",
        "insuranceContactNumber": "",
        "insurancePlanYearStart": "2026-01-01T00:00:00",
        "insurancePlanYearEnd": "2026-12-31T00:00:00",
        "planAdministratorKey": None,
        "tierStatusCode": None,
        "inNetworkCoInsurance": 0.25,
        "ppcVerified": True,
        "specialPlanConsiderations": None,
        "features": {"claims": None, "outOfPocketRepricing": None, "spendTrack": None},
        "hideSsmdCost": False,
        "active": False,
        "planFunding": "FullyInsured",
        "planDocument": "",
        "planMessages": [],
        "payer": {
            "payerKey": 2,
            "payerId": "001000",
            "payerName": "BCBS",
            "payerGroup": "001",
            "payerGroupDescription": "BCBS",
            "payerTradingPartnerServiceIdMapping": {
                "payerKey": 2,
                "tradingPartnerServiceId": "FLBCBS",
            },
        },
        "deductibleDetails": {
            "deductibleComment": "",
            "deductibleType": "Embedded",
            "inNetworkSingle": 3300.0,
            "inNetworkEEPlus": None,
            "inNetworkFamily": 6600.0,
        },
        "officeDetails": {
            "pcpOfficeVisitCoPay": None,
            "pcpOfficeVisitCoInsurance": 0.25,
            "pcpOfficeVisitBenefitOrder": 6,
            "specialistOfficeVisitCoPay": None,
            "specialistOfficeVisitCoInsurance": 0.25,
            "specialistOfficeVisitBenefitOrder": 6,
            "obgynIsPcp": False,
        },
        "outOfPocketDetails": {
            "oopmComment": "",
            "isDeductibleIncluded": True,
            "oopmNetworkSingle": 6100.0,
            "oopmNetworkEEPlus": None,
            "oopmNetworkFamily": 12200.0,
        },
        "physicianDetails": {
            "outpatientServicesCoPay": None,
            "outpatientServicesCoInsurance": 0.25,
            "outpatientServicesBenefitOrder": 6,
            "inpatientServicesCoPay": None,
            "inpatientServicesCoInsurance": 0.25,
            "inpatientServicesBenefitOrder": 6,
        },
        "emergencyCareDetails": {
            "separateErDeductible": False,
            "emergentCareDeductible": None,
            "erCoPay": None,
            "erCoInsurance": 0.25,
            "erBenefitOrder": 6,
            "urgentCareCoPay": None,
            "urgentCareCoInsurance": 0.25,
            "urgentCareBenefitOrder": 6,
            "ambulanceCoPay": None,
            "ambulanceCoInsurance": 0.25,
            "ambulanceBenefitOrder": 6,
        },
        "networks": [
            {
                "payerKey": 2,
                "payerId": "001000",
                "payerName": "BCBS",
                "subnetworkKey": 2517,
                "subnetworkDesc": "BCBS BlueCard PPO",
                "ppc": "5198",
                "priority": 1,
            }
        ],
        "censusNames": ["BCBS HDHP 1"],
    },
    "message": None,
}

PATIENT_SAMPLE = {
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
            "specialPlanConsiderations": None,
        },
        "medicalPlan": {
            "id": 10412,
            "censusName": "BCBS HDHP 1",
            "planName": "BCBS HDHP 1 Medical Plan",
            "subnetworkId": 2517,
            "specialPlanConsiderations": None,
        },
        "visionPlan": {
            "cphsPlanName": "Buy Up Vision Plan",
            "id": 1027,
            "censusName": "EyeMed Buy-up Vision",
            "planName": "a1d502bb-59af-f011-bbd3-6045bdda3fa7V1027",
            "subnetworkId": 435,
            "specialPlanConsiderations": None,
        },
    },
}


# ── Mock tools ────────────────────────────────────────────────────────────────

@mcp.tool()
async def get_medical_plan(
    account_id: str,
    medical_plan_id: str | None = None,
    auto_id: int | None = None,
) -> dict:
    """
    [MOCK] Retrieve a medical plan record.

    Args:
        account_id:      The account UUID.
        medical_plan_id: Full composite plan identifier (optional).
        auto_id:         Numeric plan key (optional).

    Returns:
        Sample medical plan payload (result + message).
    """
    return MEDICAL_PLAN_SAMPLE


@mcp.tool()
async def get_patient(
    contact_id: str,
    account_id: str | None = None,
) -> dict:
    """
    [MOCK] Retrieve a patient / contact record.

    Args:
        contact_id:  Patient contact UUID.
        account_id:  Account UUID (optional).

    Returns:
        Sample patient record with embedded plan summaries.
    """
    return PATIENT_SAMPLE


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    port      = int(os.getenv("MCP_PORT", "8000"))
    host      = os.getenv("MCP_HOST", "0.0.0.0")

    if transport == "sse":
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run(transport="stdio")
