# Initialize and prepare a repo cloned/pushed from guillaume-chervet/MLOpsPython
# Creates env + GitHub secrets (AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID, AZURE_CREDENTIALS, GIT_TOKEN)
# Robust Azure login: handles expired tokens by forcing interactive login if needed
# Robust GitHub: if fork is forbidden (you own the parent), create a new repo and push the source history

param (
    [string]$repositoryName = "MLOpsPythonWorkshop",
    [string]$environmentName = "MLOpsPython",
    [string]$tenantId = ""   # Optional: pass your tenantId to skip detection
)

$ErrorActionPreference = "Stop"

function Get-DefaultBranch {
    param([string]$RepoPath)
    Push-Location $RepoPath
    try {
        $line = git remote show origin | Select-String "HEAD branch" | ForEach-Object { $_.Line }
        if ($line) { return ($line -split ":" )[-1].Trim() } else { return "main" }
    } finally {
        Pop-Location
    }
}

function Ensure-Azure-Login {
    param([string]$PreferredTenantId)

    Write-Host "Checking Azure login..."

    # Try a quick probe to see if we're logged in
    $loggedIn = $true
    try { az account show 1>$null 2>$null } catch { $loggedIn = $false }

    if (-not $loggedIn) {
        Write-Host "Not logged in. Performing 'az login --allow-no-subscriptions'..."
        az login --allow-no-subscriptions | Out-Null
    }

    # If tenantId provided, prefer it
    if ($PreferredTenantId) {
        Write-Host "Using provided tenantId: $PreferredTenantId"
        try {
            az login --tenant $PreferredTenantId --allow-no-subscriptions | Out-Null
        } catch {
            Write-Warning "Login to provided tenant failed. Forcing re-auth..."
            az logout | Out-Null
            # Device code helps when browser SSO/session is stale
            az login --tenant $PreferredTenantId --allow-no-subscriptions --use-device-code | Out-Null
        }
        return $PreferredTenantId
    }

    # Else discover first tenant
    $firstTenantId = ""
    try {
        # This may fail with expired tokens; that's why we catch and retry below
        $firstTenantId = az account tenant list --query "[0].tenantId" -o tsv
    } catch {
        $firstTenantId = ""
    }

    if (-not $firstTenantId) {
        Write-Warning "Unable to list tenants (token likely expired). Forcing re-auth..."
        az logout | Out-Null
        # Interactive login (device code works everywhere)
        az login --allow-no-subscriptions --use-device-code | Out-Null

        # Retry tenant discovery
        try {
            $firstTenantId = az account tenant list --query "[0].tenantId" -o tsv
        } catch {
            $firstTenantId = ""
        }
    }

    if (-not $firstTenantId) {
        Write-Error "Impossible de récupérer un tenant via 'az account tenant list'. Exécute manuellement:
  az logout
  az login --tenant ""<TON_TENANT_ID>"" --scope ""https://management.core.windows.net//.default""
Puis relance le script."
        exit 1
    }

    # Lock session to that tenant
    try {
        az login --tenant $firstTenantId --allow-no-subscriptions | Out-Null
    } catch {
        Write-Warning "Login to discovered tenant failed. Forcing device-code auth..."
        az logout | Out-Null
        az login --tenant $firstTenantId --allow-no-subscriptions --use-device-code | Out-Null
    }

    return $firstTenantId
}

function Get-First-Subscription-ForTenant {
    param([string]$Tenant)

    # Prefer default subscription in this tenant
    $sid = az account list --query "[?tenantId=='$Tenant' && isDefault] | [0].id" -o tsv
    if (-not $sid) {
        $sid = az account list --query "[?tenantId=='$Tenant'] | [0].id" -o tsv
    }
    if ($sid) {
        az account set --subscription $sid | Out-Null
        Write-Host "Using tenant: $Tenant and subscription: $sid"
    } else {
        Write-Host "No subscription found for tenant $Tenant. Continuing (some operations require a subscription)."
    }
    return $sid
}

# -------------------
# Azure: ensure login + tenant + subscription
# -------------------
$tenantId = Ensure-Azure-Login -PreferredTenantId $tenantId
$subscriptionId = Get-First-Subscription-ForTenant -Tenant $tenantId

# -------------------
# GitHub auth
# -------------------
Write-Host "GitHub CLI authentication..."
gh auth login

