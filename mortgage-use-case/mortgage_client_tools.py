"""
Client-side tool wrappers for the Mortgage API.

These use @client_tool so the Agent SDK executes them locally,
bypassing the need for the Llama Stack server to reach the MCP server.
"""

import os
import json
import httpx
from typing import Optional
from llama_stack_client.lib.agents.client_tool import client_tool, ClientTool

BASE_URL = os.getenv("MORTGAGE_API_BASE_URL", "http://localhost:8083")
_http = httpx.Client(base_url=BASE_URL, timeout=30.0)


def _patch_duplicate_json_args():
    """Some model/server combos duplicate the JSON arguments string.
    Patch ClientTool.run to handle this gracefully."""
    _original_run = ClientTool.run

    def _patched_run(self, message_history):
        last = message_history[-1]
        for tc in last.tool_calls:
            if isinstance(tc.arguments, str):
                try:
                    json.loads(tc.arguments)
                except json.JSONDecodeError:
                    decoder = json.JSONDecoder()
                    try:
                        _, idx = decoder.raw_decode(tc.arguments)
                        tc.arguments = tc.arguments[:idx]
                    except json.JSONDecodeError:
                        pass
        return _original_run(self, message_history)

    ClientTool.run = _patched_run


_patch_duplicate_json_args()


def _handle(resp: httpx.Response):
    resp.raise_for_status()
    if resp.content:
        data = resp.json()
        return {"results": data} if isinstance(data, list) else data
    return {"status": "success", "status_code": resp.status_code}


@client_tool
def get_mortgage_application(application_id: int):
    """Get a mortgage application by its ID including loan type, status, credit score, income, and DTI ratio.

    :param application_id: the numeric ID of the mortgage application
    """
    return _handle(_http.get(f"/api/mortgage/applications/{application_id}"))


@client_tool
def search_applications_by_customer(customer_id: str):
    """Find all mortgage applications for a given customer.

    :param customer_id: the unique customer identifier such as AROUT or LONEP
    """
    return _handle(_http.get("/api/mortgage/applications", params={"customerId": customer_id}))


@client_tool
def get_application_conditions(application_id: int):
    """List all conditions for a mortgage application that must be satisfied before loan approval.

    :param application_id: the numeric ID of the mortgage application
    """
    return _handle(_http.get(f"/api/mortgage/applications/{application_id}/conditions"))


@client_tool
def get_application_documents(application_id: int):
    """List all documents for a mortgage application with their statuses and metadata.

    :param application_id: the numeric ID of the mortgage application
    """
    return _handle(_http.get(f"/api/mortgage/applications/{application_id}/documents"))


@client_tool
def review_document(document_id: int, status: str, rejection_reason: Optional[str] = None):
    """Accept or reject a mortgage document after reviewing it against policy criteria.

    :param document_id: the numeric ID of the document to review
    :param status: new status, must be ACCEPTED or REJECTED
    :param rejection_reason: required if rejecting, explains why the document was rejected
    """
    payload = {"status": status}
    if rejection_reason:
        payload["rejectionReason"] = rejection_reason
    return _handle(_http.post(f"/api/mortgage/documents/{document_id}/review", json=payload))


@client_tool
def update_condition_status(condition_id: int, status: str, resolution_notes: Optional[str] = None):
    """Update the status of a mortgage condition to SATISFIED, WAIVED, or PENDING_REVIEW.

    :param condition_id: the numeric ID of the condition
    :param status: new status, must be SATISFIED, WAIVED, or PENDING_REVIEW
    :param resolution_notes: optional notes explaining the resolution
    """
    payload = {"status": status}
    if resolution_notes:
        payload["resolutionNotes"] = resolution_notes
    return _handle(_http.put(f"/api/mortgage/conditions/{condition_id}", json=payload))


@client_tool
def get_credit_report(customer_id: str):
    """Retrieve credit reports for a customer with scores from multiple bureaus.

    :param customer_id: the unique customer identifier such as AROUT
    """
    return _handle(_http.get("/api/mortgage/credit-reports", params={"customerId": customer_id}))


@client_tool
def send_notification(customer_id: str, message: str, channel: Optional[str] = None):
    """Send a notification to a borrower about missing documents, rejected submissions, or required actions.

    :param customer_id: the unique customer identifier
    :param message: the notification message to send
    :param channel: delivery channel, either email, sms, or both, defaults to email
    """
    return _handle(_http.post("/api/mortgage/notifications", json={
        "customerId": customer_id,
        "message": message,
        "channel": channel or "email",
    }))


ALL_TOOLS = [
    get_mortgage_application,
    search_applications_by_customer,
    get_application_conditions,
    get_application_documents,
    review_document,
    update_condition_status,
    get_credit_report,
    send_notification,
]
