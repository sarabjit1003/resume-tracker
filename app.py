import streamlit as st
import pandas as pd
import os
import time
import random
from resume_parser import extract_text_from_pdf, extract_skills # Ensure these are correct

st.set_page_config(page_title="Resume Screening Tool", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
        .main { background-color: #fdf6f0; background-image: url('https://www.transparenttextures.com/patterns/white-wall.png'); }
        .stButton>button { background-color: #FF6F61; color: white; font-weight: bold; border-radius: 10px; }
        .stProgress>div>div>div>div { background-color: #FF6F61 !important; }
        .thought-box { background-color: #fff8f0; padding: 10px; border-left: 5px solid #FF6F61; margin-bottom: 20px; font-style: italic; color: #333; }
        .shortlist-table { background-color: #fff8f0; padding: 10px; border-radius: 10px; }
        .small-chart canvas { max-height: 300px; }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 AI Resume Screener & Smart Match Tool")

# Thought of the day (button-based reveal)
thoughts = [
    "Small progress is still progress!",
    "You’re doing amazing, keep going!",
    "HR heroes deserve coffee too ☕",
    "Hiring is tough, you’re tougher!",
    "Even Batman had a team. Don’t stress."
]
if st.button("💭 Click to see today's thought"):
    st.markdown(f"<div class='thought-box'>💡 {random.choice(thoughts)}</div>", unsafe_allow_html=True)

# Timer section
if "start_time" not in st.session_state:
    st.session_state.start_time = None
    st.session_state.elapsed = 0

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("▶️ Start Timer", key="start_timer"):
        st.session_state.start_time = time.time()
        st.success("⏱️ Timer started!")

with col2:
    if st.button("⏹️ Stop Timer", key="stop_timer"):
        if st.session_state.start_time:
            st.session_state.elapsed = time.time() - st.session_state.start_time
            st.session_state.start_time = None
            congrats = random.choice(["🎉 Great work!", "👏 You did it!", "🌟 Proud of your focus!", "✅ Task complete, well done!"])
            st.info(f"⏳ Time Elapsed: {round(st.session_state.elapsed)} seconds\n{congrats}")

if st.session_state.start_time:
    st.caption(f"🕒 Time Running: {round(time.time() - st.session_state.start_time)} seconds")

# ---
# Skill Definitions for various roles
# This dictionary provides a list of suggested skills for each role in the multiselect filter.
# All skills here should be in lowercase for consistent display and matching.

ROLE_SPECIFIC_SKILLS = {
    "data_analyst": [
        "sql", "python", "r", "excel", "tableau", "power bi", "statistical analysis",
        "data visualization", "data cleaning", "machine learning basics", "big data",
        "storytelling", "communication", "problem-solving"
    ],
    "marketing": [
        "digital marketing", "canva", "content creation", "google analytics",
        "instagram ads", "creativity", "seo basics", "social media strategy",
        "google sheets", "campaign planning", "communication", "meta ads manager",
        "seo", "content writing", "ms excel", "analytics", "research", "branding", "public relations"
    ],
    "hr": [ # Based on your provided HR resume skills
        "recruitment coordination", "ms excel", "hrms", "verbal communication", "written communication",
        "ms office", "excel pivot tables", "vlookup", "hr tools", "darwinbox", "sap",
        "empathy", "teamwork", "organizational skills", "recruitment & selection", "payroll basics",
        "employee engagement activities", "ms word", "hrms software", "resume screening",
        "employee engagement", "interview scheduling", "zoho people"
    ],
    "fresher": [ # Based on your provided Fresher resume skills
        "python", "sql basic", "ms excel", "google sheets", "communication", "time management",
        "analytical thinking", "presentation skills", "ms word", "powerpoint",
        "willingness to learn", "java", "html", "css", "creativity", "problem-solving",
        "adaptability", "basic python", "ms office suite"
    ]
    # Add more roles and their associated skills here
}


# Upload JD
jd_file = st.file_uploader("📄 Upload Job Description (TXT file or multiple paragraphs)", type="txt")

if jd_file:
    jd_text = jd_file.read().decode("utf-8")
    st.subheader("📌 Job Description Preview")
    st.text_area("Job Description Text", value=jd_text[:1000] + ("..." if len(jd_text) > 1000 else ""), height=150)
    st.markdown("---")

    st.subheader("📂 Choose Job Role")
    # Dynamically find role folders within the 'resumes' directory
    role_folders = [f for f in os.listdir("resumes") if os.path.isdir(os.path.join("resumes", f))]

    if not role_folders:
        st.error("❗ No role folders found inside 'resumes/'. Add PDFs inside folders like 'data_analyst', 'hr', etc.")
    else:
        selected_role = st.selectbox("Choose a role folder:", role_folders)
        resume_folder_path = os.path.join("resumes", selected_role)

        st.subheader("🎯 Filters")
        min_score = st.slider("Minimum Match Score (%)", 0, 100, 0)

        # Get all skills from resumes in the selected folder AND add role-specific skills from our dictionary
        all_available_skills = set()
        # First, add skills that are explicitly defined for the selected role
        if selected_role in ROLE_SPECIFIC_SKILLS:
            all_available_skills.update(ROLE_SPECIFIC_SKILLS[selected_role])
        
        # Then, iterate through resumes in the selected folder to find any additional skills
        # that might be present but not explicitly listed in ROLE_SPECIFIC_SKILLS
        for resume_file in os.listdir(resume_folder_path):
            if resume_file.endswith(".pdf"):
                resume_text_temp = extract_text_from_pdf(os.path.join(resume_folder_path, resume_file))
                # Pass the extracted text to extract_skills, which now handles lowercasing internally
                resume_skills_temp = extract_skills(resume_text_temp) 
                all_available_skills.update([skill.lower() for skill in resume_skills_temp]) # Ensure added skills are lowercase

        # Convert to list and sort for display in multiselect
        sorted_all_available_skills = sorted(list(all_available_skills))

        selected_skills = st.multiselect("🔍 Filter resumes by skills:", sorted_all_available_skills)
        searched_skills = [s.lower() for s in selected_skills] # Ensure these are also lowercased for comparison

        st.subheader("📊 Resume Match Results")
        results = []
        # Initialize session state for shortlisted candidates and feedback if not present
        if "shortlisted" not in st.session_state:
            st.session_state.shortlisted = []
        if "feedback" not in st.session_state:
            st.session_state.feedback = {}


        if searched_skills: # Only proceed if skills are selected
            for resume_file in os.listdir(resume_folder_path):
                if resume_file.endswith(".pdf"): # Ensure we only process PDF files
                    resume_path = os.path.join(resume_folder_path, resume_file)
                    resume_text = extract_text_from_pdf(resume_path)
                    
                    # --- DEBUGGING LINE: OBSERVE THIS OUTPUT CAREFULLY ---
                    # Ensure resume_text is not empty from a failed extraction before passing to extract_skills
                    if resume_text: 
                        extracted_skills_for_debug = extract_skills(resume_text) # extract_skills now returns lowercase
                        st.write(f"**{resume_file}:** Extracted skills: {', '.join(extracted_skills_for_debug)}")
                    else:
                        extracted_skills_for_debug = []
                        st.warning(f"Could not extract text from {resume_file}. Skipping skill extraction.")
                    # --- END DEBUGGING LINE ---

                    # Use the extracted skills for matching (they are already lowercase from extract_skills)
                    resume_skills_lower = extracted_skills_for_debug 

                    matched = [skill for skill in searched_skills if skill in resume_skills_lower]
                    missing = [skill for skill in searched_skills if skill not in resume_skills_lower]
                    
                    # Clean the matched/missing lists to remove empty strings or very short strings if any
                    matched_clean = [s for s in matched if s.strip() and len(s) > 1]
                    missing_clean = [s for s in missing if s.strip() and len(s) > 1]

                    # Calculate score only if there are skills to search for
                    if searched_skills:
                        score = int(len(matched_clean) / len(searched_skills) * 100)
                    else:
                        score = 0 # If no skills are selected, score is 0

                    if score >= min_score:
                        results.append({
                            "Resume": resume_file,
                            "Score (%)": score,
                            "Matched Skills": ', '.join(matched_clean),
                            "Missing Skills": ', '.join(missing_clean),
                            "Text": resume_text, # Keep original text for potential future use (e.g., full preview)
                            "Job Role": selected_role
                        })
                        if score >= 90:
                            st.warning(f"🔔 High match found: {resume_file} ({score}%)")

            if results:
                results.sort(key=lambda x: x["Score (%)"], reverse=True) # Sort by score, highest first
                df = pd.DataFrame(results)
                df.index += 1 # Start index from 1 for better display

                st.download_button(
                    label="📥 Download Results as CSV",
                    data=df.to_csv(index=True).encode('utf-8'),
                    file_name='resume_match_results.csv',
                    mime='text/csv',
                    key="download_csv_results"
                )

                for idx, res in enumerate(results, 1):
                    st.markdown(f"### {idx}. {res['Resume']} — **{res['Score (%)']}% match**")
                    st.progress(res['Score (%)'] / 100)
                    st.markdown("**Matched Skills:** " + (res["Matched Skills"] or "None"))
                    st.markdown("**Missing Skills:** " + (res["Missing Skills"] or "None"))

                    # Shortlist checkbox - unique key for each resume
                    if st.checkbox("✅ Shortlist this resume", key=f"shortlist_{res['Resume']}"):
                        # Add to shortlisted if not already present
                        if not any(d['Resume'] == res['Resume'] for d in st.session_state.shortlisted):
                            st.session_state.shortlisted.append({
                                **res,
                                "Serial": len(st.session_state.shortlisted) + 1,
                                "Feedback": st.session_state.feedback.get(res['Resume'], "") # Get existing feedback or empty
                            })
                            st.success(f"'{res['Resume']}' added to shortlisted candidates!")

                    # Feedback text input - unique key for each resume
                    feedback = st.text_input("💬 Feedback - How well did this resume fit?", key=f"feedback_{res['Resume']}", 
                                             value=st.session_state.feedback.get(res['Resume'], ""))
                    st.session_state.feedback[res['Resume']] = feedback # Store/update feedback

                    st.markdown("---")
            else:
                st.info("ℹ️ No resumes matched the current filters and selected skills. Try adjusting criteria.")
        else:
            st.warning("⚠️ Please select skills from the filter above to begin matching resumes.")

        # Shortlisted candidates section
        if st.session_state.shortlisted:
            st.subheader("📋 Shortlisted Candidates")
            shortlisted_df = pd.DataFrame(st.session_state.shortlisted)
            
            # Update feedback column with the latest from session state
            shortlisted_df["Feedback"] = shortlisted_df["Resume"].map(st.session_state.feedback)

            # Allow filtering shortlisted candidates by job role
            filter_job_shortlist = st.selectbox("Filter shortlisted candidates by Job Role:", 
                                                  ["All"] + list(shortlisted_df["Job Role"].unique()),
                                                  key="filter_job_shortlist_selectbox")
            if filter_job_shortlist != "All":
                shortlisted_df = shortlisted_df[shortlisted_df["Job Role"] == filter_job_shortlist]

            shortlisted_df.index = range(1, len(shortlisted_df) + 1) # Reset index for display
            st.dataframe(shortlisted_df.drop(columns=["Text"]), use_container_width=True) # Exclude 'Text' column

            # Skill Popularity Chart for Shortlisted Candidates
            st.subheader("📈 Skill Popularity (Shortlisted Candidates)")
            if not shortlisted_df.empty:
                # Aggregate skills from all currently displayed (filtered) shortlisted resumes
                all_shortlisted_skills = []
                for entry in shortlisted_df.to_dict('records'): # Iterate over dataframe rows as dicts
                    if entry["Matched Skills"]: # Check if skills exist for this entry
                        # Split by comma and strip whitespace for each skill
                        all_shortlisted_skills.extend([s.strip().lower() for s in entry["Matched Skills"].split(",") if s.strip()])
                
                if all_shortlisted_skills:
                    skill_counts = pd.Series(all_shortlisted_skills).value_counts().rename_axis("Skill").reset_index(name="Count")
                    st.bar_chart(skill_counts.set_index("Skill"), use_container_width=True)
                else:
                    st.info("No matched skills found in the currently filtered shortlisted resumes for popularity chart.")
            else:
                st.info("No candidates in the shortlisted table to generate skill popularity.")