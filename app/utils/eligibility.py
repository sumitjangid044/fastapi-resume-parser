from typing import Dict, List

ROLE_RULES: Dict[str, Dict] = {
    "java_developer": {
        "must_have_any": [["java"], ["spring","spring boot"], ["hibernate"]],
        "min_years": 1.0,
    },
    "python_developer": {
        "must_have_any": [["python"], ["fastapi","django","flask"]],
        "min_years": 1.0,
    },
    "full_stack_developer": {
        "must_have_any": [["javascript","typescript"], ["react"], ["node","express"], ["sql","mysql","postgresql","sqlite"]],
        "min_years": 2.0,
    },
    "frontend_developer": {
        "must_have_any": [["javascript","typescript"], ["react","next.js"], ["html"], ["css","tailwind"]],
        "min_years": 1.0,
    },
    "ai_ml_engineer": {
        "must_have_any": [["python"], ["pandas","numpy"], ["scikit-learn","tensorflow","pytorch"]],
        "min_years": 1.0,
    },
    "app_developer": {
        "must_have_any": [["android","kotlin"], ["swift"], ["react native","flutter"]],
        "min_years": 1.0,
    },
    "data_analyst": {
        "must_have_any": [["python"], ["pandas","numpy"], ["sql","mysql","postgresql","sqlite"]],
        "min_years": 0.5,
    },
}

def check_eligibility(skills, years_experience, target_role):
    role_skills = {
        "java_developer": ["java", "spring", "hibernate"],
        "python_developer": ["python", "django", "flask"],
        "full_stack_developer": ["javascript", "react", "node", "html", "css"],
        "frontend_developer": ["javascript", "react", "html", "css"],
        "ai_ml_engineer": ["python", "machine learning", "tensorflow", "pytorch"],
        "app_developer": ["android", "kotlin", "java", "flutter"],
        "data_analyst": ["sql", "excel", "powerbi", "python"]
    }

    required_skills = role_skills.get(target_role, [])
    matching_skills = [skill for skill in skills if skill.lower() in required_skills]

    # ✅ Freshers allowed (years_experience is None or 0)
    if matching_skills:
        return True  # Eligible even if fresher
    return False

