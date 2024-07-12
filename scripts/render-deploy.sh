cd ..
pwd

sh add-commit-push.sh

#!/bin/bash

API_KEY="rnd_H5JM4hI2OOZeiVWj6Za2YWxZRgSV"
SERVICE_ID="darwinrest"
REPO_BRANCH="main"  # or the branch you want to deploy from

# API endpoint
API_ENDPOINT="https://api.render.com/v1/services?limit=3/deploys"

# Create JSON payload
read -r -d '' PAYLOAD << EOM
{
  "clearCache": false,
  "branch": "$REPO_BRANCH"
}
EOM

# Make the API request
response=$(curl -s -X POST "$API_ENDPOINT" \
-H "Authorization: Bearer $API_KEY" \
-H "Content-Type: application/json" \
-d "$PAYLOAD")

# Parse the response
deploy_id=$(echo $response | jq -r '.id')

if [[ $deploy_id != "null" ]]; then
  echo "Deployment initiated successfully. Deployment ID: $deploy_id"
else
  echo "Failed to initiate deployment. Response: $response"
fi
