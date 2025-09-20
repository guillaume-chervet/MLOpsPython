#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./init_repository.sh "MLOpsPythonMyDemo" "MLOpsPython" "optional-tenant-id"
# Defaults:
repositoryName="${1:-MLOpsPythonWorkshop}"
environmentName="${2:-MLOpsPython}"
preferredTenantId="${3:-}"

sourceRepo="guillaume-chervet/MLOpsPython"

# ----- helpers -----
get_default_branch() {
  # prints the default branch name for the current repo (assumes 'origin' exists)
  local line
  if line="$(git remote show origin 2>/dev/null | grep 'HEAD branch')"; then
    echo "${line##*: }" | xargs
  else
    echo "main"
  fi
}

ensure_azure_login() {
  # uses $preferredTenantId (may be empty)
  echo "Checking Azure login..."

  if ! az account show >/dev/null 2>&1; then
    echo "Not logged in. Running 'az login --allow-no-subscriptions'..."
    az login --allow-no-subscriptions >/dev/null
  fi

  if [[ -n "$preferredTenantId" ]]; then
    echo "Using provided tenantId: $preferredTenantId"
    if ! az login --tenant "$preferredTenantId" --allow-no-subscriptions >/dev/null 2>&1; then
      echo "Login to provided tenant failed. Forcing re-auth with device code..."
      az logout >/dev/null 2>&1 || true
      az login --tenant "$preferredTenantId" --allow-no-subscriptions --use-device-code >/dev/null
    fi
    echo "$preferredTenantId"
    return 0
  fi

  local firstTenantId=""
  if ! firstTenantId="$(az account tenant list --query "[0].tenantId" -o tsv 2>/dev/null)"; then
    firstTenantId=""
  fi

  if [[ -z "$firstTenantId" ]]; then
    echo "Unable to list tenants (token may be expired). Forcing re-auth..."
    az logout >/dev/null 2>&1 || true
    az login --allow-no-subscriptions --use-device-code >/dev/null
    firstTenantId="$(az account tenant list --query "[0].tenantId" -o tsv)"
  fi

  if [[ -z "$firstTenantId" ]]; then
    echo "ERROR: Impossible de récupérer un tenant via 'az account tenant list'."
    echo "Exécute manuellement :"
    echo '  az logout'
    echo '  az login --tenant "<TON_TENANT_ID>" --scope "https://management.core.windows.net//.default"'
    echo "Puis relance le script."
    exit 1
  fi

  if ! az login --tenant "$firstTenantId" --allow-no-subscriptions >/dev/null 2>&1; then
    echo "Login to discovered tenant failed. Forcing device-code auth..."
    az logout >/dev/null 2>&1 || true
    az login --tenant "$firstTenantId" --allow-no-subscriptions --use-device-code >/dev/null
  fi

  echo "$firstTenantId"
}

get_first_subscription_for_tenant() {
  local tenant="$1"
  local sid=""
  sid="$(az account list --query "[?tenantId=='$tenant' && isDefault] | [0].id" -o tsv)"
  if [[ -z "$sid" ]]; then
    sid="$(az account list --query "[?tenantId=='$tenant'] | [0].id" -o tsv)"
  fi
  if [[ -n "$sid" ]]; then
    az account set --subscription "$sid" >/dev/null
    echo "Using tenant: $tenant and subscription: $sid"
  else
    echo "No subscription found for tenant $tenant. Continuing (some operations require a subscription)."
  fi
  echo "$sid"
}

# ----- Azure login / tenant + subscription -----
tenantId="$(ensure_azure_login)"
subscriptionId="$(get_first_subscription_for_tenant "$tenantId")"

# ----- GitHub auth -----
echo "GitHub CLI authentication..."
gh auth login

# ----- Try fork, else fallback to 'create new repo and push source' -----
echo "Forking repo and setting remotes..."
forkOk=true
if ! gh repo fork "https://github.com/$sourceRepo" --default-branch-only --fork-name "$repositoryName" --clone; then
  forkOk=false
