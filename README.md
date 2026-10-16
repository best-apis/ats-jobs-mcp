# ats-jobs-mcp

MCP server that gives an AI agent a daily-refreshed index of **350k+ open jobs from 12,000+ company career sites** (Greenhouse, Lever, Ashby, SmartRecruiters, Recruitee, Personio). It calls the [ATS Jobs Feed](https://apify.com/best_apis/ats-jobs-feed) Apify Actor (pay per result, hard cost cap per call).

[![Run on Apify](https://apify.com/actor-badge?actor=best_apis/ats-jobs-feed)](https://apify.com/best_apis/ats-jobs-feed)

## Tools
- `search_jobs(keywords, country, remote_only, seniority, posted_within_days, limit)`
- `new_jobs_since(days, keywords, country, limit)`: what opened since yesterday
- `company_hiring_signals(function, min_open_jobs, limit)`: who is hiring most this week

## Install
```bash
# run directly from GitHub (no PyPI package is published yet)
uvx --from git+https://github.com/best-apis/ats-jobs-mcp ats-jobs-mcp
# or: pip install git+https://github.com/best-apis/ats-jobs-mcp
```
Claude Desktop / Cursor config:
```json
{ "mcpServers": { "ats-jobs": { "command": "uvx", "args": ["--from", "git+https://github.com/best-apis/ats-jobs-mcp", "ats-jobs-mcp"], "env": { "APIFY_TOKEN": "<your token>" } } } }
```
Get a token from a free Apify account (Settings, API & integrations). `ATS_JOBS_MAX_COST_USD` (default 1.0) caps spend per tool call.

Note: the `ats-jobs-mcp` name on PyPI belongs to an unrelated project, so install from this repo as shown above.

Prefer no local install? Use the hosted Apify MCP server: `https://mcp.apify.com?tools=best_apis/ats-jobs-feed`.

MIT licensed. Data: public job-board endpoints; employers can request removal via the Actor's Issues tab.
