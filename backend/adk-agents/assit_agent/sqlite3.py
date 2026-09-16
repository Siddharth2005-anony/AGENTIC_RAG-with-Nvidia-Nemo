# agent/tools.py

import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "company.db"
)


def query_sqlite(question: str) -> dict:
    """
    Retrieve structured business data from SQLite.

    Use this tool for:
    - Revenue
    - Expenses
    - Profit
    - Financial quarters

    Args:
        question: User's question about financial data.

    Returns:
        Financial data retrieved from SQLite.
    """

    question_lower = question.lower()

    if "revenue" in question_lower:
        metric = "revenue"

    elif "expense" in question_lower:
        metric = "expenses"

    elif "profit" in question_lower:
        metric = "profit"

    else:
        return {
            "status": "error",
            "message": "Unsupported financial metric."
        }

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = f"""
            SELECT quarter, {metric}
            FROM financials
            ORDER BY quarter;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        return {
            "status": "success",
            "metric": metric,
            "data": [
                {
                    "quarter": row[0],
                    "value": row[1]
                }
                for row in rows
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }