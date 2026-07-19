import streamlit as st
import requests
import json
import sys
from pathlib import Path

# Add backend directory to sys.path to allow importing local modules if running directly
ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.agents.career_graph import CareerGraph
    from app.agents.state import CareerState
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

# Premium Theme and Styling
st.set_page_config(
    page_title="SkillSync AI - Career Analysis & Recommendations",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and premium dark/glassmorphic look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        background: linear-gradient(135deg, #FF3366 0%, #FF6633 50%, #FFCC33 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #8892B0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 51, 102, 0.4);
        box-shadow: 0 10px 20px rgba(255, 51, 102, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FF3366;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #CCD6F6;
        font-weight: 600;
    }
    
    .skill-tag {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
        transition: all 0.2s ease;
    }
    
    .skill-tag-matched {
        background: rgba(46, 213, 115, 0.15);
        color: #2ed573;
        border: 1px solid rgba(46, 213, 115, 0.3);
    }
    
    .skill-tag-matched:hover {
        background: rgba(46, 213, 115, 0.25);
    }
    
    .skill-tag-missing {
        background: rgba(255, 71, 87, 0.15);
        color: #ff4757;
        border: 1px solid rgba(255, 71, 87, 0.3);
    }
    
    .skill-tag-missing:hover {
        background: rgba(255, 71, 87, 0.25);
    }
    
    .card-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFF;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }
    
    /* Custom button styling */
    .stButton>button {
        background: linear-gradient(135deg, #FF3366 0%, #FF6633 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF6633 0%, #FF3366 100%);
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 51, 102, 0.5);
    }
    
    /* Accordion header text */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title & Header
st.markdown('<div class="main-title">🎯 SkillSync AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Career Analysis & Skill Gap Recommendation System</div>', unsafe_allow_html=True)

# Sample Data Definition
SAMPLE_RESUME = """John Doe
Senior Frontend Engineer

Summary:
Passionate frontend developer with 4+ years of experience designing and implementing rich web applications. Strong expert in React, TypeScript, and CSS frameworks. Experienced in leading small teams, optimizing rendering performance, and implementing robust frontend architectures.

Technical Skills:
- Languages: JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL
- Frameworks & Libraries: React, Next.js, Redux Toolkit, Tailwind CSS, Jest, React Testing Library
- Tools: Git, Webpack, Vite, Docker, VS Code, Figma
- Concepts: RESTful APIs, GraphQL, Responsive Web Design, Web Accessibility (WCAG), CI/CD pipelines

Experience:
Frontend Engineer @ WebCore Solutions (2023 - Present)
- Led migrations from legacy codebase to modern React + TypeScript stack, improving core web vitals by 35%.
- Maintained a shared UI components library with React and Tailwind CSS, standardizing designs across 4 separate products.
- Implemented responsive landing pages and state management using Redux.

Software Developer @ DevAgency (2022 - 2023)
- Built custom dashboard applications using Next.js and REST APIs for client projects.
- Collaborated with UX designers to translate Figma mockups into pixel-perfect components.
- Setup end-to-end testing setups using Cypress."""

SAMPLE_JOB_DESC = """Senior Full-Stack Engineer (React & Python)

We are looking for a Senior Full-Stack Engineer to help build our core web application. You will work on designing interactive customer-facing interfaces and scale our backend services.

Required Technical Skills:
- Frontend: React, Next.js, TypeScript, Tailwind CSS, Redux
- Backend: Python, FastAPI or Django, PostgreSQL
- Database & Cache: Redis, SQL
- Infrastructure: Docker, Git, CI/CD, AWS (S3, EC2)
- Testing: Jest, PyTest, Unit Testing

Qualifications:
- Solid experience building and deploying production-grade web applications.
- Strong analytical and debugging skills.
- Comfort working in a fast-paced environment with regular releases."""

# Sidebar for settings & info
with st.sidebar:
    st.image("https://img.icons8.com/gradient/512/artificial-intelligence.png", width=100)
    st.markdown("### Settings")
    
    connection_mode = st.radio(
        "API Connection Mode",
        ["Auto (Try API, fallback to local)", "Force Local Graph", "Force API Backend"],
        key="connection_mode_radio"
    )
    
    import os
    default_api_url = os.environ.get("BACKEND_API_URL", "http://127.0.0.1:8080")
    api_url = st.text_input("FastAPI Backend URL", default_api_url, key="api_url_input")
    
    st.markdown("---")
    st.markdown("### How it works")
    st.write(
        "1. **Extract**: AI parses your resume and the job description.\n"
        "2. **Match**: Identifies overlapping skills and critical missing requirements.\n"
        "3. **Plan**: Formulates a detailed learning roadmap, course options, and structured report."
    )
    
    if st.button("Load Sample Data", key="load_sample_data_btn"):
        st.session_state["resume_input"] = SAMPLE_RESUME
        st.session_state["job_input"] = SAMPLE_JOB_DESC
        st.success("Sample data loaded!")

# Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Paste Resume Text")
    resume_text = st.text_area(
        "Paste the raw text of your resume here:",
        value=st.session_state.get("resume_input", ""),
        height=300,
        placeholder="Enter your professional experience, summary, and skills...",
        key="resume_text_area"
    )

with col2:
    st.markdown("### 📋 Paste Job Description")
    job_desc = st.text_area(
        "Paste the target job description here:",
        value=st.session_state.get("job_input", ""),
        height=300,
        placeholder="Enter the job duties, requirements, and required skills...",
        key="job_desc_area"
    )

# Action button
analyze_btn = st.button("🚀 Analyze Career Alignment", key="analyze_alignment_btn")

if analyze_btn:
    if not resume_text.strip():
        st.error("Please enter your resume text first!")
    elif not job_desc.strip():
        st.error("Please enter the target job description first!")
    else:
        # Perform analysis
        with st.spinner("SkillSync AI is analyzing your profile... Please wait."):
            results = None
            error_message = ""
            
            # API Method
            use_api = connection_mode in ["Auto (Try API, fallback to local)", "Force API Backend"]
            use_local = connection_mode in ["Auto (Try API, fallback to local)", "Force Local Graph"]
            
            if use_api:
                try:
                    response = requests.post(
                        f"{api_url.rstrip('/')}/api/v1/analyze",
                        json={
                            "resume_text": resume_text,
                            "job_description": job_desc
                        },
                        timeout=60
                    )
                    if response.status_code == 200:
                        results = response.json()
                    else:
                        error_message = f"Backend API returned status code {response.status_code}: {response.text}"
                except Exception as e:
                    error_message = f"Failed to connect to API backend: {str(e)}"
            
            # Local Fallback Method
            if results is None and use_local:
                if GRAPH_AVAILABLE:
                    st.info("Using local LangGraph pipeline instance...")
                    try:
                        graph = CareerGraph()
                        initial_state = {
                            "resume_text": resume_text,
                            "job_description": job_desc,
                            "resume_data": {},
                            "job_data": {},
                            "matched_skills": [],
                            "missing_skills": [],
                            "match_score": 0,
                            "roadmap": "",
                            "courses": [],
                            "report": ""
                        }
                        final_state = graph.run(initial_state)
                        results = {
                            "match_score": final_state["match_score"],
                            "matched_skills": final_state["matched_skills"],
                            "missing_skills": final_state["missing_skills"],
                            "roadmap": final_state["roadmap"],
                            "courses": final_state["courses"],
                            "report": final_state["report"]
                        }
                    except Exception as ex:
                        error_message += f"\nLocal graph run failed: {str(ex)}"
                else:
                    error_message += "\nLocal LangGraph environment not loaded. Make sure backend is in PYTHONPATH."

            # Display Results
            if results:
                st.success("Analysis complete!")
                
                # Visual stats / Metrics
                st.markdown("### 📊 Alignment Summary")
                m_col1, m_col2, m_col3 = st.columns(3)
                
                score = results["match_score"]
                
                # Assign dynamic colors based on score
                if score >= 80:
                    score_color = "#2ed573" # Green
                elif score >= 50:
                    score_color = "#ffa502" # Orange
                else:
                    score_color = "#ff4757" # Red
                
                with m_col1:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-value" style="color: {score_color};">{score}%</div>
                            <div class="metric-label">Match Score</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with m_col2:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-value" style="color: #2ed573;">{len(results['matched_skills'])}</div>
                            <div class="metric-label">Matched Skills</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                with m_col3:
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-value" style="color: #ff4757;">{len(results['missing_skills'])}</div>
                            <div class="metric-label">Missing Skills</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Detailed Skill Comparison
                st.markdown("### 🛠️ Skills Analysis")
                s_col1, s_col2 = st.columns(2)
                
                with s_col1:
                    st.markdown('<div class="card-header">Matched Skills</div>', unsafe_allow_html=True)
                    if results["matched_skills"]:
                        matched_html = "".join([f'<span class="skill-tag skill-tag-matched">{skill}</span>' for skill in results["matched_skills"]])
                        st.markdown(matched_html, unsafe_allow_html=True)
                    else:
                        st.info("No matching technical skills found.")
                        
                with s_col2:
                    st.markdown('<div class="card-header">Missing Skills</div>', unsafe_allow_html=True)
                    if results["missing_skills"]:
                        missing_html = "".join([f'<span class="skill-tag skill-tag-missing">{skill}</span>' for skill in results["missing_skills"]])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.success("Excellent! You match all identified technical skills.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Learning Roadmap & Report
                st.markdown("### 📈 Career Advisory Plan")
                
                tab1, tab2, tab3 = st.tabs(["🛣️ Learning Roadmap", "📚 Recommended Courses", "📝 Advisory Report"])
                
                with tab1:
                    st.markdown("#### Personalized Upskilling Roadmap")
                    st.write(results["roadmap"])
                    
                with tab2:
                    st.markdown("#### Recommended Learning Resources")
                    if results["courses"]:
                        for idx, course in enumerate(results["courses"]):
                            st.info(f"📘 **Course {idx+1}**: {course}")
                    else:
                        st.write("No specific courses recommended.")
                        
                with tab3:
                    st.markdown("#### Evaluation Report")
                    st.write(results["report"])
                    
            else:
                st.error("Could not generate analysis results. See details below:")
                st.code(error_message)
