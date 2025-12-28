

from config import MATCH_CONFIG


def match_internships(student, internships):
    recommendations = []

    for internship in internships:
        total_score = 0
        matched_skills = []
        score_breakdown = {
            "skills": 0,
            "interest": 0,
            "location": 0,
            "remote": 0
        }

        
        for skill in student["skills"]:
            if skill in internship["required_skills"]:
                matched_skills.append(skill)

        skill_score = len(matched_skills) * MATCH_CONFIG["SKILL_WEIGHT"]
        if skill_score > MATCH_CONFIG["MAX_SKILL_SCORE"]:
            skill_score = MATCH_CONFIG["MAX_SKILL_SCORE"]

        score_breakdown["skills"] = skill_score
        total_score += skill_score

        
        title_words = internship["title"].lower().split()
        if any(word in student["interests"] for word in title_words):
            total_score += MATCH_CONFIG["INTEREST_SCORE"]
            score_breakdown["interest"] = MATCH_CONFIG["INTEREST_SCORE"]

        
        if student["preferred_location"] == internship["location"]:
            total_score += MATCH_CONFIG["LOCATION_SCORE"]
            score_breakdown["location"] = MATCH_CONFIG["LOCATION_SCORE"]


        if internship["mode"] == "remote":
            total_score += MATCH_CONFIG["REMOTE_BONUS"]
            score_breakdown["remote"] = MATCH_CONFIG["REMOTE_BONUS"]

        
        if total_score < MATCH_CONFIG["MIN_SCORE_TO_RECOMMEND"]:
            continue

        recommendations.append({
            "internship": internship,
            "total_score": total_score,
            "matched_skills": matched_skills,
            "score_breakdown": score_breakdown
        })


    recommendations.sort(key=lambda x: x["total_score"], reverse=True)
    return recommendations
