# Load job roles and skill data
import json
import pandas as pd
from pathlib import Path

def load_job_roles(json_path="data/job_roles.json"):
    """
    Load job roles and required skills from a JSON file.
    Example JSON format:
    [
        {"role": "Data Scientist", "skills": ["python", "machine learning", "statistics"]},
        {"role": "DevOps Engineer", "skills": ["docker", "aws", "ci/cd", "kubernetes"]}
    ]
    """
    file = Path(json_path)
    if not file.exists():
        raise FileNotFoundError(f"{json_path} not found. Please create the dataset.")
    
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_job_roles_csv(csv_path="data/job_roles.csv"):
    """
    Load job roles and required skills from a CSV file.
    Example CSV format:
    role,skills
    Data Scientist,"python, machine learning, statistics"
    DevOps Engineer,"docker, aws, ci/cd, kubernetes"
    """
    file = Path(csv_path)
    if not file.exists():
        raise FileNotFoundError(f"{csv_path} not found. Please create the dataset.")

    df = pd.read_csv(file)
    jobs = []
    for _, row in df.iterrows():
        skills = [s.strip().lower() for s in row["skills"].split(",")]
        jobs.append({"role": row["role"], "skills": skills})
    return jobs


if __name__ == "__main__":
    # Example usage
    try:
        roles = load_job_roles()
        print("Loaded from JSON:", roles)
    except Exception as e:
        print("JSON loader error:", e)

    try:
        roles_csv = load_job_roles_csv()
        print("Loaded from CSV:", roles_csv)
    except Exception as e:
        print("CSV loader error:", e)
