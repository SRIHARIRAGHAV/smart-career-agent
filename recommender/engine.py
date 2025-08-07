# Recommendation engine logic here
import json

def load_job_roles(path='smart-career-agent/data/job_roles.json'):
    with open(path, 'r') as file:
        return json.load(file)

def recommend_roles(user_skills, interest_field):
    roles = load_job_roles()
    recommendations = []
    for role in roles:
        match_count = len(set(role['required_skills']) & set(user_skills))
        if role['title'] == interest_field or match_count >= 2:
            recommendations.append({
                "title": role['title'],
                "match_count": match_count,
                "recommended_courses": role['recommended_courses']
            })
    return recommendations
