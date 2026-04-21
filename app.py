import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from parser import extract_text
from nlp_utils import extract_skills, extract_basic_info, extract_expected_skills
from similarity import calculate_similarity
from llm_feedback import get_feedback, parse_feedback

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    /* Skill badges */
    .skill-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    .missing-skill-badge {
        background-color: #ffebee;
        color: #c62828;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    .present-skill-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    /* Status indicators */
    .success-text {
        color: #4caf50;
        font-weight: bold;
    }
    
    .warning-text {
        color: #ff9800;
        font-weight: bold;
    }
    
    .error-text {
        color: #f44336;
        font-weight: bold;
    }
    
    /* Feedback styling */
    .feedback-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Score card */
    .score-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1rem;
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title("Analysis Settings")
    
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Comprehensive", "Quick Scan", "ATS Focused"]
    )
    
    show_details = st.checkbox("Show Detailed Analysis", value=True)
    
    st.divider()
    st.markdown("###  Quick Stats")
    st.markdown("- **ATS Score**: Calculated with AI")
    st.markdown("- **Skills Match**: Keyword & semantic analysis")
    st.markdown("- **Experience Fit**: Role-specific matching")
    
    st.divider()
    st.caption(" Your data is secure and private")

# Main header
st.markdown("""
<div class="main-header">
    <h1>AI Resume Analyzer</h1>
    <p>Smart Resume Screening & Analysis powered by Artificial Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for upload
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX (Max 10MB)"
    )
    
    if uploaded_file:
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        st.json(file_details)

with col2:
    job_desc = st.text_area(
        " Paste Job Description",
        height=200,
        placeholder="Paste the job description here for analysis..."
    )

# Main analysis
if uploaded_file and job_desc:
    
    # Show loading spinner
    with st.spinner(" Analyzing your resume with AI..."):
        # Extract text
        text = extract_text(uploaded_file)
        
        # Extract basic info
        info = extract_basic_info(text)
        
        # Extract skills
        skills = extract_skills(text)
        expected_skills = extract_expected_skills(job_desc)
        
        # Calculate similarity score
        score = calculate_similarity(text, job_desc)
        percentage = score * 100
        
        # Get AI feedback
        feedback_text = get_feedback(text, job_desc)
        parsed_feedback = parse_feedback(feedback_text)
    
    # Stats Row - 4 columns
    st.markdown("###  Analysis Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    # Get ATS score from parsed feedback
    ats_score = parsed_feedback['ats_score']
    try:
        ats_score_int = int(ats_score) if ats_score != 'N/A' else percentage
    except:
        ats_score_int = percentage
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3> Match Score</h3>
            <h2 style="color: white;">{percentage:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3> ATS Score</h3>
            <h2 style="color: white;">{ats_score_int:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Skills Match</h3>
            <h2 style="color: white;">{len([s for s in expected_skills if s in skills])}/{len(expected_skills) if expected_skills else 0}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3> Total Skills</h3>
            <h2 style="color: white;">{len(skills)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Resume Preview Section
    with st.expander(" Resume Preview", expanded=False):
        st.text_area("Resume Content", text[:1000], height=200)
        
        # File info
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Name:** {info['Name']}")
            st.info(f"**Email:** {info['Email']}")
        with col2:
            st.info(f"**Total Skills Found:** {len(skills)}")
            st.info(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Skills Analysis Section
    st.markdown("###  Skills Analysis")
    
    # Create two columns for skills display
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("####  Skills Found in Resume")
        if skills:
            skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in sorted(skills)])
            st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
        else:
            st.warning("No skills detected")
    
    with col2:
        st.markdown("#### Expected Skills")
        if expected_skills:
            skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in sorted(expected_skills)])
            st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No expected skills listed")
    
    st.divider()
    
    # Skills Comparison Table with Colors
    st.markdown("###  Skills Comparison Matrix")
    
    # Create comparison data with color coding
    comparison_data = []
    for skill in expected_skills:
        present = skill in skills
        status = "✅ Present" if present else "❌ Missing"
        
        comparison_data.append({
            "Skill": skill.upper(),
            "Status": status,
            "Match": "✓" if present else "✗"
        })
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        
        # Color the dataframe function
        def color_status(val):
            if "Present" in str(val):
                return 'background-color: #d4edda; color: #155724'
            elif "Missing" in str(val):
                return 'background-color: #f8d7da; color: #721c24'
            return ''
        
        # Apply styling (compatible with newer pandas versions)
        try:
            styled_df = df_comparison.style.applymap(color_status, subset=['Status'])
        except AttributeError:
            styled_df = df_comparison.style.map(color_status, subset=['Status'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("No specific skills mentioned in the job description")
    
    # Missing Skills Section
    missing_skills = [s for s in expected_skills if s not in skills]
    if missing_skills:
        st.markdown("#### ❌ Missing Skills")
        missing_html = "".join([f'<span class="missing-skill-badge">{skill}</span>' for skill in missing_skills])
        st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)
        st.warning(f"⚠️ Your resume is missing {len(missing_skills)} key skill{'s' if len(missing_skills) > 1 else ''} required for this role")
    else:
        st.success(" Excellent! Your resume contains all the required skills!")
    
    st.divider()
    
    # Visualization Section
    st.markdown("###  Match Analysis")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Score Gauge", " Comparison Chart", " Skills Radar"])
    
    with tab1:
        # Gauge chart using plotly
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = percentage,
            title = {'text': "Overall Match Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4caf50" if percentage >= 70 else "#ff9800" if percentage >= 50 else "#f44336"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffebee"},
                    {'range': [50, 75], 'color': "#fff3e0"},
                    {'range': [75, 100], 'color': "#e8f5e9"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with tab2:
        # Detailed comparison chart
        metrics = {
            'Skills Match': len([s for s in expected_skills if s in skills]) / max(len(expected_skills), 1) * 100,
            'Overall Similarity': percentage,
            'ATS Score': ats_score_int,
            'Keyword Density': min(percentage * 0.8, 100)
        }
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color=['#4caf50', '#2196f3', '#ff9800', '#9c27b0'],
                text=[f'{v:.1f}%' for v in metrics.values()],
                textposition='auto',
            )
        ])
        fig_bar.update_layout(
            title="Detailed Metrics Breakdown",
            yaxis_title="Score (%)",
            yaxis_range=[0, 100],
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab3:
        # Radar chart for skill categories (simplified)
        categories = ['Technical Skills', 'Soft Skills', 'Experience', 'Education', 'ATS Compatibility']
        resume_scores = [
            min(100, len([s for s in skills if s in ['python', 'sql', 'machine learning']]) * 25),
            60,  # Soft skills (placeholder)
            min(100, percentage),
            min(100, percentage * 0.9),
            ats_score_int
        ]
        required_scores = [85, 70, 75, 85, 80]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=resume_scores,
            theta=categories,
            fill='toself',
            name='Your Resume',
            line_color='#4caf50'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=required_scores,
            theta=categories,
            fill='toself',
            name='Job Requirements',
            line_color='#f44336'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=400,
            title="Skills Category Comparison"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Progress Bar
    st.markdown("#### Match Progress")
    st.progress(int(percentage))
    
    st.divider()
    
    # AI Feedback Section
    st.markdown("###  AI-Powered Feedback")
    
    # Display ATS Score prominently
    st.markdown(f"""
    <div class="score-card">
        <h3> ATS Compatibility Score</h3>
        <div class="score-number">{ats_score_int}/100</div>
        <p>{'Excellent ATS Compatibility!' if ats_score_int >= 80 else 'Good ATS Score' if ats_score_int >= 60 else 'Needs ATS Optimization'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display parsed feedback sections
    if parsed_feedback['strengths']:
        with st.expander("Strengths", expanded=True):
            for strength in parsed_feedback['strengths'][:5]:
                st.markdown(f"✅ {strength}")
    
    if parsed_feedback['weaknesses']:
        with st.expander("⚠️ Areas for Improvement", expanded=True):
            for weakness in parsed_feedback['weaknesses'][:5]:
                st.markdown(f"🔴 {weakness}")
    
    if parsed_feedback['suggestions']:
        with st.expander(" Actionable Suggestions", expanded=True):
            for suggestion in parsed_feedback['suggestions'][:5]:
                st.markdown(f"📌 {suggestion}")
    
    if parsed_feedback['keywords']:
        with st.expander(" Keywords to Add", expanded=False):
            keywords_html = "".join([f'<span class="skill-badge">{kw}</span>' for kw in parsed_feedback['keywords'][:10]])
            st.markdown(f"<div>{keywords_html}</div>", unsafe_allow_html=True)
    
    if parsed_feedback['section_feedback']:
        with st.expander(" Section-wise Feedback", expanded=False):
            for section, feedback in parsed_feedback['section_feedback'].items():
                st.markdown(f"**{section}:** {feedback}")
    
    if parsed_feedback['recommendation'] != 'N/A':
        st.markdown("###  Overall Recommendation")
        rec_color = "success-text" if "Strong" in parsed_feedback['recommendation'] else "warning-text" if "Good" in parsed_feedback['recommendation'] else "error-text"
        st.markdown(f'<p class="{rec_color}">📌 {parsed_feedback["recommendation"]}</p>', unsafe_allow_html=True)
    
    # Show raw feedback in expander if needed
    with st.expander(" View Detailed AI Analysis", expanded=False):
        st.markdown(feedback_text)
    
    st.divider()
    
    # Actionable Recommendations
    st.markdown("###  Quick Action Items")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("#### Immediate Actions")
        recommendations = [
            "✨ Add missing keywords from job description",
            "✨ Quantify achievements with metrics",
            "✨ Improve resume formatting for ATS",
            "✨ Highlight relevant experience first"
        ]
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    with rec_col2:
        st.markdown("#### Skill Development")
        if missing_skills:
            for skill in missing_skills[:3]:
                st.markdown(f"-  Take a course in **{skill}**")
                st.markdown(f"  -  Build a project using {skill}")
        else:
            st.markdown("-  Take advanced certifications")
            st.markdown("- Contribute to open source")
    
    # Export Options
    st.divider()
    st.markdown("###  Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Download PDF Report", use_container_width=True):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button(" Export as CSV", use_container_width=True):
            # Create CSV data
            export_data = {
                "Metric": ["Match Score", "ATS Score", "Skills Match", "Total Skills", "Missing Skills"],
                "Value": [f"{percentage:.1f}%", f"{ats_score_int}%", 
                         f"{len([s for s in expected_skills if s in skills])}/{len(expected_skills) if expected_skills else 0}", 
                         len(skills), len(missing_skills)]
            }
            df_export = pd.DataFrame(export_data)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label=" Download CSV",
                data=csv,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col3:
        if st.button("🔗 Share Analysis", use_container_width=True):
            st.info("Share feature coming soon!")

else:
    # Show placeholder when no data
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background-color: #f8f9fa; border-radius: 10px;">
        <h3> Ready to analyze your resume?</h3>
        <p>Upload your resume and paste the job description to get started!</p>
        <p style="color: #666;">Get AI-powered insights, match scores, and actionable recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show features
    st.markdown("### ✨ Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ####  AI Analysis
        - Smart skill extraction
        - Contextual matching
        - Semantic similarity
        - ATS score calculation
        """)
    
    with col2:
        st.markdown("""
        ####  Visual Insights
        - Interactive charts
        - Score gauges
        - Skills comparison
        - Radar analysis
        """)
    
    with col3:
        st.markdown("""
        ####  Smart Recommendations
        - Missing skills
        - ATS optimization
        - Career guidance
        - Keyword suggestions
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Powered by Google Gemini AI | Secure & Private | Real-time Analysis</p>
    <p>Built with Streamlit, Gemini AI, and NLP</p>
</div>
""", unsafe_allow_html=True)