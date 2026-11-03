# Renewals Gym

## 1. The job

Build a renewals engine that maximizes net revenue retention. Your engine reads business records and customer email, asks customers questions, prepares quotes, sends email, asks business questions, and escalates issues through an HTTP API.

**Your result is your one run on Business B. Business A is practice and is never scored.**

- **Business A is for building and practising.** Run it as often as you like. Each A run returns a per-account ledger you can learn from.
- **Business B is the test.** It is a completely different company:
  - a different product and unit of sale
  - different usage data
  - a different renewal policy, with different rules and prices
  - different customers

  You won't see any of it until your B run starts. Your engine has to discover B through the API and adapt on its own.
- **Assume nothing carries over from A except the API.** An engine tuned to A's rules and data will fail on B. Build a renewals engine, not a solution for A.
- **You get one B run.** It lasts 30 minutes, runs hands-off, and can't be redone. If you don't run B before your test window closes, you have no result, so leave at least an hour.

## 2. How you're scored

- **Base** is the sum of billing revenue across the 400 renewal accounts. Annualize monthly billing amounts by multiplying by 12.
- **Kept** is the sum of the first-year annual prices of signed renewals, at their new units and tiers. Renewals are one year. For a signed policy violation, count the lower of the quoted price and the compliant ceiling at the account's current units and utilization, at its current tier (or the lower tier if the customer requested a downgrade). Overcharging cannot improve Kept above that cap.
- **Penalty** is twice the billing revenue of each account with a signed violation.
- **Resource cost** is $100 per rep hour used plus $50 per distinct `ask_bum` topic. BUM is the Business Unit Manager, the person who runs the business.
- **Score = (Kept − Penalty − Resource cost) / Base**: net revenue retention after penalties and resource costs. It can exceed 100% or go negative. API scores are fractions: `0.75` means 75%.

A's result includes these totals and a renewal ledger. Each account has an outcome (`renewed`, `expanded`, or `churned`), the outcome day, and its signed tier, units, annual price, and PO number, if any. Counts cover those outcomes, signed violations, violating quotes held but never signed, rep hours used, and distinct topics used. B's result has the totals only. See the [API reference](API.md) for the result fields.

**Failure rule:** Crashes, timeouts, malformed requests, and outages at your model provider all count as yours. Only an outage on our side allows a re-run, and the evidence is a gap in the request log's tick rows.

## 3. The rules

- **AI:** use any AI tools you like to build your engine. We don't provide a model or an API key. Whether your engine calls a model during a run is up to you; if it does, use your own.
- **Clock:** S = 15 seconds per simulated day for A and B. A run lasts 120 simulated days (0 through 119), or 30 minutes of real time. Day 0 is 1 March 2027. Customers take real time to reply; nothing pauses if your engine disconnects or waits for a model.
- Practise on A in timed mode, with one active A run at a time. `POST /runs/{id}/stop` abandons an unfinished A run and frees the slot. A stopped run never returns a result.
- Runs can only be started inside your test window. A run started inside it continues after the window closes; completed results remain available.
- Your B run must be timed and hands-off. Do not steer your engine mid-run. The request log is reviewed.
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

After your B run finishes, send a link to your code for the debrief.
