# life-ops

A human-gated life dashboard. One human. Many agents. Self-hosted.

Agents write work. You decide. The app never posts, buys, or cancels.

Five primitives only: **Project**, **Queue item**, **Human gate**, **Cost event**, **Routine**. Domain UIs (X, shopping, calendar, memes) are optional modules. Product contract: [`docs/life-ops.md`](docs/life-ops.md).

This repository is public and friend-forkable. It is **not** a multi-tenant SaaS.

## How this relates to `sethweiland/memes`

`sethweiland/memes` is the meme pipeline (Imgflip scrape, generation, video, RAG, Instagram). Until cutover, the live site [ops.sethweiland.com](https://ops.sethweiland.com) still runs from that repo on Fly app `meme-ops`.

This repo is the extracted life-ops shell: Home, Projects, Spend, X review, Grok Bot routines, Folders nav, tenant loader, S3 `ops/` store, calendar week + horizon. It keeps the same URL contracts (`/`, `/projects/`, `/spend/`, `/x/`, `/grok-bot/`) so Fly cutover later is a deploy-source change, not an IA rewrite.

`modules.memes` may stay in tenant YAML as a flag that hides or no-ops meme folder links. This app does **not** import or serve the meme pipeline. `/memes/` 404s here on purpose.

Private runtime data stays in S3 `ops/` (tenant, board, spend, calendar snapshot, queues). Do not commit `config/tenant.yaml` or `data/tech_spend.json`.

## Friend standup

1. Fork or clone this repo.
2. Copy the example tenant and put your bets in:

   ```bash
   cp config/tenant.example.yaml config/tenant.yaml
   ```

   Edit `human`, `site.domain`, `projects`, and optional `folders`. Leave `shared` / `unallocated` out. Leave `last_done` / `next_steps` null if you do not know them. `config/tenant.yaml` is gitignored. No secrets in YAML.

3. Optional secrets / env:

   ```bash
   cp .env.example .env
   ```

   A board + spend + empty calendar instance needs no provider keys. Optional S3 (same `ops/` layout the memes deploy already uses):

   ```
   MEME_ASSETS_BUCKET=your-private-bucket
   AWS_DEFAULT_REGION=us-east-1
   ```

   Optional calendar ICS: `CALENDAR_ICS_URL` in the environment, never in YAML.

4. Run locally:

   ```bash
   pip install -r requirements.txt
   python web/run.py
   # http://localhost:5050  → Home, then Projects
   ```

   Tests: `pytest`.

5. Optional Fly + Cloudflare Access: use `Dockerfile` / `fly.toml` and put Access in front of the hostname. Skip Access on localhost. The Flask app does not replace Access.

## Production cutover (not this PR)

Do **not** `fly deploy` this repo onto `meme-ops` or change Cloudflare until you intend to switch the live site.

When you are ready:

1. Confirm this app boots against the existing S3 bucket (`MEME_ASSETS_BUCKET`) and `ops/tenant.yaml` already used by meme-ops.
2. Deploy this repo to Fly app `meme-ops` (same `fly.toml` app name) so `ops.sethweiland.com` keeps its hostname and path contracts.
3. Leave Cloudflare Access as-is unless the hostname changes.
4. Keep `sethweiland/memes` as the meme pipeline. Point meme-specific work there; do not re-import it here.

Until then, production stays on memes.
