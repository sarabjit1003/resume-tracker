from resume_parser import parse_all_resumes, extract_skills

def match_score(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched = resume_skills.intersection(jd_skills)
    match_score = round((len(matched) / len(jd_skills)) * 100, 2) if jd_skills else 0

    return {
        "resume_skills": list(resume_skills),
        "jd_skills": list(jd_skills),
        "matched_skills": list(matched),
        "match_score": match_score
    }
