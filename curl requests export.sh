## Get Accounts
curl "http://localhost:8000/api/accounts/?balance_gt=1000&balance_lt=1000000&page_size=10&page=1" \
     -H 'Accept: application/json'

## Get Account
curl "http://localhost:8000/api/accounts/DE51656568681196355587/" \
     -H 'Accept: application/json'

## Get Transactions
curl "http://localhost:8000/api/transactions/?page_size=10&page=1" \
     -H 'Accept: application/json'

## Create Transaction
curl -X "POST" "http://localhost:8000/api/transactions/" \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json' \
     -d $'{
  "targetAccountIban": "DE51656568681196355587",
  "sourceAccountIban": "DE20214577582752901028",
  "reference": "reference",
  "recipientName": "recipientName",
  "amount": 100,
  "targetBic": "targetBic"
}'

## Seed
curl -X "POST" "http://localhost:8000/api/debug/seed/" \
     -H 'Content-Type: multipart/form-data' \
     -H 'Accept: application/json' \
     -d $'{
  "upload_file": ""
}'
