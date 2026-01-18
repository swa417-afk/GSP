#!/bin/bash
echo "Testing GSP Backend API..."
echo ""

BASE_URL="http://localhost:4000"

# 1. Health Check
echo "1. Testing /health endpoint..."
curl -s $BASE_URL/health | jq .
echo ""

# 2. Register User
echo "2. Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}')
echo $REGISTER_RESPONSE | jq .
echo ""

# 3. Login
echo "3. Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}')
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')
echo $LOGIN_RESPONSE | jq .
echo ""

# 4. Submit GSP Receipt
echo "4. Testing GSP receipt submission..."
SUBMIT_RESPONSE=$(curl -s -X POST $BASE_URL/api/gsp/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "modelId": "gpt-4",
    "inputHash": "abc123hash",
    "outputHash": "xyz789hash",
    "policyId": "policy-001"
  }')
RECEIPT_ID=$(echo $SUBMIT_RESPONSE | jq -r '.receiptId')
echo $SUBMIT_RESPONSE | jq .
echo ""

# 5. Get Receipt
echo "5. Testing receipt retrieval..."
curl -s $BASE_URL/api/gsp/receipt/$RECEIPT_ID \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 6. List Receipts
echo "6. Testing receipts list..."
curl -s $BASE_URL/api/gsp/receipts \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

echo "✅ API Test Complete!"
