#!/usr/bin/env bash
#
# ACME Agent Workshop -- Full Deployment Script
#
# Builds container images via OpenShift Binary Builds and deploys
# all backend services (PostgreSQL, APIs, MCP servers) into the
# target namespace.
#
# Usage:
#   ./deploy.sh [NAMESPACE]
#
# Default namespace: acme-workshop
# Requires: oc CLI logged in with cluster-admin or namespace-admin privileges.

set -euo pipefail

NAMESPACE="${1:-acme-workshop}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
K8S_DIR="$SCRIPT_DIR/k8s"

info()  { echo "==> $*"; }
error() { echo "ERROR: $*" >&2; exit 1; }

command -v oc >/dev/null 2>&1 || error "oc CLI not found. Install it from https://mirror.openshift.com/pub/openshift-v4/clients/ocp/"
oc whoami >/dev/null 2>&1   || error "Not logged in to OpenShift. Run: oc login <cluster>"

# ---------------------------------------------------------------------------
# 1. Ensure namespace exists
# ---------------------------------------------------------------------------
info "Using namespace: $NAMESPACE"
if ! oc get project "$NAMESPACE" >/dev/null 2>&1; then
  info "Creating namespace $NAMESPACE"
  oc new-project "$NAMESPACE" --display-name="ACME Workshop" || oc create namespace "$NAMESPACE"
fi
oc project "$NAMESPACE"

# ---------------------------------------------------------------------------
# 2. Build container images (Binary Builds)
# ---------------------------------------------------------------------------
build_image() {
  local name="$1"
  local context_dir="$2"
  local dockerfile_relpath="${3:-}"

  info "Building image: $name (from $context_dir)"

  # If the Dockerfile lives in a subdirectory (e.g. deployment/Dockerfile),
  # copy it to the context root temporarily so `oc start-build` can find it.
  local needs_cleanup=false
  if [[ -n "$dockerfile_relpath" && -f "$context_dir/$dockerfile_relpath" && ! -f "$context_dir/Dockerfile" ]]; then
    cp "$context_dir/$dockerfile_relpath" "$context_dir/Dockerfile"
    needs_cleanup=true
  fi

  if oc get buildconfig "$name" -n "$NAMESPACE" >/dev/null 2>&1; then
    info "  BuildConfig $name already exists, starting new build"
  else
    oc new-build --binary --strategy=docker --name="$name" -n "$NAMESPACE" 2>/dev/null || true
  fi

  oc start-build "$name" \
    --from-dir="$context_dir" \
    --follow \
    -n "$NAMESPACE"

  if $needs_cleanup; then
    rm -f "$context_dir/Dockerfile"
  fi

  info "  Image $name built successfully"
}

info "Building Java API images (this takes 2-4 min each)..."
build_image "customer-api" "$REPO_ROOT/01-backend-apis/customer-api" "deployment/Dockerfile"
build_image "finance-api"  "$REPO_ROOT/01-backend-apis/finance-api"  "deployment/Dockerfile"
build_image "mortgage-api" "$REPO_ROOT/mortgage-use-case/mortgage-api" "deployment/Dockerfile"

info "Building Python MCP server images..."
build_image "customer-mcp" "$REPO_ROOT/02-mcp-servers/customer-mcp"
build_image "finance-mcp"  "$REPO_ROOT/02-mcp-servers/finance-mcp"
build_image "mortgage-mcp" "$REPO_ROOT/mortgage-use-case/mortgage-mcp"

# ---------------------------------------------------------------------------
# 3. Deploy PostgreSQL, APIs, MCP servers
# ---------------------------------------------------------------------------
apply_with_namespace() {
  local file="$1"
  # Replace the NAMESPACE placeholder with the actual namespace
  sed "s|NAMESPACE|$NAMESPACE|g" "$file" | oc apply -n "$NAMESPACE" -f -
}

info "Deploying PostgreSQL instances..."
oc apply -n "$NAMESPACE" -f "$K8S_DIR/postgres.yaml"

info "Waiting for PostgreSQL pods to be ready..."
oc rollout status deployment/postgres-cust -n "$NAMESPACE" --timeout=120s
oc rollout status deployment/postgres-fin  -n "$NAMESPACE" --timeout=120s
oc rollout status deployment/postgres-mort -n "$NAMESPACE" --timeout=120s

info "Deploying backend APIs..."
apply_with_namespace "$K8S_DIR/apis.yaml"

info "Deploying MCP servers..."
apply_with_namespace "$K8S_DIR/mcps.yaml"

# ---------------------------------------------------------------------------
# 4. Wait for all pods
# ---------------------------------------------------------------------------
info "Waiting for API pods to be ready (may take 60-90s for Spring Boot startup)..."
oc rollout status deployment/customer-api -n "$NAMESPACE" --timeout=180s
oc rollout status deployment/finance-api  -n "$NAMESPACE" --timeout=180s
oc rollout status deployment/mortgage-api -n "$NAMESPACE" --timeout=180s

info "Waiting for MCP server pods to be ready..."
oc rollout status deployment/customer-mcp -n "$NAMESPACE" --timeout=120s
oc rollout status deployment/finance-mcp  -n "$NAMESPACE" --timeout=120s
oc rollout status deployment/mortgage-mcp -n "$NAMESPACE" --timeout=120s

# ---------------------------------------------------------------------------
# 5. Print environment block for participants
# ---------------------------------------------------------------------------
CLUSTER_DOMAIN=$(oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}')

echo ""
echo "========================================================================"
echo "  Deployment complete!  Namespace: $NAMESPACE"
echo "========================================================================"
echo ""
echo "Paste the following into your .env file:"
echo ""
echo "# ACME Backend APIs (OpenShift routes)"
echo "CUSTOMER_API_BASE_URL=https://$(oc get route acme-customer-service -n "$NAMESPACE" -o jsonpath='{.spec.host}')"
echo "FINANCE_API_BASE_URL=https://$(oc get route acme-finance-service -n "$NAMESPACE" -o jsonpath='{.spec.host}')"
echo "MORTGAGE_API_BASE_URL=https://$(oc get route mortgage-api-route -n "$NAMESPACE" -o jsonpath='{.spec.host}')"
echo ""
echo "# MCP Servers (OpenShift routes)"
echo "CUSTOMER_MCP_SERVER_URL=https://$(oc get route mcp-customer-route -n "$NAMESPACE" -o jsonpath='{.spec.host}')/mcp"
echo "FINANCE_MCP_SERVER_URL=https://$(oc get route mcp-finance-route -n "$NAMESPACE" -o jsonpath='{.spec.host}')/mcp"
echo "MORTGAGE_MCP_SERVER_URL=https://$(oc get route mcp-mortgage-route -n "$NAMESPACE" -o jsonpath='{.spec.host}')/mcp"
echo ""
echo "========================================================================"
echo ""
echo "Pod status:"
oc get pods -n "$NAMESPACE" -l 'app in (postgres-cust,postgres-fin,postgres-mort,customer-api,finance-api,mortgage-api,customer-mcp,finance-mcp,mortgage-mcp)'
