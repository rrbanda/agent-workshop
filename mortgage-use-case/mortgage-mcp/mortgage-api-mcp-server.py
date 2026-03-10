#!/usr/bin/env python3
"""
FastMCP server for NovaCrest Mortgage API
Provides tools to query and manage mortgage applications, documents, conditions, and credit reports.

Server Configuration:
    - Transport: streamable HTTP
    - Port: Configurable via PORT_FOR_MORTGAGE_MCP (default: 9003)
    - Host: Configurable via HOST_FOR_MORTGAGE_MCP (default: 0.0.0.0)

Environment Variables:
    MORTGAGE_API_BASE_URL: Base URL for the Mortgage API
    PORT_FOR_MORTGAGE_MCP: Port number for the MCP server (default: 9003)
    HOST_FOR_MORTGAGE_MCP: Host address to bind to (default: 0.0.0.0)
"""

from fastmcp import FastMCP
from dotenv import load_dotenv
import asyncio
import httpx
import os
import logging
from typing import Optional, Dict, Any

mcp = FastMCP("mortgage-api")

load_dotenv()

port = int(os.getenv("PORT_FOR_MORTGAGE_MCP", "9003"))
host = os.getenv("HOST_FOR_MORTGAGE_MCP", "0.0.0.0")
BASE_URL = os.getenv("MORTGAGE_API_BASE_URL", "http://localhost:8083")

http_client: Optional[httpx.AsyncClient] = None


async def get_http_client() -> httpx.AsyncClient:
    global http_client
    if http_client is None:
        http_client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)
    return http_client


