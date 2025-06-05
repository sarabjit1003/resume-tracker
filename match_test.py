from resume_parser import parse_all_resumes
from job_matcher import match_resume_to_jobdesc

job_description = """
We are looking for a candidate skilled in Python, SQL, communication, and Power BI. 
Experience with data analysis and teamwork is a plus.
"""

resumes = parse_all_resumes("resumes")

for name, content in resumes.items():
    print(f"\n--- {name} ---")
    result = match_resume_to_jobdesc(content, job_description)
    print("Matched Skills:", result['matched_skills'])
    print("Match Score:", result['match_score'], "%")
