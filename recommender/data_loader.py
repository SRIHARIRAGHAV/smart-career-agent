# data_loader.py
import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

BASE_DIR = Path(__file__).parent  # ensures paths are relative to this script
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # create data dir for dev convenience

SAMPLE_JSON = [
    {"role": "Data Scientist", "skills": ["python", "machine learning", "statistics"]},
    {"role": "DevOps Engineer", "skills": ["docker", "aws", "ci/cd", "kubernetes"]}
]

def _write_sample_files():
    """Create sample JSON and CSV if none exist (safe for dev)."""
    json_path = DATA_DIR / "job_title_des.json"
    csv_path = DATA_DIR / "job_title_des.csv"
    if not json_path.exists():
        json_path.write_text(json.dumps(SAMPLE_JSON, indent=2), encoding="utf-8")
    if not csv_path.exists():
        df = pd.DataFrame({
            "role": [r["role"] for r in SAMPLE_JSON],
            "skills": [", ".join(r["skills"]) for r in SAMPLE_JSON]
        })
        df.to_csv(csv_path, index=False, encoding="utf-8")

def load_job_roles(json_path: str = None) -> List[Dict[str, Any]]:
    """
    Load job roles from JSON. Path is resolved relative to this file by default.
    """
    if json_path is None:
        json_path = str(DATA_DIR / "job_title_des.json")
    file = Path(json_path)
    if not file.exists():
        raise FileNotFoundError(f"JSON file not found at: {file.resolve()}")
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        # basic validation
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of {role, skills} objects.")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file}: {e}")

def load_job_roles_csv(csv_path: str = None) -> List[Dict[str, Any]]:
    """
    Load job roles from CSV. Columns expected: role, skills
    Skills column can be comma-separated string.
    """
    if csv_path is None:
        csv_path = str(DATA_DIR / "job_title_des.csv")
    file = Path(csv_path)
    if not file.exists():
        raise FileNotFoundError(f"CSV file not found at: {file.resolve()}")
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise ValueError(f"Failed to read CSV {file}: {e}")

    if "role" not in df.columns or "skills" not in df.columns:
        raise ValueError(f"CSV must contain 'role' and 'skills' columns. Found: {list(df.columns)}")

    jobs = []
    for i, row in df.iterrows():
        role = str(row["role"]).strip()
        raw_skills = row.get("skills", "")
        if pd.isna(raw_skills):
            skills = []
        else:
            # allow ; or , as delimiter
            sep = ";" if ";" in str(raw_skills) and "," not in str(raw_skills) else ","
            skills = [s.strip().lower() for s in str(raw_skills).split(sep) if s.strip()]
        jobs.append({"role": role, "skills": skills})
    return jobs

if __name__ == "__main__":
    # For convenience, if no data files exist, write sample ones.
    _write_sample_files()

    # Test loaders
    try:
        roles = load_job_roles()
        print("Loaded JSON:", roles)
    except Exception as e:
        print("JSON loader error:", e)

    try:
        roles_csv = load_job_roles_csv()
        print("Loaded CSV:", roles_csv)
    except Exception as e:
        print("CSV loader error:", e)
