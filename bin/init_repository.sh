# Script based on https://www.techwatching.dev/posts/scripting-azure-ready-github-repository/
#.\init_repository.sh "MLOpsPythonMyDemo" "MLOpsPython"

# Définir les paramètres avec des valeurs par défaut
repositoryName="${1:-MLOpsPythonWorkshop}"
environmentName="${2:-MLOpsPython}"

# Authenticate using Azure CLI (az) and GitHub CLI (gh)
az login
gh auth login

# Fork MLOpsPython repository
gh repo fork https://github.com/guillaume-chervet/MLOpsPython --default-branch-only --fork-name "$repositoryName" --clone

# Change directory to the local repository
cd "$repositoryName"

# Remove the upstream remote and set the upstream to the main branch
git remote remove upstream
git push --set-upstream origin main

# Retrieve the repository full name (org/repo)
repositoryFullName=$(gh repo view --json nameWithOwner -q ".nameWithOwner")

# Set the default repository
gh repo set-default "https://github.com/${repositoryFullName}"

# Create environment
gh api --method PUT -H "Accept: application/vnd.github+json" "repos/${repositoryFullName}/environments/${environmentName}"

# Retrieve the current subscription and current tenant identifiers using Azure CLI
subscriptionId=$(az account show --query "id" -o tsv)
tenantId=$(az account show --query "tenantId" -o tsv)
credentials=$(az ad sp create-for-rbac --name "mlapp" --role contributor --scopes "/subscriptions/$subscriptionId" --sdk-auth)
# Create an App Registration and its associated service principal using Azure CLI
#appId=$(az ad app create --display-name "GitHub Action OIDC for ${repositoryFullName}" --query "appId" -o tsv)
#servicePrincipalId=$(az ad sp create --id "$appId" --query "id" -o tsv)

# Assign the contributor role to the service principal on the subscription using Azure CLI
#az role assignment create --role contributor --subscription "$subscriptionId" --assignee-object-id "$servicePrincipalId" --assignee-principal-type ServicePrincipal --scope "/subscriptions/$subscriptionId"

# Prepare parameters for federated credentials
#parametersJson='{
#    "name": "'"$environmentName"'",
#    "issuer": "https://token.actions.githubusercontent.com",
#    "subject": "repo:'"$repositoryFullName"':environment:'"$environmentName"'",
#    "description": "Development",
#    "audiences": [
#        "api://AzureADTokenExchange"
#    ]
#}'

# Create federated credentials using Azure CLI
#az ad app federated-credential create --id "$appId" --parameters "$parametersJson"

# Create GitHub secrets needed for the GitHub Actions using GitHub CLI
#gh secret set AZURE_TENANT_ID --body "$tenantId" --env "$environmentName"
#gh secret set AZURE_SUBSCRIPTION_ID --body "$subscriptionId" --env "$environmentName"
#gh secret set AZURE_CLIENT_ID --body "$appId" --env "$environmentName"
jsonCredentials=$(echo "$credentials" | jq -c .)
escapedJsonCredentials=$(echo $jsonCredentials | sed 's/"/\\"/g')
echo escapedJsonCredentials
gh secret set AZURE_CREDENTIALS --body "$escapedJsonCredentials" --env "$environmentName"
gh secret set DOCKER_PASSWORD --body "robertcarry" --env "$environmentName"
gh secret set DOCKER_USENAME --body "dckr_pat_e2lZ9YgpMt8APE-Qxzn89u6mt28" --env "$environmentName"

# Run the GitHub workflow
gh workflow enable main.yml
#gh workflow run main.yml

# Get the run ID
#runId=$(gh run list --workflow=main.yml --json databaseId -q ".[0].databaseId")

# Watch the run
#gh run watch "$runId"

# Open the repository in the browser
gh repo view -w