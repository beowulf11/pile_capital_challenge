# pile_capital_challenge

FastAPI solution for coding challenge.

## Description

Projects has the following structure:

```bash
pile_capital_challenge/
├── deploy/  # Docker stuff.
│   ├── python/
│   │  └── Dockerfile  # Dockerfile to build python backend image.
│   ├── docker-compose.yml  # Production docker-compose file.
│   ├── docker-compose.dev.yml  # Development docker-compose file.
│   └── docker-compose.test.yml  # Test docker-compose file.
├── migrations/  # Alembic migrations for database.
├── src/  # Startup script. Starts uvicorn.
│   ├── accounts/  # Module for accounts. Includes Router, Repository, Models and Schema.
│   ├── core/  # Module for core functionality. Includes Application, Settings, BaseSchema, BaseModel, Middleware, ...
│   ├── db/  # Module contains db configurations, engine, session, ...
│   ├── debug/  # Module contains routes for development. Currently only /seed.
│   ├── transactions/  # Module for transactions. Includes Router, Repository, Models and Schema.
│   └── __main__.py  # Startup script. Starts uvicorn.
├── tests  # Tests for project.
├── curl requests export.sh  # Curl requests.
├── Makefile  # Makefile for project. Run `make` to get help.
├── pile_capital_challenge.postman_collection.json  # Postman collection.
├── pyproject.toml  # Project configuration.
└── README.md  # This file.
```

You need to have `docker` and `docker compose` installed to run this project
(preferably `make` too). To get help run `make` in the root directory of the project.

## Running

To start a development version of the project run:

```bash
make dev-build  # Build docker image.
make dev
```

You can see swagger documentation at `http://localhost:8000/api/docs`.

To seed the database go to `http://localhost:8000/api/docs` and send `accounts.json`
to `/api/debug/seed/` endpoint. This will ingest the accounts into the database. If you
want to delete the database, run `make dev-db-delete`.

## Development

To start a development version of the project run:

```bash
make dev-build  # Build docker image.
make dev
```

You can start editing files. Once saved the project will be reloaded.

## Connection to FE

I am not sure if you want something specific here, or just a generic description of how
to connect to the backend. It will be a description of how to use individual endpoints.

We would "import" the routes to our FE application. The accounts endpoint has an array
of accounts and `metadata` object which hold information regarding pagination. So the
initial page would show a paginated list of accounts with some filter at the top and
paging controls at the bottom. Each account would be a link to their
detail (`/api/accounts/{iban}`). The detail page would show the account details
from `/api/accounts/{iban}`.

On the profile page there would be option to create a new transaction. This would send a
POST request to `/api/transactions/` with the transaction data. If successful, we need
to update the account balance on the FE.

## Notes

I was not sure what `Log each transfer either through the application or your db
extension of choice. Make sure that these logs persist.` means, so I created a table
`transfer_logs` which logs all transfers.

## Improvements

List of improvements that could be done to the project:

- Add more tests
- Actually use .env file. Currently it is not used, but it's prepared.
- Setup needed for production version
- Add command to apply migrations (up or down)
- Specific endpoint for account transactions
- More filter to transactions
- Caching
- ...