async def handle_response(response: httpx.Response) -> Dict[str, Any]:
    try:
        response.raise_for_status()
        if response.content:
            data = response.json()
            if isinstance(data, list):
                return {"results": data}
            return data
        return {"status": "success", "status_code": response.status_code}
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_detail = e.response.json()
        except Exception:
            error_detail = e.response.text
        return {
            "error": f"HTTP {e.response.status_code}",
            "detail": error_detail,
            "status_code": e.response.status_code
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_mortgage_application(application_id: int) -> Dict[str, Any]:
    """
    Get a mortgage application by its ID.

    Retrieves full details of a mortgage application including loan type, status,
    credit score, income, and debt-to-income ratio.

    Args:
        application_id: The numeric ID of the mortgage application

    Returns:
        Mortgage application details including applicationNumber, customerId,
        propertyAddress, loanAmount, loanType, status, creditScore, annualIncome,
        debtToIncomeRatio, createdAt, updatedAt
    """
    client = await get_http_client()
    response = await client.get(f"/api/mortgage/applications/{application_id}")
    return await handle_response(response)


@mcp.tool()
async def search_applications_by_customer(customer_id: str) -> Dict[str, Any]:
    """
    Find all mortgage applications for a given customer.

    Args:
        customer_id: The unique customer identifier (e.g., "AROUT", "LONEP")

    Returns:
        List of mortgage applications for the customer with their details and statuses
    """
    client = await get_http_client()
    response = await client.get("/api/mortgage/applications", params={"customerId": customer_id})
    return await handle_response(response)


@mcp.tool()
async def get_application_conditions(application_id: int) -> Dict[str, Any]:
    """
    List all conditions for a mortgage application.

    Conditions are requirements that must be satisfied before the loan can be
    approved (e.g., missing documents, verification needs).

    Args:
        application_id: The numeric ID of the mortgage application

    Returns:
        List of conditions with conditionNumber, description, requiredDocumentType,
        status (OPEN, SATISFIED, WAIVED, PENDING_REVIEW), and resolutionNotes
    """
    client = await get_http_client()
    response = await client.get(f"/api/mortgage/applications/{application_id}/conditions")
    return await handle_response(response)


@mcp.tool()
async def get_application_documents(application_id: int) -> Dict[str, Any]:
    """
    List all documents for a mortgage application.

    Shows submitted, requested, accepted, and rejected documents with their
    metadata including dates and rejection reasons.

    Args:
        application_id: The numeric ID of the mortgage application

    Returns:
        List of documents with documentNumber, documentType, status (REQUESTED,
        UPLOADED, ACCEPTED, REJECTED), fileName, description, rejectionReason,
        documentDate, uploadedDate, reviewedDate
    """
    client = await get_http_client()
    response = await client.get(f"/api/mortgage/applications/{application_id}/documents")
    return await handle_response(response)


@mcp.tool()
async def review_document(
    document_id: int,
    status: str,
    rejection_reason: Optional[str] = None
) -> Dict[str, Any]:
    """
    Accept or reject a mortgage document.

    Reviews a submitted document and updates its status. If rejecting, provide
    a clear reason so the borrower knows what to fix.

    Args:
        document_id: The numeric ID of the document to review
        status: New status - must be "ACCEPTED" or "REJECTED"
        rejection_reason: Required if rejecting. Explain why the document was rejected
            (e.g., "Statement is older than 60 days")

    Returns:
        Confirmation with the updated document status
    """
    client = await get_http_client()
    payload = {"status": status}
    if rejection_reason:
        payload["rejectionReason"] = rejection_reason
    response = await client.post(f"/api/mortgage/documents/{document_id}/review", json=payload)
    return await handle_response(response)


@mcp.tool()
async def update_condition_status(
    condition_id: int,
    status: str,
    resolution_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update the status of a mortgage condition.

    Mark a condition as satisfied, waived, or pending review.

    Args:
        condition_id: The numeric ID of the condition
        status: New status - must be "SATISFIED", "WAIVED", or "PENDING_REVIEW"
        resolution_notes: Optional notes explaining the resolution

    Returns:
        Confirmation with the updated condition status
    """
    client = await get_http_client()
    payload = {"status": status}
    if resolution_notes:
        payload["resolutionNotes"] = resolution_notes
    response = await client.put(f"/api/mortgage/conditions/{condition_id}", json=payload)
    return await handle_response(response)


@mcp.tool()
async def get_credit_report(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve credit reports for a customer.

    Returns credit scores from multiple bureaus along with debt information
    used for underwriting decisions.

    Args:
        customer_id: The unique customer identifier (e.g., "AROUT")

    Returns:
        List of credit reports with creditScore, creditBureau, totalDebt,
        monthlyObligations, derogatoryMarks, totalAccounts, openAccounts, reportDate
    """
    client = await get_http_client()
    response = await client.get("/api/mortgage/credit-reports", params={"customerId": customer_id})
    return await handle_response(response)


@mcp.tool()
async def send_notification(
    customer_id: str,
    message: str,
    channel: Optional[str] = "email"
) -> Dict[str, Any]:
    """
    Send a notification to a borrower.

    Use this to inform borrowers about missing documents, rejected submissions,
    or other actions they need to take.

    Args:
        customer_id: The unique customer identifier
        message: The notification message to send
        channel: Delivery channel - "email", "sms", or "both" (default: "email")

    Returns:
        Confirmation that the notification was sent
    """
    client = await get_http_client()
    payload = {
        "customerId": customer_id,
        "message": message,
        "channel": channel or "email"
    }
    response = await client.post("/api/mortgage/notifications", json=payload)
    return await handle_response(response)


async def cleanup():
    global http_client
    if http_client:
        await http_client.aclose()
        http_client = None


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Mortgage MCP Server Configuration:")
    logger.info(f"  MORTGAGE_API_BASE_URL: {BASE_URL}")
    logger.info(f"  PORT_FOR_MORTGAGE_MCP: {port}")
    logger.info(f"  HOST_FOR_MORTGAGE_MCP: {host}")
    logger.info("=" * 60)

    try:
        mcp.run(transport="http", port=port, host=host)
    finally:
        asyncio.run(cleanup())
