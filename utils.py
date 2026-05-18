import json
from collections import Counter
from typing import Optional
import numpy as np
import pandas as pd
import os

def calculate_revenue(price: float, quantity: int, discount_pct: float = 0) -> float:
    """
    Returns the final revenue after applying discount.
    Formula: price * quantity * (1 - discount_pct / 100)
    Default discount is 0%.
    """
    return price * quantity * (1 - discount_pct / 100)


def classify_customer(age: Optional[int]) -> str:
    """
    Returns customer segment as a string:
    - age < 25     → "Youth"
    - 25 <= age < 45 → "Adult"
    - age >= 45    → "Senior"
    - age is None  → "Unknown"
    Use type hints in your function signature.
    """
    if age is None:
        return "Unknown"
    elif age < 25:
        return "Youth"
    elif age < 45:
        return "Adult"
    else:
        return "Senior"


def is_valid_email(email: str) -> bool: 
    """
    Returns True if email contains '@' and '.', else False.
    """
    return '@' in email and '.' in email


def load_config(filepath: str) -> dict:
    """
    Reads a JSON file and returns it as a Python dictionary.
    Use a context manager (with block).
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def write_summary_report(stats: dict, output_path: str) -> None:
    """
    Writes a plain-text summary report to the given file path.
    Each key-value pair in stats should be on its own line.
    Format: "Key: Value"
    Use a context manager (with block).
    """
    with open(output_path, 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")


print("Utils module loaded successfully.")
print("calculate_revenue(100, 5, 10):", calculate_revenue(100, 5, 10))
print("classify_customer(30):", classify_customer(30))
print("classify_customer(None):", classify_customer(None))
print("is_valid_email('a@b.com'):", is_valid_email('a@b.com'))
print("is_valid_email('invalid-email'):", is_valid_email('invalid-email'))



'''
Then write a small test block at the bottom of utils.py (inside if __name__ == "__main__":) that:

Loads the config using your load_config() function
Prints the project_name and tax_rate
Calls calculate_revenue(1200, 3, 10) and prints the result
Calls classify_customer(None) and prints the result

'''


if __name__ == "__main__":
    config = load_config("config.json")
    print("Project Name:", config.get('project_name'))
    print("Tax Rate:", config.get('tax_rate'))

    revenue = calculate_revenue(1200, 3, 10)
    print("Calculated Revenue:", revenue)

    customer_segment = classify_customer(None)
    print("Customer Segment for None age:", customer_segment)





