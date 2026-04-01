#!/usr/bin/env bash
#
# ACME Agent Workshop -- Teardown Script
#
# Removes all workshop resources from the target namespace.
# Does NOT delete the namespace itself.
#
# Usage:
#   ./teardown.sh [NAMESPACE]
#
# Default namespace: acme-workshop

set -euo pipefail

NAMESPACE="${1:-acme-workshop}"

info()  { echo "==> $*"; }

command -v oc >/dev/null 2>&1 || { echo "ERROR: oc CLI not found" >&2; exit 1; }

info "Tearing down ACME Workshop resources in namespace: $NAMESPACE"

info "Deleting MCP servers..."
oc delete deployment customer-mcp finance-mcp mortgage-mcp -n "$NAMESPACE" --ignore-not-found
oc delete service mcp-customer-service mcp-finance-service mcp-mortgage-service -n "$NAMESPACE" --ignore-not-found
oc delete route mcp-customer-route mcp-finance-route mcp-mortgage-route -n "$NAMESPACE" --ignore-not-found

info "Deleting backend APIs..."
oc delete deployment customer-api finance-api mortgage-api -n "$NAMESPACE" --ignore-not-found
oc delete service acme-customer-service acme-finance-service acme-mortgage-service -n "$NAMESPACE" --ignore-not-found
oc delete route acme-customer-service acme-finance-service mortgage-api-route -n "$NAMESPACE" --ignore-not-found

info "Deleting PostgreSQL instances..."
oc delete deployment postgres-cust postgres-fin postgres-mort -n "$NAMESPACE" --ignore-not-found
oc delete service postgres-cust postgres-fin postgres-mort -n "$NAMESPACE" --ignore-not-found

info "Deleting build configs and image streams..."
for name in customer-api finance-api mortgage-api customer-mcp finance-mcp mortgage-mcp; do
  oc delete buildconfig "$name" -n "$NAMESPACE" --ignore-not-found
  oc delete imagestream "$name" -n "$NAMESPACE" --ignore-not-found
done

info "Teardown complete for namespace: $NAMESPACE"
