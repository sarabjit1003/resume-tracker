from pdfminer.high_level import extract_text
import os
import re #  regular expression module

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfminer.six."""
    try:
        return extract_text(pdf_path)
    except Exception as e:
       
        print(f"Error reading PDF {pdf_path}: {e}")
        return "" # Return an empty string if text extraction fails

def extract_skills(text):
    """
    Extracts skills from the given text using predefined patterns.
    Converts text to lowercase and uses regex for flexible matching.
    """
    text_lower = text.lower() # Convert entire text to lowercase once

    # Define  dictionary of skills using regex patterns.
   
    # The values are regex patterns to match that skill in various forms.
    skill_patterns = {
        # Marketing Skills 
        "digital marketing": r"\b(digital\s*marketing|online\s*marketing|internet\s*marketing|digi\s*marketing)\b",
        "canva": r"\b(canva)\b",
        "content creation": r"\b(content\s*creation|content\s*development|content\s*strategy|content\s*writing|copywriting|blogging|article\s*writing)\b",
        "google analytics": r"\b(google\s*analytics|ga(\b|\s*(basic|advanced))?|google\s*ana(?:lytics)?)\b",
        "instagram ads": r"\b(instagram\s*ads|insta\s*ads|ig\s*ads)\b",
        "creativity": r"\b(creativity|creative|innovative|ideation|design\s*thinking)\b",
        "seo basics": r"\b(seo\s*basics|basic\s*seo)\b",
        "seo": r"\b(seo|search\s*engine\s*optimization|on-page\s*seo|off-page\s*seo)\b",
        "social media strategy": r"\b(social\s*media\s*strategy|social\s*media\s*marketing|smm|social\s*networks)\b",
        "google sheets": r"\b(google\s*sheets|g\s*sheets|sheets|spreadsheets)\b",
        "campaign planning": r"\b(campaign\s*planning|marketing\s*campaigns|campaign\s*management|ad\s*campaigns)\b",
        "communication": r"\b(communication|communicator|interpersonal\s*skills|written\s*communication|verbal\s*communication)\b",
        "meta ads manager": r"\b(meta\s*ads\s*manager|facebook\s*ads|fb\s*ads|instagram\s*ads)\b",
        "content writing": r"\b(content\s*writing|copywriting|article\s*writing|blog\s*writing)\b",
        "ms excel": r"\b(ms\s*excel|excel|microsoft\s*excel|spreadsheets)\b",
        "analytics": r"\b(analytics|data\s*analytics)\b",
        "research": r"\b(research|market\s*research)\b",
        "branding": r"\b(brand\s*management|branding)\b",
        "public relations": r"\b(public\s*relations|pr)\b",

        # HR Skills 
        "recruitment coordination": r"\b(recruitment\s*coordination|recruiting\s*coordinator)\b",
        "hrms": r"\b(hrms|human\s*resources\s*management\s*system)\b",
        "verbal communication": r"\b(verbal\s*communication|oral\s*communication)\b",
        "written communication": r"\b(written\s*communication)\b",
        "ms office": r"\b(ms\s*office|microsoft\s*office|word|powerpoint)\b", 
        "excel pivot tables": r"\b(pivot\s*tables|excel\s*pivot\s*tables)\b",
        "vlookup": r"\b(vlookup)\b",
        "hr tools": r"\b(hr\s*tools)\b",
        "darwinbox": r"\b(darwinbox)\b",
        "sap": r"\b(sap)\b",
        "empathy": r"\b(empathy|empathetic)\b",
        "teamwork": r"\b(teamwork|team\s*player|collaboration|collaborative)\b",
        "organizational skills": r"\b(organizational\s*skills|organization)\b",
        "recruitment & selection": r"\b(recruitment\s*&\s*selection|recruitment\s*and\s*selection|talent\s*acquisition)\b",
        "payroll basics": r"\b(payroll\s*basics|basic\s*payroll)\b",
        "employee engagement activities": r"\b(employee\s*engagement\s*activities|employee\s*engagement)\b",
        "ms word": r"\b(ms\s*word|microsoft\s*word|word)\b",
        "hrms software": r"\b(hrms\s*software)\b",
        "resume screening": r"\b(resume\s*screening|cv\s*screening)\b",
        "employee engagement": r"\b(employee\s*engagement)\b",
        "interview scheduling": r"\b(interview\s*scheduling|schedule\s*interviews)\b",
        "zoho people": r"\b(zoho\s*people)\b",

        # Fresher Skills 
        "python": r"\b(python|basic\s*python)\b",
        "sql basic": r"\b(sql\s*basic|basic\s*sql)\b",
        "html": r"\b(html)\b",
        "css": r"\b(css)\b",
        "time management": r"\b(time\s*management)\b",
        "analytical thinking": r"\b(analytical\s*thinking|analytical\s*skills|analytically)\b",
        "presentation skills": r"\b(presentation\s*skills|presenting)\b",
        "powerpoint": r"\b(powerpoint)\b",
        "willingness to learn": r"\b(willingness\s*to\s*learn|eager\s*to\s*learn|fast\s*learner)\b",
        "java": r"\b(java)\b",
        "adaptability": r"\b(adaptability|adaptable)\b",
        "ms office suite": r"\b(ms\s*office\s*suite|microsoft\s*office\s*suite|ms\s*office)\b", 
        "problem-solving": r"\b(problem\s*solving|problem-solving|troubleshooting)\b",
        
       
        'leadership': r"\b(leadership|leader|lead)\b",
        'project management': r"\b(project\s*management|pmp|agile|scrum)\b",
        'data analysis': r"\b(data\s*analysis|data\s*analyst|analyzing\s*data)\b",
        'machine learning': r"\b(machine\s*learning|ml)\b",
        'public speaking': r"\b(public\s*speaking|presentations)\b",
        'teaching': r"\b(teaching|mentor)\b",
        'power bi': r"\b(power\s*bi)\b",
        'tableau': r"\b(tableau)\b",
        'numpy': r"\b(numpy)\b",
        'pandas': r"\b(pandas)\b",
        'customer service': r"\b(customer\s*service|client\s*service)\b", 
        'data entry': r"\b(data\s*entry)\b",
        'report writing': r"\b(report\s*writing|report\s*generation)\b",
        'critical thinking': r"\b(critical\s*thinking)\b",
        'attention to detail': r"\b(attention\s*to\s*detail|detail-oriented)\b"
    }

    found_skills = set() # Use a set to avoid duplicate skills and ensure uniqueness
    for skill_name, pattern in skill_patterns.items():
        # search for the pattern in the lowercase text
        if re.search(pattern, text_lower):
            found_skills.add(skill_name)
    
    return list(found_skills)
