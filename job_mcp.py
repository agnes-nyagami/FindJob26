import logging
from typing import List
from pathlib import Path
from mcp.server.fastmcp import FastMCP, tool
from jobspy import scrape_jobs
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jobspy_mcp")


# Create the MCP Server
mcp = FastMCP("jobspy_mcp")

def _normalize_company(name: str) -> str:
    return name.lower().strip() 


@tool()
def search_jobs(
    role: str,
    location: str,
    employers: List[str],
    results_wanted: int = 10,
) -> List[dict]:
    """
    Search for job openings using JobSpy.

    Parameters:
    - role: Job title or role (e.g. 'Data Scientist')
    - location: City/state string 
    - employers: List of employer names already verified as sponsors

    Returns:
    A list of job dicts with:
      - title
      - company
      - location
      - job_url
      - description
      - date_posted
    """

    if not location.strip():
        raise ValueError("Location must be provided (e.g. 'Austin, TX').")

    if not employers:
        raise ValueError("Employers list must be provided and non-empty.")

    logger.info(
        f"Searching jobs | role='{role}' | location='{location}' | employers={len(employers)}"
    )

    jobs_df = scrape_jobs(
        site_name=["indeed", "linkedin", "zip_recruiter"],
        search_term=role,
        location=location,
        results_wanted=results_wanted,
    )

    if jobs_df.empty:
        logger.info("No jobs returned from JobSpy.")
        return []

    # Normalize companies safely
    jobs_df = jobs_df.fillna("")
    jobs_df["company_norm"] = jobs_df["company"].astype(str).str.lower().str.strip()

    allowed = {_normalize_company(e) for e in employers}

    jobs_df = jobs_df[jobs_df["company_norm"].isin(allowed)]

    if jobs_df.empty:
        logger.info("No jobs matched sponsoring employers.")
        return []

    results = jobs_df[
        [
            "title",
            "company",
            "location",
            "job_url",
            "description",
            "date_posted",
        ]
    ].to_dict(orient="records")

    logger.info(f"Returning {len(results)} sponsored job openings.")
    return results
    
if __name__ == "__main__":
    mcp.run()