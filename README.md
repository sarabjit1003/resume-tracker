
 📄 Resume Tracker App

A smart and user-friendly Resume Screening Tool built with **Python** and **Streamlit**. This app helps recruiters or job seekers quickly compare a resume against a job description by identifying matching and missing skills.


 🚀 Features

- Upload a Resume (PDF or Text) and Job Description files.
- Automatically extracts keywords and skills from both documents.
- Shows matched skills and highlights missing skills.
- Provides an overall match score with visual graphs.
- Easy-to-use web interface using Streamlit.



📂 Project Structure

resume_tracker/
├── resumes/               # Folder containing example resumes or test data organized by job roles
├── app.py                 # Main Streamlit application that runs the web interface
├── match_engine.py        # Core logic that compares resumes with job descriptions and calculates match scores
├── match_test.py          # Test script to validate and debug the matching logic (unit tests or sample runs)
├── resume_parser.py       # Code to extract text and relevant info (like skills) from resume files
├── job matcher.py         # (Assuming typo, probably 'job_matcher.py') Script/module to process job descriptions and assist matching
├── requirements.txt       # Lists all Python libraries/packages needed to run the project
└── README.md              # Project overview, instructions, and documentation

 🛠️ How to Run the App Locally

1. Clone or download this repository to your local machine.
2. Install required Python packages by running:
   pip install -r requirements.txt

3. Run the Streamlit app using:
streamlit run app.py

4. Open your browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).


 📸 Screenshots

_Add screenshots here later as you enhance the UI._


 💡 Future Enhancements

- Add database support to store resumes and user feedback.
- Implement user authentication and role-based access.
- Improve UI/UX design and add more interactive visualizations.
- Support more file formats for resumes and job descriptions.


 👩‍💻 Author

**Sarabjit Mehta**  
Passionate about automating recruitment processes and building easy-to-use tools.



📺 Demo Video

For a quick walkthrough of the project, watch the demo here:  
[YouTube Link or other video hosting link]


📄 License

This project is open-source and available under the MIT License.

