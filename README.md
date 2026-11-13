# Renewals Gym

## 1. The job

Build a renewals engine that maximizes net revenue retention. Your engine reads business records and customer email, asks customers questions, prepares quotes, sends email, asks business questions, and escalates issues through an HTTP API.

**Your result comes from two scored runs: one on Business B, then one on Business C. Business A is practice and is never scored.**

- **Business A is for building and practising.** Run it as often as you like. Each A run returns a per-account ledger you can learn from.
- **Business B is your first test.** It is a completely different company:
  - a different product and unit of sale
  - different usage data
  - a different renewal policy, with different rules and prices
  - different customers

  You won't see any of it until your B run starts. Your engine has to discover B through the API and adapt on its own. Once your B run finishes, its result includes a per-account ledger, as A's does.
- **Then improve.** Study what happened on B and improve your engine. Business C is different again, from A and from B, so fix what made your engine fragile rather than tuning it to B.
- **Business C is your second test.** It is another completely different company that you won't see until your C run starts. You can start it only after your B run has finished. Its result has totals only.
- **Assume nothing carries over between businesses except the API.** An engine tuned to one business's rules and data will fail on the next. Build a renewals engine, not a solution for A or B.
- **You get one B run and one C run.** Each lasts 30 minutes, runs hands-off, and can't be redone. Both must start inside your test window, so leave at least an hour for each, plus time between them to improve your engine. If you don't run them before your window closes, you have no result.

## 2. How you're scored

Your result has three parts: your Business B score, your Business C score, and our review of the code and write-up you send (§5). C shows what you learned from B. The debrief call walks through all of them.

- **Base** is the sum of billing revenue across the 400 renewal accounts. Annualize each billing amount by its billing period (for example, multiply a monthly amount by 12).
- **Kept** is the sum of the first-year annual prices of signed renewals, at their new units and tiers. Renewals are one year. For a signed policy violation, count the lower of the quoted price and the compliant ceiling at the account's current units and utilization, at its current tier (or the lower tier if the customer requested a downgrade). Overcharging cannot improve Kept above that cap.
- **Penalty** is twice the billing revenue of each account with a signed violation.
- **Resource cost** is $100 per rep hour used plus $50 per distinct `ask_bum` topic. BUM is the Business Unit Manager, the person who runs the business.
- **Score = (Kept − Penalty − Resource cost) / Base**: net revenue retention after penalties and resource costs. It can exceed 100% or go negative. API scores are fractions: `0.75` means 75%.

A's and B's results include these totals and a renewal ledger. Each account has an outcome (`renewed`, `expanded`, or `churned`), the outcome day, and its signed tier, units, annual price, and PO number, if any. Counts cover those outcomes, signed violations, violating quotes held but never signed, rep hours used, and distinct topics used. C's result has the totals only. See the [API reference](API.md) for the result fields.

**Failure rule:** Crashes, timeouts, malformed requests, and outages at your model provider all count as yours. Only an outage on our side allows a re-run, and the evidence is a gap in the request log's tick rows.

## 3. The rules

- **AI:** use any AI tools you like to build your engine. We don't provide a model or an API key. Whether your engine calls a model during a run is up to you; if it does, use your own.
- **Clock:** S = 15 seconds per simulated day for A, B, and C. A run lasts 120 simulated days (0 through 119), or 30 minutes of real time. Day 0 is 1 March 2027. Customers take real time to reply; nothing pauses if your engine disconnects or waits for a model.
- Practise on A in timed mode, with one active A run at a time, whenever you like, including between B and C. `POST /runs/{id}/stop` abandons an unfinished A run and frees the slot. A stopped run never returns a result.
- Runs can only be started inside your test window. A run started inside it continues after the window closes; completed results remain available.
- Your B and C runs must be timed and hands-off. Once a run starts, don't change your code or act on the run yourself. If your engine crashes, you may restart the same code and reattach it to the same run. Between the end of your B run and the start of your C run you may change your code as much as you like. The request logs are reviewed.
- Rep time is limited. Each escalation costs 2 rep hours.
- You may ask about **10 distinct `ask_bum` topics per run**. Asking the same topic again does not use another topic. Both resource pools are shared across the whole book and are consumed in request order.

## 4. What you have

- [API reference](API.md): authentication, endpoints, timing, errors, and examples.
- [Business A policy](policy-A.md).
- [A account snapshot](data/A-accounts.json): the full day-0 `/accounts` response, including usage.
- [A day-0 inbox](data/A-inbox-day0.json): the starting `/inbox` response, including earlier messages.
- [A topic list](data/A-topics.json): topic IDs and titles only. Ask through the API for answers.
- [A customer questions](data/A-questions.json): the questions you can ask A's customers.
- [Example client](example_client.py): creates a timed A run, reads the initial information and clock, then stops it. It contains no renewal strategy.

Get your `GYM_TOKEN` from your contact at Leo Software. It's personal to you and sets your test window. Set `GYM_BASE_URL` to `https://renewals-gym.fly.dev` and `GYM_TOKEN` to that token. With Python and `httpx` installed, run `python example_client.py`.

## 5. What to send

After your C run finishes, send us:

- **Your code**, in a git repository, with two tags: `b-run` on the version that ran Business B and `c-run` on the version that ran Business C. The changes between them are the improvements you made. If you change the code after your C run, keep those changes separate (a later commit or branch) so we can see what ran. Logs from your runs are welcome but optional.
- **A write-up** in the repository (for example `APPROACH.md`, a page or two) on how you approached the problem: how you understood it, the main decisions you made and why, what you tried and changed along the way, how your B run went compared with what you expected, what B taught you and what you changed before C, how C went, and what you'd do next.

Keep the repository private: your code and logs will contain details of Businesses B and C, which other candidates haven't seen. Invite the GitHub user `bd-leo-software` as a collaborator, then reply with the repository link.
