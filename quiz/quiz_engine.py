# Quiz logic here
def get_quiz_questions():
    return [
        {
            "question": "Do you enjoy working with numbers and data?",
            "field": "Data Science"
        },
        {
            "question": "Do you like designing user interfaces?",
            "field": "Frontend Development"
        },
        {
            "question": "Do you enjoy automating infrastructure and deployments?",
            "field": "DevOps"
        },
        {
            "question": "Do you enjoy creating mobile applications?",
            "field": "App Development"
        }
    ]

def evaluate_answers(answers):
    from collections import Counter
    counter = Counter(answers)
    recommended_field = counter.most_common(1)[0][0]
    return recommended_field
