# StartupPilot AI API Contract

Base path: `/api/v1`

## Authentication

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/google`
- `POST /auth/refresh`
- `GET /auth/me`

## Projects

- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `DELETE /projects/{project_id}`

## Generators

- `POST /projects/{project_id}/generations`
- `GET /projects/{project_id}/generations`
- `GET /generations/{generation_id}`

## Reports

- `GET /projects/{project_id}/reports`
- `GET /reports/{report_id}`

## Documents and RAG

- `POST /projects/{project_id}/documents`
- `GET /projects/{project_id}/documents`
- `POST /projects/{project_id}/chat`

## Exports

- `POST /reports/{report_id}/exports`
- `GET /exports/{export_id}`

## Billing

- `GET /billing/subscription`
- `POST /billing/checkout`
- `POST /billing/portal`