fi

if [[ "$forkOk" != "true" || ! -d "$repositoryName" ]]; then
  echo "Fork failed or target directory missing. Falling back to 'create new repo and push source'..."

  ghLogin="$(gh api user --jq .login)"
  if [[ -z "$ghLogin" ]]; then
    echo "ERROR: Unable to get GitHub login via 'gh api user'."
    exit 1
  fi

  echo "Creating new repository '$ghLogin/$repositoryName'..."
  gh repo create "$ghLogin/$repositoryName" --private --disable-wiki --confirm

  tmpdir="$(mktemp -d)"
  git clone "https://github.com/$sourceRepo" "$tmpdir" >/dev/null

  pushd "$tmpdir" >/dev/null
  defaultBranch="$(get_default_branch)"
  git remote remove origin >/dev/null 2>&1 || true
  git remote add origin "https://github.com/$ghLogin/$repositoryName.git"
  git push -u origin --all
  git push --tags
  popd >/dev/null

  if [[ -d "$repositoryName" ]]; then
    echo "Target folder '$repositoryName' already exists locally; skipping move."
  else
    mv "$tmpdir" "$repositoryName"
  fi
fi

cd "$repositoryName"

# Remove 'upstream' if exists (ignore errors)
git remote remove upstream >/dev/null 2>&1 || true

repoDefaultBranch="$(get_default_branch)"
git push --set-upstream origin "$repoDefaultBranch"

# Repo nameWithOwner (org/repo)
repositoryFullName="$(gh repo view --json nameWithOwner -q ".nameWithOwner")"
gh repo set-default "https://github.com/${repositoryFullName}"

# Create environment
echo "Creating environment '$environmentName'..."
gh api --method PUT -H "Accept: application/vnd.github+json" "repos/${repositoryFullName}/environments/${environmentName}"

# ----- Azure SP + Secrets -----
# Re-check subscriptionId if empty
if [[ -z "${subscriptionId:-}" ]]; then
  subscriptionId="$(az account show --query "id" -o tsv 2>/dev/null || true)"
fi

credentials="{}"
if [[ -n "${subscriptionId:-}" ]]; then
  echo "Creating Service Principal (Contributor) scoped to subscription..."
  spName="mlapp-${repositoryName}-$(date +%Y%m%d%H%M%S)"
  # create-for-rbac outputs JSON
  credentials="$(az ad sp create-for-rbac --name "$spName" --role contributor --scopes "/subscriptions/$subscriptionId" --sdk-auth)"
else
  echo "No subscription => skipping SP creation (AZURE_CREDENTIALS will be '{}')."
fi

# Secrets
if [[ -n "${tenantId:-}" ]]; then
  echo "Setting AZURE_TENANT_ID..."
  printf "%s" "$tenantId" | gh secret set AZURE_TENANT_ID --env "$environmentName" --body -
fi

if [[ -n "${subscriptionId:-}" ]]; then
  echo "Setting AZURE_SUBSCRIPTION_ID..."
  printf "%s" "$subscriptionId" | gh secret set AZURE_SUBSCRIPTION_ID --env "$environmentName" --body -
fi

echo "Setting AZURE_CREDENTIALS..."
# Ensure minified JSON and send via STDIN (avoid quoting issues)
jsonCredentials="$(printf "%s" "$credentials" | jq -c '.')"
printf "%s" "$jsonCredentials" | gh secret set AZURE_CREDENTIALS --env "$environmentName" --body -

echo "Setting GIT_TOKEN..."
git_token="$(gh auth token)"
printf "%s" "$git_token" | gh secret set GIT_TOKEN --env "$environmentName" --body -

# Enable workflow
echo "Enabling workflow main.yml..."
gh workflow enable main.yml

# Open repo
echo "Opening repository page..."
gh repo view -w
