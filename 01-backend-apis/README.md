# Module 01: Backend APIs

## Learning Objectives

- Understand the ACME domain model (Customer and Finance)
- Build and deploy the Spring Boot REST APIs to OpenShift
- Explore the API endpoints via Swagger UI

> [!TIP]
> **Capstone Preview:** In the capstone, you will work with a Mortgage API that follows this same Spring Boot pattern -- same entity/repository/controller structure, same Swagger UI, same seed data approach.

## Prerequisites

- [Module 00: Environment Setup](../00-setup/) completed
- Access to an OpenShift cluster (logged in via `oc`)

## Concepts

Agents need **tools** to interact with the real world. In this workshop, the tools are REST APIs that manage ACME's customer and financial data. Before building agents, you need to understand what data and operations are available.

## ACME Domain Model

### Customer API (port 8081)

A single `Customer` entity with fields: customerId (5-char), companyName, contactName, contactTitle, address, city, region, postalCode, country, phone, fax, contactEmail.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Search customers (query params: companyName, contactName, contactEmail, phone) |
| GET | `/api/customers/{id}` | Get customer by ID |
| POST | `/api/customers` | Create customer |
| PUT | `/api/customers/{id}` | Update customer |
| DELETE | `/api/customers/{id}` | Delete customer |

### Finance API (port 8082)

Four entities: Order, Invoice, Dispute, Receipt -- all linked by customerId.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/finance/orders/history` | Order history for a customer |
| POST | `/api/finance/invoices/history` | Invoice history for a customer |
| POST | `/api/finance/disputes/duplicate-charge` | Start duplicate charge dispute |
| POST | `/api/finance/receipts/find-lost` | Find lost receipt |

## Step-by-Step

> [!NOTE]
> **Working directory:** All commands in this module run from the **repo root** (`agent-workshop/`).

Since Llama Stack runs on RHOAI, the backend APIs must also be deployed on OpenShift so MCP servers can reach them.

### 1. Build the Customer API

```bash
oc new-build --binary --strategy=docker --name=customer-api
cp 01-backend-apis/customer-api/deployment/Dockerfile 01-backend-apis/customer-api/Dockerfile
oc start-build customer-api --from-dir=01-backend-apis/customer-api/ --follow
rm 01-backend-apis/customer-api/Dockerfile
```

### 2. Build the Finance API

```bash
oc new-build --binary --strategy=docker --name=finance-api
cp 01-backend-apis/finance-api/deployment/Dockerfile 01-backend-apis/finance-api/Dockerfile
oc start-build finance-api --from-dir=01-backend-apis/finance-api/ --follow
rm 01-backend-apis/finance-api/Dockerfile
```

### 3. Deploy to OpenShift

```bash
oc apply -f 00-setup/admin/k8s/apis.yaml
```

This creates Deployments, Services, PostgreSQL instances, and Routes for both APIs. The databases are auto-populated with seed data on startup.

### 4. Get the Route URLs

```bash
echo "CUSTOMER_API_BASE_URL=https://$(oc get route acme-customer-service -o jsonpath='{.spec.host}')"
echo "FINANCE_API_BASE_URL=https://$(oc get route acme-finance-service -o jsonpath='{.spec.host}')"
```

Set these in your `.env` file.

### 5. Explore the APIs

- Customer Swagger: `https://<customer-route>/swagger-ui.html`
- Finance Swagger: `https://<finance-route>/swagger-ui.html`

## Verification

```bash
source .env

# Search customers
curl $CUSTOMER_API_BASE_URL/api/customers?companyName=Around

# Get order history
curl -X POST $FINANCE_API_BASE_URL/api/finance/orders/history \
  -H "Content-Type: application/json" \
  -d '{"customerId": "AROUT"}'
```

You should see JSON responses with customer and order data.

## Key Takeaways

- The Customer API provides CRUD + search operations for customer master data
- The Finance API provides order/invoice history, dispute management, and receipt recovery
- Both APIs use PostgreSQL and auto-populate with seed data on startup
- These APIs will be wrapped as MCP tools in the next module

## Next Module

Proceed to [02-mcp-servers](../02-mcp-servers/) to wrap these APIs as LLM-callable MCP tools.
