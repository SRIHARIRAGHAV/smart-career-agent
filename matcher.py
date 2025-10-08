# recommender/matcher.py
from pathlib import Path
from collections import defaultdict
from .data_loader import load_job_roles  # relative import; adjust if needed
import math

def normalize_skill(s):
    return s.strip().lower()

def score_role(role_skills, user_skills):
    """
    role_skills: list of role-required skills (strings)
    user_skills: list of user skills (strings)
    Returns: dict with match_count, role_skill_count, match_ratio (0-1), score (0-100)
    """
    role_set = {normalize_skill(s) for s in role_skills}
    user_set = {normalize_skill(s) for s in user_skills}

    matched = role_set & user_set
    match_count = len(matched)
    role_count = len(role_set) if role_set else 1

    # match_ratio: proportion of role skills the user has
    match_ratio = match_count / role_count

    # Score heuristic: weighted by match_ratio and absolute matches (gives advantage to closer fits)
    score = (0.7 * match_ratio + 0.3 * (match_count / (match_count + 3))) * 100
    score = round(score, 1)

    return {
        "matched_skills": sorted(matched),
        "match_count": match_count,
        "role_skill_count": role_count,
        "match_ratio": round(match_ratio, 3),
        "score": score
    }

def recommend_roles(user_skills, top_k=5, min_score=15, json_path="data/job_roles.json"):
    """
    user_skills: list of strings (extracted from resume)
    top_k: number of top recommendations to return
    min_score: filter out roles with score below this threshold
    json_path: path to job_roles.json (used by load_job_roles)
    """
    # Basic sanitization
    if not user_skills:
        return []

    # Load roles
    roles = load_job_roles(json_path)

    scored = []
    for r in roles:
        role_skills = r.get("skills") or r.get("required_skills") or r.get("required_skills_list") or r.get("required_skills", [])
        # ensure list
        if isinstance(role_skills, str):
            role_skills = [s.strip() for s in role_skills.split(",") if s.strip()]

        s = score_role(role_skills, user_skills)
        # attach metadata
        scored.append({
            "title": r.get("role") or r.get("title") or r.get("name") or "Unknown Role",
            "description": r.get("description", ""),
            "required_skills": role_skills,
            "matched_skills": s["matched_skills"],
            "match_count": s["match_count"],
            "role_skill_count": s["role_skill_count"],
            "match_ratio": s["match_ratio"],
            "score": s["score"],
            "recommended_courses": r.get("recommended_courses", [])
        })

    # Filter and sort
    filtered = [r for r in scored if r["score"] >= min_score]
    filtered.sort(key=lambda x: (x["score"], x["match_count"], x["match_ratio"]), reverse=True)

    # Return top_k
    return filtered[:top_k]

if __name__ == "__main__":
    # quick manual test
    example_user_skills = ["Python", "Pandas", "SQL", "Docker", "Git"]
    recs = recommend_roles(example_user_skills, top_k=5, json_path="data/job_roles.json")
    import json
    print(json.dumps(recs, indent=2))