# -------------------
# Try fork, else fallback to "create new repo and push source"
# -------------------
$sourceRepo = "guillaume-chervet/MLOpsPython"
$targetName = $repositoryName

Write-Host "Forking repo and setting remotes..."
$forkOk = $true
$forkError = $null
try {
    gh repo fork "https://github.com/$sourceRepo" --default-branch-only --fork-name $targetName --clone
} catch {
    $forkOk = $false
    $forkError = $_.Exception.Message
}

if (-not $forkOk -or -not (Test-Path -LiteralPath $targetName)) {
    if ($forkError) {
        Write-Host "Fork failed: $forkError"
    } else {
        Write-Host "Fork failed: directory '$targetName' not created."
    }

    $ghLogin = gh api user --jq .login
    if (-not $ghLogin) {
        Write-Error "Unable to get GitHub login via 'gh api user'."
        exit 1
    }

    Write-Host "Creating new repository '$ghLogin/$targetName'..."
    gh repo create "$ghLogin/$targetName" --private --disable-wiki --confirm

    # Clone source repo to a temp location
    $tempRoot = Join-Path $env:TEMP ("src-" + [System.Guid]::NewGuid().ToString("N"))
    git clone "https://github.com/$sourceRepo" $tempRoot | Out-Null

    $defaultBranch = Get-DefaultBranch -RepoPath $tempRoot
    if (-not $defaultBranch) { $defaultBranch = "main" }

    Push-Location $tempRoot
    try {
        git remote remove origin 2>$null
        git remote add origin "https://github.com/$ghLogin/$targetName.git"
        git push -u origin --all
        git push --tags
    } finally {
        Pop-Location
    }

    if (Test-Path -LiteralPath $targetName) {
        Write-Host "Target folder '$targetName' already exists locally; skipping move."
    } else {
        Move-Item -LiteralPath $tempRoot -Destination $targetName
    }
}

Set-Location $targetName

# Remove 'upstream' if exists (ignore errors)
try { git remote remove upstream 2>$null } catch { }

$repoDefaultBranch = Get-DefaultBranch -RepoPath (Get-Location).Path
if (-not $repoDefaultBranch) { $repoDefaultBranch = "main" }
git push --set-upstream origin $repoDefaultBranch

# Repo nameWithOwner (org/repo)
$repositoryFullName = gh repo view --json nameWithOwner -q ".nameWithOwner"
gh repo set-default "https://github.com/${repositoryFullName}"

# Create environment
Write-Host "Creating environment '$environmentName'..."
gh api --method PUT -H "Accept: application/vnd.github+json" repos/${repositoryFullName}/environments/${environmentName}

# -------------------
# Azure SP + Secrets
# -------------------
if (-not $subscriptionId) {
    # try once more (user may have set one after login)
    try { $subscriptionId = az account show --query "id" -o tsv } catch { $subscriptionId = "" }
}

$credentials = "{}"
if ($subscriptionId) {
    Write-Host "Creating Service Principal (Contributor) scoped to subscription..."
    $spName = "mlapp-$($repositoryName)-$(Get-Date -Format 'yyyyMMddHHmmss')"
    $credentials = az ad sp create-for-rbac --name $spName --role contributor --scopes /subscriptions/$subscriptionId --sdk-auth | Out-String
} else {
    Write-Host "No subscription => skipping SP creation (AZURE_CREDENTIALS will be '{}')."
}

# Secrets
if ($tenantId) {
    Write-Host "Setting AZURE_TENANT_ID..."
    gh secret set AZURE_TENANT_ID --body $tenantId --env "$environmentName"
}
if ($subscriptionId) {
    Write-Host "Setting AZURE_SUBSCRIPTION_ID..."
    gh secret set AZURE_SUBSCRIPTION_ID --body $subscriptionId --env "$environmentName"
}

Write-Host "Setting AZURE_CREDENTIALS..."
$jsonCredentials = $credentials | ConvertFrom-Json | ConvertTo-Json -Compress
$jsonCredentials | gh secret set AZURE_CREDENTIALS --env "$environmentName" --body -

Write-Host "Setting GIT_TOKEN..."
$git_token = gh auth token
gh secret set GIT_TOKEN --body "$git_token" --env "$environmentName"

# Enable workflow
Write-Host "Enabling workflow main.yml..."
gh workflow enable main.yml

# Open repo
Write-Host "Opening repository page..."
gh repo view -w
