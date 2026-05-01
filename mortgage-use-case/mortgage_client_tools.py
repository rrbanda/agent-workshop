"""
Client-side tool wrappers for the Mortgage API.

These use @client_tool so the Agent SDK executes them locally,
bypassing the need for the Llama Stack server to reach the MCP server.

Also provides ChatCompletionAgent -- a drop-in Agent replacement that
routes through /v1/chat/completions instead of /v1/responses.  This
avoids a server-side bug where the Responses-API-to-Gemini conversion
keeps a stray ``type`` field inside ``tools[i].function``.
"""

import os
import json
import httpx
from typing import Optional, List, Dict, Any, Iterator
from uuid import uuid4
from llama_stack_client.lib.agents.client_tool import client_tool, ClientTool
from llama_stack_client.lib.agents.turn_events import (
    AgentStreamChunk,
    TurnStarted,
    TurnCompleted,
    TurnFailed,
    StepStarted,
    StepProgress,
    StepCompleted,
    TextDelta,
    ToolCallIssuedDelta,
    InferenceStepResult,
    ToolExecutionStepResult,
)
from llama_stack_client.lib.agents.types import ToolCall

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


class ChatCompletionAgent:
    """Agent that uses /v1/chat/completions for tool-calling.

    Drop-in replacement for ``Agent`` that works around a Llama Stack
    Responses-API bug where client-tool definitions include a ``type``
    field that Gemini rejects.  The Chat Completions endpoint does the
    conversion correctly.

    ``file_search`` tools are transparently converted to a function tool
    that queries the vector store via the Llama Stack API.
    """

    def __init__(self, client, *, model: str, instructions: str,
                 tools: Optional[List] = None, **kwargs):
        self.client = client
        self._model = model
        self._instructions = instructions
        self._sessions: Dict[str, List[Dict[str, Any]]] = {}

        self._cc_tools: List[Dict[str, Any]] = []
        self._tool_impls: Dict[str, ClientTool] = {}
        self._vector_store_ids: List[str] = []

        for tool in (tools or []):
            if isinstance(tool, ClientTool):
                schema = tool.get_input_schema()
                self._cc_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.get_name(),
                        "description": tool.get_description(),
                        "parameters": schema,
                    },
                })
                self._tool_impls[tool.get_name()] = tool
            elif isinstance(tool, dict):
                if tool.get("type") == "file_search":
                    self._vector_store_ids = tool.get("vector_store_ids", [])
                    self._cc_tools.append({
                        "type": "function",
                        "function": {
                            "name": "file_search",
                            "description": (
                                "Search the lending policy knowledge base. "
                                "Returns relevant passages from ACME's mortgage "
                                "lending policy documents."
                            ),
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "The search query",
                                    }
                                },
                                "required": ["query"],
                            },
                        },
                    })

    def create_session(self, session_name: str) -> str:
        sid = f"cc_session_{uuid4().hex[:12]}"
        self._sessions[sid] = []
        return sid

    def _exec_file_search(self, query: str) -> str:
        results = []
        for vs_id in self._vector_store_ids:
            resp = self.client.vector_stores.search(
                vector_store_id=vs_id,
                query=query,
            )
            items = resp.data if hasattr(resp, "data") else resp
            for item in items:
                if hasattr(item, "content"):
                    for c in (item.content if isinstance(item.content, list) else [item.content]):
                        text = c.text if hasattr(c, "text") else str(c)
                        results.append(text)
                else:
                    results.append(str(item))
        return "\n---\n".join(results[:5]) if results else "No relevant documents found."

    def _exec_tool(self, name: str, arguments: str) -> str:
        if name == "file_search":
            params = json.loads(arguments)
            return self._exec_file_search(params.get("query", ""))
        tool = self._tool_impls.get(name)
        if not tool:
            return f"Unknown tool: {name}"
        try:
            params = json.loads(arguments)
            result = tool.run_impl(**params)
            return json.dumps(result, ensure_ascii=False) if not isinstance(result, str) else result
        except Exception as e:
            return f"Error: {e}"

    def create_turn(self, messages: List[Dict[str, Any]],
                    session_id: str, stream: bool = True,
                    **kwargs):
        if stream:
            return self._run_turn(messages, session_id)
        return self._run_turn_sync(messages, session_id)

    def _run_turn_sync(self, new_messages, session_id):
        """Non-streaming: consume the generator and return a response object."""
        final_text = ""
        for chunk in self._run_turn(new_messages, session_id):
            evt = chunk.event
            if isinstance(evt, StepProgress) and isinstance(evt.delta, TextDelta):
                final_text += evt.delta.text

        class _Content:
            def __init__(self, text):
                self.text = text

        class _OutputItem:
            def __init__(self, text):
                self.content = [_Content(text)]

        class _Response:
            def __init__(self, text):
                self.output = [_OutputItem(text)]

        return _Response(final_text)

    def _run_turn(self, new_messages, session_id) -> Iterator[AgentStreamChunk]:
        turn_id = f"turn_{uuid4().hex[:12]}"
        step_counter = 0
        history = self._sessions.get(session_id, [])

        msgs = [{"role": "system", "content": self._instructions}]
        msgs.extend(history)
        msgs.extend(new_messages)

        yield AgentStreamChunk(event=TurnStarted(turn_id=turn_id, session_id=session_id))

        max_iterations = 10
        for _ in range(max_iterations):
            step_id = f"{turn_id}_step_{step_counter}"
            step_counter += 1
            yield AgentStreamChunk(event=StepStarted(
                step_id=step_id, step_type="inference", turn_id=turn_id))

            try:
                resp = self.client.chat.completions.create(
                    model=self._model,
                    messages=msgs,
                    tools=self._cc_tools or None,
                )
            except Exception as e:
                yield AgentStreamChunk(event=TurnFailed(
                    turn_id=turn_id, session_id=session_id,
                    error_message=str(e)))
                return

            choice = resp.choices[0]
            msg = choice.message

            if msg.tool_calls:
                tool_calls = []
                for tc in msg.tool_calls:
                    tc_obj = ToolCall(call_id=tc.id, tool_name=tc.function.name,
                                     arguments=tc.function.arguments)
                    tool_calls.append(tc_obj)
                    yield AgentStreamChunk(event=StepProgress(
                        step_id=step_id, step_type="inference", turn_id=turn_id,
                        delta=ToolCallIssuedDelta(
                            call_id=tc.id, tool_type="function",
                            tool_name=tc.function.name,
                            arguments=tc.function.arguments)))

                yield AgentStreamChunk(event=StepCompleted(
                    step_id=step_id, step_type="inference", turn_id=turn_id,
                    result=InferenceStepResult(
                        step_id=step_id, response_id=resp.id or "",
                        text_content="", function_calls=tool_calls,
                        server_tool_executions=[], stop_reason="tool_calls")))

                tool_step_id = f"{turn_id}_step_{step_counter}"
                step_counter += 1
                yield AgentStreamChunk(event=StepStarted(
                    step_id=tool_step_id, step_type="tool_execution",
                    turn_id=turn_id, metadata={"server_side": False}))

                assistant_msg: Dict[str, Any] = {"role": "assistant", "content": msg.content}
                assistant_msg["tool_calls"] = [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name,
                                  "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ]
                msgs.append(assistant_msg)

                tool_responses = []
                for tc in msg.tool_calls:
                    content = self._exec_tool(tc.function.name, tc.function.arguments)
                    tool_responses.append({
                        "call_id": tc.id,
                        "tool_name": tc.function.name,
                        "content": content,
                    })
                    msgs.append({"role": "tool", "tool_call_id": tc.id, "content": content})

                yield AgentStreamChunk(event=StepCompleted(
                    step_id=tool_step_id, step_type="tool_execution",
                    turn_id=turn_id,
                    result=ToolExecutionStepResult(
                        step_id=tool_step_id,
                        tool_calls=tool_calls,
                        tool_responses=tool_responses)))
                continue

            text = msg.content or ""
            yield AgentStreamChunk(event=StepProgress(
                step_id=step_id, step_type="inference", turn_id=turn_id,
                delta=TextDelta(text=text)))
            yield AgentStreamChunk(event=StepCompleted(
                step_id=step_id, step_type="inference", turn_id=turn_id,
                result=InferenceStepResult(
                    step_id=step_id, response_id=resp.id or "",
                    text_content=text, function_calls=[],
                    server_tool_executions=[], stop_reason="end_of_turn")))

            new_history = msgs[1:]
            new_history.append({"role": "assistant", "content": text})
            self._sessions[session_id] = new_history

            yield AgentStreamChunk(event=TurnCompleted(
                turn_id=turn_id, session_id=session_id,
                final_text=text, response_ids=[resp.id or ""],
                num_steps=step_counter))
            return


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
