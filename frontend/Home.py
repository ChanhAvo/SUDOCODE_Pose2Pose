import streamlit as st
import sys
from pathlib import Path

# Add backend directory to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Page configuration
st.set_page_config(
    page_title="Poselinguo - AI Sign Language Learning",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    .feature-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .how-it-works {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .cta-section {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
    }
    .stats-box {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤟 Poselinguo")
    st.markdown("*AI-Powered Sign Language Learning*")
    st.markdown("---")

    st.markdown("### 📍 Navigation")
    st.info("""
    **Home** - Project Overview

    **About** - Team & Mission

    **Documentation** - Guides & Help
    """)

    st.markdown("---")
    st.markdown("### 🌟 Quick Stats")
    st.metric("Active Features", "4+")
    st.metric("Learning Modules", "500+")
    st.metric("AI Models", "3")

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🤟 Welcome to Poselinguo</div>
        <div class="hero-subtitle">
            Master Sign Language with AI-Powered Personalized Learning
        </div>
        <p style="font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Break communication barriers and connect with the deaf community through
            our intelligent, adaptive learning platform that makes sign language education
            accessible, engaging, and effective for everyone.
        </p>
    </div>
""", unsafe_allow_html=True)

# Project Overview
st.markdown("## 📖 What is Poselinguo?")
st.markdown("""
**Poselinguo** is an innovative AI-powered application designed to revolutionize sign language education.
We combine cutting-edge deep learning technology with personalized teaching methodologies to create an
immersive learning experience that adapts to each learner's unique needs and pace.

Our platform leverages advanced computer vision, natural language processing, and machine learning to provide:
- **Real-time pose detection and feedback**
- **Personalized learning paths based on your skill level**
- **Interactive AI chat assistant for instant help**
- **Comprehensive progress tracking and analytics**
""")

st.markdown("---")

# Key Features
st.markdown("## ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered Learning</h3>
            <p>Advanced deep learning models analyze your signing in real-time, providing instant feedback
            on accuracy, hand positioning, and movement patterns.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Personalized Path</h3>
            <p>Take an initial assessment to determine your level, then receive customized learning modules
            and exercises tailored to your proficiency and goals.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>RAG Chat Assistant</h3>
            <p>Ask questions about any pose or sign using natural language. Our RAG-powered AI provides
            instant, contextual answers to help you learn faster.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎥</div>
            <h3>Video Learning</h3>
            <p>Watch demonstrations and guess signs, then practice with your camera on to compare
            your poses with tutorial examples.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Real-Time Scoring</h3>
            <p>Get immediate feedback with detailed scoring on your pose accuracy, helping you
            improve quickly and track your progress.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Progress Analytics</h3>
            <p>Monitor your learning journey with comprehensive analytics, tracking modules completed,
            practice time, and skill improvements.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# How It Works
st.markdown("## 🚀 How It Works")
st.markdown('<div class="how-it-works">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="step-card">
            <h3>1️⃣ Assessment</h3>
            <p><strong>Take a quick test</strong> to identify your current sign language proficiency level:</p>
            <ul>
                <li>Beginner</li>
                <li>Intermediate</li>
                <li>Advanced</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="step-card">
            <h3>2️⃣ Personalization</h3>
            <p><strong>Complete a questionnaire</strong> about your:</p>
            <ul>
                <li>Learning goals</li>
                <li>Interests & preferences</li>
                <li>Available time</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="step-card">
            <h3>3️⃣ Generate Path</h3>
            <p><strong>Receive custom materials</strong> including:</p>
            <ul>
                <li>Personalized modules</li>
                <li>Targeted exercises</li>
                <li>Progress milestones</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="step-card">
            <h3>4️⃣ Interactive Learning</h3>
            <p><strong>Study your modules</strong> with engaging activities:</p>
            <ul>
                <li><strong>Video Watching:</strong> Guess signs by watching demonstrations</li>
                <li><strong>Live Practice:</strong> Perform poses with camera-based real-time comparison</li>
                <li><strong>Instant Feedback:</strong> Get scoring and corrections immediately</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="step-card">
            <h3>5️⃣ Continuous Support</h3>
            <p><strong>Access help anytime</strong> with:</p>
            <ul>
                <li><strong>Chat with Poselinguo:</strong> Ask questions about any pose or sign</li>
                <li><strong>Natural Language:</strong> Type your questions in plain English</li>
                <li><strong>Instant Answers:</strong> Get context-aware responses powered by RAG</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Technology Overview
st.markdown("## 🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="stats-box">
            <h3>🎨 Frontend</h3>
            <ul style="text-align: left; display: inline-block;">
                <li>Streamlit</li>
                <li>Real-time Video Processing</li>
                <li>Responsive Design</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stats-box">
            <h3>🧠 AI/ML</h3>
            <ul style="text-align: left; display: inline-block;">
                <li>Deep Learning Models</li>
                <li>RAG System (LangChain)</li>
                <li>Computer Vision</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stats-box">
            <h3>⚙️ Backend</h3>
            <ul style="text-align: left; display: inline-block;">
                <li>Python</li>
                <li>Pose Estimation APIs</li>
                <li>NLP Processing</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Use Cases
st.markdown("## 🎯 Who Is This For?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👥 Personal Learners
    - **Family & Friends**: Communicate with deaf/hard of hearing loved ones
    - **Cultural Enthusiasts**: Explore sign language and deaf culture
    - **Self-Improvement**: Add a valuable skill to your repertoire

    ### 🎓 Students & Educators
    - **Academic Requirements**: Complete coursework in sign language
    - **Special Education**: Support inclusive classroom environments
    - **Language Students**: Learn as a second or third language
    """)

with col2:
    st.markdown("""
    ### 💼 Professionals
    - **Healthcare Workers**: Better serve deaf patients
    - **Customer Service**: Provide inclusive service experiences
    - **Interpreters**: Prepare for certification exams

    ### 🌍 Community Members
    - **Volunteers**: Engage with deaf community organizations
    - **Advocates**: Promote accessibility and inclusion
    - **Content Creators**: Create accessible content
    """)

st.markdown("---")

# Call to Action
st.markdown("""
    <div class="cta-section">
        <h2 style="color: #1E3A8A; margin-bottom: 1rem;">🎉 Ready to Start Your Journey?</h2>
        <p style="font-size: 1.2rem; color: #334155; margin-bottom: 2rem;">
            Join our community of learners and start mastering sign language today!
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Get Started Now", use_container_width=True, type="primary"):
        st.balloons()
        st.success("🎉 Welcome to Poselinguo! Navigate to the About page to learn more about our team, or start exploring the features above!")

st.markdown("<br>", unsafe_allow_html=True)

# Quick Links
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👥 Meet Our Team", use_container_width=True):
        st.info("📍 Navigate to the **About** page in the sidebar to learn about our team!")
with col2:
    if st.button("📚 View Documentation", use_container_width=True):
        st.info("📖 Check out the **Documentation** page for detailed guides!")
with col3:
    if st.button("💬 Try AI Chat", use_container_width=True):
        st.info("🚧 AI Chat feature coming soon!")

st.markdown("---")

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p style="font-size: 1.1rem;"><strong>Poselinguo</strong> - Empowering Communication Through AI</p>
        <p>Breaking barriers, building bridges through sign language education 🤟</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">Made with ❤️ by Team Poselinguo | © 2024</p>
    </div>
""", unsafe_allow_html=True)
