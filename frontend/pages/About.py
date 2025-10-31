import streamlit as st

# Page configuration
st.set_page_config(
    page_title="About Us - Poselinguo",
    page_icon="👥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .about-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .about-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .about-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
    }
    .mission-card {
        background: linear-gradient(145deg, #f0f8ff, #e6f3ff);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .team-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    .team-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .team-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .team-role {
        font-size: 1rem;
        color: #7B1FA2;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .value-card {
        background: linear-gradient(145deg, #fff3e0, #ffe0b2);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stats-box {
        background: linear-gradient(145deg, #e8f5e9, #c8e6c9);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="about-header">
        <div class="about-title">👥 About Us</div>
        <div class="about-subtitle">
            Meet the passionate team behind Poselinguo
        </div>
    </div>
""", unsafe_allow_html=True)

# Mission & Vision
st.markdown("## 🎯 Our Mission & Vision")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="mission-card">
            <h3>🚀 Our Mission</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                To break down communication barriers and foster inclusivity by providing an intelligent,
                adaptive learning platform that makes sign language education accessible, engaging, and
                effective for learners at all levels.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
                We believe that everyone should have the opportunity to communicate freely, regardless
                of hearing ability, and that technology can be a powerful tool in bridging communication gaps.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="mission-card">
            <h3>🌟 Our Vision</h3>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                A world where sign language is universally understood and accessible, where communication
                barriers no longer exist, and where the deaf and hard of hearing communities are fully
                integrated into society.
            </p>
            <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
                Through AI-powered education, we aim to create a global community of sign language users
                who can connect, communicate, and collaborate without limitations.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Our Story
st.markdown("## 📖 Our Story")
st.markdown("""
**Poselinguo** was born from a simple yet powerful observation: while technology has revolutionized education
in countless ways, sign language learning remained largely traditional and inaccessible to many.

Our team came together with a shared passion for leveraging cutting-edge AI technology to solve real-world
problems. We recognized that deep learning, computer vision, and natural language processing could transform
how people learn sign language - making it more interactive, personalized, and effective than ever before.

What started as a project has evolved into a mission to empower millions of people worldwide to communicate
across hearing barriers, fostering a more inclusive and connected society.
""")

st.markdown("---")

# Meet the Team
st.markdown("## 👨‍💻 Meet Our Team")
st.markdown("### The People Building the Future of Sign Language Education")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="team-card">
            <div class="team-icon">👨‍💻</div>
            <div class="team-name">Huy Mai</div>
            <div class="team-role">Mentee • AI/ML Engineer</div>
            <p style="text-align: left;">
                Specializes in developing and optimizing deep learning models for pose estimation and
                real-time feedback. Passionate about making AI accessible and practical for education.
            </p>
            <hr style="margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #666;">
                <strong>Focus Areas:</strong><br>
                • Pose Detection Models<br>
                • Learning Algorithms<br>
                • Model Optimization
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="team-card">
            <div class="team-icon">👩‍💻</div>
            <div class="team-name">Tram Anh</div>
            <div class="team-role">Mentee • Frontend Developer</div>
            <p style="text-align: left;">
                Designs intuitive and engaging user interfaces that make learning sign language
                enjoyable. Committed to creating accessible experiences for all learners.
            </p>
            <hr style="margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #666;">
                <strong>Focus Areas:</strong><br>
                • User Experience Design<br>
                • Frontend Development<br>
                • Accessibility Features
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="team-card">
            <div class="team-icon">👨‍💻</div>
            <div class="team-name">Phuoc Chu</div>
            <div class="team-role">Mentee • Backend Engineer</div>
            <p style="text-align: left;">
                Builds robust backend systems that power our personalization engine and data processing
                pipelines. Ensures scalability and reliability of our platform.
            </p>
            <hr style="margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #666;">
                <strong>Focus Areas:</strong><br>
                • Backend Architecture<br>
                • Data Processing<br>
                • System Integration
            </p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="team-card">
            <div class="team-icon">👨‍🏫</div>
            <div class="team-name">Huy Vo</div>
            <div class="team-role">Mentor • Tech Lead</div>
            <p style="text-align: left;">
                Guides the team with extensive expertise in AI and software architecture. Provides
                strategic direction and ensures technical excellence across all aspects of the project.
            </p>
            <hr style="margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #666;">
                <strong>Focus Areas:</strong><br>
                • Technical Leadership<br>
                • AI Architecture<br>
                • Team Development
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Our Values
st.markdown("## 💎 Our Core Values")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="value-card">
            <h3>🌍 Accessibility</h3>
            <p>We believe education should be accessible to everyone, everywhere. Our platform is designed
            to remove barriers and provide equal learning opportunities.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="value-card">
            <h3>🚀 Innovation</h3>
            <p>We embrace cutting-edge technology and continuously push the boundaries of what's possible
            in AI-powered education.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="value-card">
            <h3>🤝 Inclusivity</h3>
            <p>We're committed to fostering a community where everyone feels welcome and supported,
            regardless of their background or ability level.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="value-card">
            <h3>📚 Learning-First</h3>
            <p>Every feature we build is designed with learner success in mind. We prioritize effectiveness
            and engagement in everything we do.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="value-card">
            <h3>💡 Transparency</h3>
            <p>We believe in open communication and clear explanations of how our AI systems work and make
            decisions about your learning path.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="value-card">
            <h3>🌱 Growth</h3>
            <p>We're dedicated to continuous improvement - both in our technology and in supporting
            your personal learning journey.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Impact & Goals
st.markdown("## 📊 Our Impact & Goals")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stats-box">
            <h2 style="color: #1E88E5; margin: 0;">500+</h2>
            <p style="margin: 0.5rem 0 0 0;"><strong>Sign Lessons</strong></p>
            <p style="font-size: 0.9rem; color: #666;">Comprehensive curriculum</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stats-box">
            <h2 style="color: #1E88E5; margin: 0;">3</h2>
            <p style="margin: 0.5rem 0 0 0;"><strong>AI Models</strong></p>
            <p style="font-size: 0.9rem; color: #666;">Powering our platform</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stats-box">
            <h2 style="color: #1E88E5; margin: 0;">∞</h2>
            <p style="margin: 0.5rem 0 0 0;"><strong>Learning Paths</strong></p>
            <p style="font-size: 0.9rem; color: #666;">Personalized for you</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stats-box">
            <h2 style="color: #1E88E5; margin: 0;">24/7</h2>
            <p style="margin: 0.5rem 0 0 0;"><strong>AI Support</strong></p>
            <p style="font-size: 0.9rem; color: #666;">Always available</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.info("""
**Our Commitment**: We're dedicated to continuously improving our platform, expanding our curriculum,
and reaching more learners worldwide. Every feature we add and every improvement we make is driven by
our mission to make sign language education accessible to all.
""")

st.markdown("---")

# Get Involved
st.markdown("## 🤝 Get Involved")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌟 Join Our Community
    Whether you're a learner, educator, or advocate for accessibility, there's a place for you in the
    Poselinguo community:

    - **Learn with us**: Start your sign language journey today
    - **Share feedback**: Help us improve our platform
    - **Spread the word**: Tell others about our mission
    - **Contribute**: Share your expertise and ideas
    """)

with col2:
    st.markdown("""
    ### 📬 Contact Us
    We'd love to hear from you! Whether you have questions, suggestions, or just want to say hello:

    - **Feedback**: Share your experience and suggestions
    - **Partnerships**: Collaborate with us on accessibility initiatives
    - **Press Inquiries**: Learn more about our work
    - **General Questions**: We're here to help!
    """)

st.markdown("---")

# Call to Action
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.success("""
    **Ready to join us in breaking down communication barriers?**

    Start your sign language learning journey today and be part of a movement toward a more
    inclusive and connected world.
    """)

    if st.button("🚀 Start Learning Now", use_container_width=True, type="primary"):
        st.balloons()
        st.info("👉 Head back to the Home page to begin your personalized learning journey!")

st.markdown("---")

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">
            <strong>Poselinguo</strong> - Breaking Barriers, Building Bridges
        </p>
        <p style="font-size: 1rem; margin-bottom: 0.5rem;">
            Empowering communication through AI-powered sign language education 🤟
        </p>
        <p style="font-size: 0.9rem; color: #999;">
            Made with ❤️ by Team Poselinguo | © 2024
        </p>
    </div>
""", unsafe_allow_html=True)
