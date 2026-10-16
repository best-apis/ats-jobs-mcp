"""MCP server exposing the ATS Jobs Feed Apify Actor as three tools. Needs APIFY_TOKEN (free Apify account)."""
import os
from datetime import date, timedelta

from apify_client import ApifyClient
from mcp.server.fastmcp import FastMCP

ACTOR = "best_apis/ats-jobs-feed"
mcp = FastMCP("ats-jobs")
MAX_COST = float(os.environ.get("ATS_JOBS_MAX_COST_USD", "1.0"))  # hard cap per tool call


def _run(run_input: dict, limit: int) -> list[dict]:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(
        run_input={**run_input, "maxItems": max(1, min(limit, 200))}, max_total_charge_usd=MAX_COST
    )
    return list(client.dataset(run.default_dataset_id).iterate_items())


@mcp.tool()
def search_jobs(keywords: list[str], country: str = "", remote_only: bool = False,
                seniority: str = "", posted_within_days: int = 14, limit: int = 25) -> list[dict]:
    """Search open jobs across Greenhouse, Lever, Ashby, SmartRecruiters, Recruitee and Personio career sites.
    country: ISO code or name (e.g. DE, Germany). seniority: intern|junior|mid|senior|lead|staff|principal|manager|director|executive."""
    inp = {"mode": "jobs", "searchKeywords": keywords, "postedWithinDays": posted_within_days, "descriptionMode": "none"}
    if country:
        inp["locations"] = [country]
    if remote_only:
        inp["workplace"] = ["remote"]
    if seniority:
        inp["seniority"] = [seniority]
    return _run(inp, limit)


@mcp.tool()
def new_jobs_since(days: int = 1, keywords: list[str] | None = None, country: str = "", limit: int = 50) -> list[dict]:
    """Jobs that opened in the last N days (daily changes feed), optionally filtered by keywords and country."""
    inp = {"mode": "changes", "changeTypes": ["new"], "changesSince": (date.today() - timedelta(days=days)).isoformat(), "descriptionMode": "none"}
    if keywords:
        inp["searchKeywords"] = keywords
    if country:
        inp["locations"] = [country]
    return _run(inp, limit)


@mcp.tool()
def company_hiring_signals(function: str = "", min_open_jobs: int = 5, limit: int = 25) -> list[dict]:
    """Companies with open roles, jobs posted in the last 7/30 days, remote share and top skills. function e.g. engineering, data, sales."""
    inp = {"mode": "companies", "minOpenJobs": min_open_jobs}
    if function:
        inp["functions"] = [function]
    rows = _run(inp, limit)
    return sorted(rows, key=lambda r: -(r.get("postedLast7d") or 0))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
