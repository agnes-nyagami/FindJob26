from pathlib import Path
import sqlite3
import csv

BASE_DIR = Path(__file__).resolve().parent   

CSV_PATH = BASE_DIR / "H1B_2020_2023_summary.csv"
DB_PATH = BASE_DIR / "sponsorship.db"
TABLE_NAME = "sponsors"              

def csv_to_sqlite():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Drop old table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")

    # Create table
    cursor.execute(f"""
        CREATE TABLE {TABLE_NAME} (
            employer TEXT,
            total_approvals INTEGER,
            city TEXT,
            state TEXT,
            zip TEXT
        );
    """)

    # Open CSV and insert rows
    with open(CSV_PATH, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [
            (
                row["Employer"],
                int(row["total_approvals"]),
                row["cities"],
                row["states"],
                row["zip_codes"]
            )
            for row in reader
        ]

    cursor.executemany(
        f"INSERT INTO {TABLE_NAME} (employer, total_approvals, city, state, zip) VALUES (?, ?, ?, ?, ?)",
        rows
    )

    # Indexes for FAST queries
    cursor.execute(f"CREATE INDEX idx_state ON {TABLE_NAME}(state);")
    cursor.execute(f"CREATE INDEX idx_employer ON {TABLE_NAME}(employer);")

    conn.commit()
    conn.close()

    print("CSV successfully imported into SQLite!")


if __name__ == "__main__":
    csv_to_sqlite()
