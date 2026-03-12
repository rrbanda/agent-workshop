# Module 01: Backend APIs

## Learning Objectives

- Understand the NovaCrest domain model (Customer and Finance)
- Run the Spring Boot REST APIs locally
- Explore the API endpoints via Swagger UI

> **Capstone Preview:** In the capstone, you will work with a Mortgage API that follows this same Spring Boot pattern -- same entity/repository/controller structure, same Swagger UI, same seed data approach.

## Prerequisites

- [Module 00: Environment Setup](../00-setup/) completed
- PostgreSQL running with `novacrest_customer` and `novacrest_finance` databases

## Concepts

Agents need **tools** to interact with the real world. In this workshop, the tools are REST APIs that manage NovaCrest's customer and financial data. Before building agents, you need to understand what data and operations are available.

## NovaCrest Domain Model

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

> **Working directory:** All commands in this module run from `01-backend-apis/`.

### 1. Build and Run Customer API

In a dedicated terminal:

```bash
cd customer-api
mvn clean package -DskipTests
mvn spring-boot:run
```

### 2. Build and Run Finance API

In a second terminal:

```bash
cd finance-api
mvn clean package -DskipTests
mvn spring-boot:run
```

### 3. Explore the APIs

- Customer Swagger: http://localhost:8081/swagger-ui.html
- Finance Swagger: http://localhost:8082/swagger-ui.html

## Verification

```bash
# Search customers
curl http://localhost:8081/api/customers?companyName=Around

# Get order history
curl -X POST http://localhost:8082/api/finance/orders/history \
  -H "Content-Type: application/json" \
  -d '{"customerId": "AROUT"}'
```

## Key Takeaways

- The Customer API provides CRUD + search operations for customer master data
- The Finance API provides order/invoice history, dispute management, and receipt recovery
- Both APIs use PostgreSQL and auto-populate with seed data on startup
- These APIs will be wrapped as MCP tools in the next module

## Next Module

Proceed to [02-mcp-servers](../02-mcp-servers/) to wrap these APIs as LLM-callable MCP tools.
