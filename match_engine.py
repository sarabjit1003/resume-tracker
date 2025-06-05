# match_engine.py

from difflib import SequenceMatcher
from resume_parser import extract_skills  

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

def clean_skills(skill_list):
    return [s.lower().strip() for s in skill_list]

def match_score(resume_text, jd_text):
    jd_skills = clean_skills(extract_skills(jd_text))
    resume_skills = clean_skills(extract_skills(resume_text))

    matched = []
    for jd_skill in jd_skills:
        for res_skill in resume_skills:
            if is_similar(jd_skill, res_skill):
                matched.append(jd_skill)
                break

    matched = list(set(matched))
    missing = [skill for skill in jd_skills if skill not in matched]

    if len(jd_skills) == 0:
        score = 0.0
    else:
        score = round(len(matched) / len(jd_skills) * 100, 2)

    return score, matched, missing
