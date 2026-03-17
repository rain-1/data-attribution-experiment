#!/bin/bash

loraname=$1
message=$2

# Let jq safely construct and escape the JSON payload
json_payload=$(jq -n \
  --arg model "$loraname" \
  --arg msg "$message" \
  '{
    model: $model,
    messages: [
      {role: "user", content: $msg}
    ],
    max_tokens: 150
  }')

# Send the safely escaped payload via curl
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "$json_payload" | jq

