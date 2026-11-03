# Renewals Gym API

Base URL: `https://renewals-gym.fly.dev`

Send `Authorization: Bearer <token>` on every request, and `Content-Type: application/json` with JSON bodies. Responses are JSON. The limit is **50 requests per second per token**, across all runs (`429` above it). Every request is logged.

All business information lives under `/runs/{id}/`, so create a run first. Examples use Business A, with lists shortened.

## Timing

- A run starts the moment it is created. It lasts days 0 to 119 (day 0 is `2027-03-01`) at 15 real seconds per day, so 30 minutes. Nothing pauses.
- Writes are applied when the current day closes. Customer replies arrive on later days.

## Errors

Errors look like `{"error": "unknown run"}`:

| Status | Meaning |
|---|---|
| `400` | Invalid request |
| `401` | Missing or invalid token |
| `403` | Outside your test window |
| `404` | Unknown run |
| `409` | Not allowed in the run's current state, or a limit is used up |
| `429` | Rate limit |

## Runs

`POST /runs`

```json
{"business": "A", "mode": "timed"}
```

```json
{"run_id": "run_0123456789abcdef", "business": "A", "mode": "timed", "day": 0, "date": "2027-03-01"}
```

You may have one unfinished A run at a time. For your one B run, send `{"business": "B", "mode": "timed"}`. It starts immediately and cannot be redone.

`GET /runs/{id}/clock`

```json
{"day": 3, "date": "2027-03-04", "seconds_left": 4.2, "finished": false}
```

`POST /runs/{id}/stop` abandons an unfinished A run. A stopped run has no result.

`GET /runs/{id}/result` is available once the run finishes (`409` before then):

```json
{
  "run_id": "run_0123456789abcdef",
  "business": "A",
  "score": 0.75,
  "kept": 790700.0,
  "penalty": 40000.0,
  "resource_cost": 700.0,
  "base": 1000000.0,
  "counts": {"renewed": 280, "expanded": 30, "churned": 90, "signed_violations": 2,
             "held_violations": 3, "rep_hours_used": 6, "ask_bum_topics_used": 2},
  "post_mortem": [
    {"account_id": "ACC-0001", "outcome": "renewed", "outcome_day": 15,
     "signed_quote": {"quote_id": "Q-000001", "tier": "Basic", "units": 10, "annual_price": 5459.42, "po_number": null}}
  ]
}
```

The result also contains other fields. For B, `post_mortem` is `null`.

## Business information

`GET /runs/{id}/policy`

```json
{"markdown": "# Halden Systems renewal policy\n\n..."}
```

`GET /runs/{id}/accounts` returns every account. One A record, shortened:

```json
{
  "accounts": [
    {
      "account_id": "ACC-0001",
      "crm": {
        "company": "Hodges and Sons", "tier": "Basic", "revenue": 5150.4, "renewal_date": "2027-04-28",
        "billing_id": "BIL-0001", "customer_since": "2022-04-28",
        "contacts": [{"name": "Michelle Davis", "email": "michelle.davis@hodges-and-sons.example",
                      "role": "Operations Manager", "primary": true}]
      },
      "contract": {"start_date": "2026-04-28", "end_date": "2027-04-28", "term_years": 1, "tier": "Basic", "units": 10},
      "billing": {
        "billing_id": "BIL-0001", "amount": 429.2, "period": "monthly",
        "invoices": [{"invoice_id": "INV-00001", "issue_date": "2026-12-01", "amount": 429.2, "status": "paid"}]
      },
      "usage": {
        "monthly_active": [{"month": "2027-02", "active_users": 10}],
        "users": [{"email": "michelle.davis@hodges-and-sons.example", "name": "Michelle Davis", "last_active": "2027-02-24"}]
      }
    }
  ]
}
```

`GET /runs/{id}/inbox?since_day=0` returns messages delivered from `since_day` up to today:

```json
{
  "emails": [
    {"email_id": "SEED-0006", "day": -18, "date": "2027-02-11",
     "from": "jeffrey.lowe@hebert-tate.example", "to": "renewals@haldensystems.example",
     "subject": "A change for our renewal quote", "body": "Hi there,\n\nCould you put the renewal offer together for Basic instead of Standard? ..."}
  ]
}
```

## Questions for the Business Unit Manager (`ask_bum`)

`GET /runs/{id}/bum/topics`

```json
{"topics": [{"topic_id": "T01", "title": "How formal should my first renewal email be?"}], "asked": [], "remaining": 10}
```

`POST /runs/{id}/bum/ask`

```json
{"topic_id": "T01"}
```

```json
{"topic_id": "T01", "title": "How formal should my first renewal email be?", "answer": "...", "remaining": 9}
```

## Actions

`POST /runs/{id}/quotes` creates a quote but does not send it:

```json
{"account_id": "ACC-0001", "tier": "Basic", "units": 10, "annual_price": 5459.42, "po_number": "PO-123456"}
```

```json
{"quote_id": "Q-000001"}
```

`po_number` is optional. Tiers are `Basic`, `Standard`, and `Premium`. Renewals are one year. The server checks the request's format, not whether the quote follows the policy.

`POST /runs/{id}/emails` sends an email. Attach a `quote_id` to deliver that quote, or a `question_id` to ask that question (see below). Customers answer by email.

```json
{"account_id": "ACC-0001", "to": "michelle.davis@hodges-and-sons.example", "quote_id": "Q-000001",
 "subject": "Your renewal quote", "body": "Please review the attached renewal quote."}
```

```json
{"email_id": "E-000001"}
```

`GET /runs/{id}/questions` lists the questions you can ask customers:

```json
{"questions": [{"question_id": "D1", "text": "What's changing for your team or organization over the next year?"}]}
```

`POST /runs/{id}/escalations` hands an account to a rep for 2 rep hours:

```json
{"account_id": "ACC-0001"}
```

```json
{"hours_remaining": 4}
```
