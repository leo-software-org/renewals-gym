"""Read a timed Business A run, then abandon it; no renewal strategy."""

import os

import httpx


def main() -> None:
    base_url = os.environ["GYM_BASE_URL"].rstrip("/")
    token = os.environ["GYM_TOKEN"]
    with httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {token}"}, timeout=30) as client:
        response = client.post("/runs", json={"business": "A", "mode": "timed"})
        response.raise_for_status()
        run_path = f"/runs/{response.json()['run_id']}"

        try:
            policy = client.get(f"{run_path}/policy")
            policy.raise_for_status()
            print("Policy characters:", len(policy.json()["markdown"]))
            accounts = client.get(f"{run_path}/accounts")
            accounts.raise_for_status()
            rows = accounts.json()["accounts"]
            print("Accounts:", len(rows))
            print("User rows:", sum(len(account["usage"]["users"]) for account in rows))
            inbox = client.get(f"{run_path}/inbox", params={"since_day": 0})
            inbox.raise_for_status()
            print("Day-0 inbox:", len(inbox.json()["emails"]))

            clock = client.get(f"{run_path}/clock")
            clock.raise_for_status()
            print("Clock:", clock.json())
        finally:
            stopped = client.post(f"{run_path}/stop")
            stopped.raise_for_status()
            print("Stopped:", stopped.json())


if __name__ == "__main__":
    main()
