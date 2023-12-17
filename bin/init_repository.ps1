# Script based on https://www.techwatching.dev/posts/scripting-azure-ready-github-repository/
# Initialize git repository with current code
# You should have added the main.yml workflow file in the `.github\workflows` directory

#.\init_repository.ps1 -repositoryName "MLOpsPythonMyDemo" -environmentName "MLOpsPython"
param (
    [string]$repositoryName = "MLOpsPythonWorkshop",
    [string]$environmentName = "MLOpsPython"
)

az login
gh auth login

# Fork MLOPsPython repository
gh repo fork https://github.com/guillaume-chervet/MLOpsPython --default-branch-only --fork-name $repositoryName --clone
cd $repositoryName
git remote remove upstream
git push --set-upstream origin main

# Retrieve the repository full name (org/repo)
$repositoryFullName=$(gh repo view --json nameWithOwner -q ".nameWithOwner")

gh repo set-default "https://github.com/${repositoryFullName}"

# Create environment
gh api --method PUT -H "Accept: application/vnd.github+json" repos/${repositoryFullName}/environments/${environmentName}

# Retrieve the current subscription and current tenant identifiers
$subscriptionId=$(az account show --query "id" -o tsv)
$tenantId=$(az account show --query "tenantId" -o tsv)

# Create an App Registration and its associated service principal
$appId=$(az ad app create --display-name "GitHub Action OIDC for ${repositoryFullName}" --query "appId" -o tsv)
$servicePrincipalId=$(az ad sp create --id $appId --query "id" -o tsv)

# Assign the contributor role to the service principal on the subscription
az role assignment create --role contributor --subscription $subscriptionId --assignee-object-id  $servicePrincipalId --assignee-principal-type ServicePrincipal --scope /subscriptions/$subscriptionId

# Prepare parameters for federated credentials
$parametersJson=@{
    name = "${environmentName}"
    issuer = "https://token.actions.githubusercontent.com"
    subject = "repo:${repositoryFullName}:environment:${environmentName}"
    description = "Development"
    audiences = @(
        "api://AzureADTokenExchange"
    )
}

# Change parameters to single line string with escaped quotes to make it work with Azure CLI
# https://medium.com/medialesson/use-dynamic-json-strings-with-azure-cli-commands-in-powershell-b191eccc8e9b
$parameters=$($parametersJson | ConvertTo-Json -Depth 100 -Compress).Replace("`"", "\`"")

# Create federated credentials
az ad app federated-credential create --id $appId --parameters $parameters

# Create GitHub secrets needed for the GitHub Actions
gh secret set AZURE_TENANT_ID --body $tenantId --env $environmentName
gh secret set AZURE_SUBSCRIPTION_ID --body $subscriptionId --env $environmentName
gh secret set AZURE_CLIENT_ID --body $appId --env $environmentName
gh secret set DOCKER_PASSWORD --body "robertcarry" --env "$environmentName"
gh secret set DOCKER_USENAME --body "dckr_pat_e2lZ9YgpMt8APE-Qxzn89u6mt28" --env "$environmentName"

# Run workflow
gh workflow enable main.yml
#gh workflow run main.yml
#$runId=$(gh run list --workflow=main.yml --json databaseId -q ".[0].databaseId")
#gh run watch $runId

# Open the repository in the browser
gh repo view -w