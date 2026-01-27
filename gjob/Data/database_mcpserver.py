from pathlib import Path
from mcp.server.fastmcp import FastMCP
from crewai.tools import tool
import sqlite3
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sponsorship.db"

mcp = FastMCP("sponsorship-db")

@tool
def find_sponsors(state: str, city: str | None = None) -> str:
    """
    Query H1B sponsors filtered by US state.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT employer, total_approvals, city, state, zip
        FROM sponsors
        WHERE state = ? AND LOWER(city) LIKE ?;
    """

    cursor.execute(query, (state.upper(), f"%{city.lower()}%"))
    rows = cursor.fetchall()

    conn.close()

    result = [
        {
            "employer": r[0],
            "total_approvals": r[1],
            "city": r[2],
            "state": r[3],
            "zip": r[4],
        }
        for r in rows
    ]

    return json.dumps(result)

if __name__ == "__main__":
    mcp.run()

