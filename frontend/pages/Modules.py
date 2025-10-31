# -*- coding: utf-8 -*-
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Learning Modules - Poselinguo",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .modules-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .module-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #1E88E5;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    .module-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1rem;
    }
    .module-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin: 0;
    }
    .module-badge {
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-beginner {
        background: #d4edda;
        color: #155724;
    }
    .badge-intermediate {
        background: #fff3cd;
        color: #856404;
    }
    .badge-advanced {
        background: #cce5ff;
        color: #004085;
    }
    .badge-locked {
        background: #f8d7da;
        color: #721c24;
    }
    .badge-completed {
        background: #d1ecf1;
        color: #0c5460;
    }
    .lesson-list {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    .lesson-item {
        background: white;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .lesson-item:last-child {
        margin-bottom: 0;
    }
    .lesson-number {
        background: #1E88E5;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    .lesson-completed {
        background: #28a745;
    }
    .lesson-content {
        flex-grow: 1;
    }
    .lesson-title {
        font-weight: 600;
        color: #333;
        margin: 0;
    }
    .lesson-duration {
        font-size: 0.85rem;
        color: #666;
    }
    .progress-section {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Module database - abbreviated for space
MODULES_DATABASE = {
    "Beginner": [
        {
            "id": "mod1",
            "title": "ASL Alphabet & Fingerspelling Fundamentals",
            "description": "Master the foundation of American Sign Language by learning the manual alphabet and fingerspelling techniques.",
            "difficulty": "Beginner",
            "duration": "2 weeks",
            "lessons_count": 8,
            "estimated_hours": 12,
            "skills": ["Hand shapes", "Letter formation", "Spelling fluency", "Recognition speed"],
            "lessons": [
                {"title": "Introduction to Manual Alphabet", "duration": "45 min", "type": "Video"},
                {"title": "Letters A-M Practice", "duration": "90 min", "type": "Interactive"},
                {"title": "Letters N-Z Practice", "duration": "90 min", "type": "Interactive"},
                {"title": "Common Words", "duration": "60 min", "type": "Practice"},
                {"title": "Speed Drills", "duration": "45 min", "type": "Practice"},
                {"title": "Reading Practice", "duration": "60 min", "type": "Interactive"},
                {"title": "Names and Places", "duration": "45 min", "type": "Practice"},
                {"title": "Assessment", "duration": "30 min", "type": "Quiz"}
            ]
        },
        {
            "id": "mod2",
            "title": "Basic Greetings and Introductions",
            "description": "Learn essential signs for everyday greetings, introductions, and simple conversations.",
            "difficulty": "Beginner",
            "duration": "2 weeks",
            "lessons_count": 10,
            "estimated_hours": 15,
            "skills": ["Basic vocabulary", "Social phrases", "Question formation", "Polite expressions"],
            "lessons": [
                {"title": "Common Greetings", "duration": "60 min", "type": "Video"},
                {"title": "Introducing Yourself", "duration": "75 min", "type": "Interactive"},
                {"title": "Asking Questions", "duration": "90 min", "type": "Interactive"},
                {"title": "Polite Phrases", "duration": "45 min", "type": "Practice"},
                {"title": "Family Signs", "duration": "60 min", "type": "Interactive"},
                {"title": "Feelings", "duration": "60 min", "type": "Practice"},
                {"title": "Yes/No Questions", "duration": "45 min", "type": "Interactive"},
                {"title": "Practice Conversations", "duration": "90 min", "type": "Practice"},
                {"title": "Deaf Etiquette", "duration": "45 min", "type": "Video"},
                {"title": "Assessment", "duration": "40 min", "type": "Quiz"}
            ]
        }
    ],
    "Intermediate": [
        {
            "id": "mod5",
            "title": "Advanced Conversational Phrases",
            "description": "Take your signing to the next level with complex sentence structures and natural conversational flow.",
            "difficulty": "Intermediate",
            "duration": "3 weeks",
            "lessons_count": 12,
            "estimated_hours": 20,
            "skills": ["Complex sentences", "Idioms", "Conversational flow", "Natural expressions"],
            "lessons": [
                {"title": "Complex Sentence Structures", "duration": "90 min", "type": "Video"},
                {"title": "ASL Idioms", "duration": "75 min", "type": "Interactive"},
                {"title": "Describing People", "duration": "90 min", "type": "Interactive"},
                {"title": "Expressing Opinions", "duration": "75 min", "type": "Practice"},
                {"title": "Making Plans", "duration": "90 min", "type": "Interactive"},
                {"title": "Past Events", "duration": "90 min", "type": "Interactive"},
                {"title": "Future Plans", "duration": "90 min", "type": "Interactive"},
                {"title": "Giving Directions", "duration": "75 min", "type": "Practice"},
                {"title": "Agreement", "duration": "60 min", "type": "Practice"},
                {"title": "Clarification Strategies", "duration": "60 min", "type": "Interactive"},
                {"title": "Extended Practice", "duration": "120 min", "type": "Practice"},
                {"title": "Assessment", "duration": "60 min", "type": "Quiz"}
            ]
        }
    ],
    "Advanced": [
        {
            "id": "mod9",
            "title": "Professional and Technical Signing",
            "description": "Master specialized vocabulary for professional settings including medical, legal, and business contexts.",
            "difficulty": "Advanced",
            "duration": "4 weeks",
            "lessons_count": 14,
            "estimated_hours": 25,
            "skills": ["Professional vocabulary", "Technical terms", "Formal register", "Specialized contexts"],
            "lessons": [
                {"title": "Professional Communication", "duration": "90 min", "type": "Video"},
                {"title": "Medical Terminology", "duration": "120 min", "type": "Interactive"},
                {"title": "Legal Terms", "duration": "120 min", "type": "Interactive"},
                {"title": "Educational Settings", "duration": "90 min", "type": "Practice"},
                {"title": "Business Vocabulary", "duration": "90 min", "type": "Interactive"},
                {"title": "Technology Signs", "duration": "90 min", "type": "Interactive"},
                {"title": "Financial Terms", "duration": "75 min", "type": "Practice"},
                {"title": "Meeting Skills", "duration": "120 min", "type": "Interactive"},
                {"title": "Interview Signing", "duration": "90 min", "type": "Practice"},
                {"title": "Formal Register", "duration": "75 min", "type": "Video"},
                {"title": "Professional Networking", "duration": "90 min", "type": "Interactive"},
                {"title": "Workplace Scenarios", "duration": "120 min", "type": "Practice"},
                {"title": "Case Studies", "duration": "90 min", "type": "Project"},
                {"title": "Assessment", "duration": "75 min", "type": "Quiz"}
            ]
        }
    ]
}

# Initialize session state
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Guest User",
        "level": "Beginner",
        "completed_modules": [],
        "current_module": None,
        "total_hours": 0
    }

# Ensure all keys exist in user_profile
if "completed_modules" not in st.session_state.user_profile:
    st.session_state.user_profile["completed_modules"] = []
if "current_module" not in st.session_state.user_profile:
    st.session_state.user_profile["current_module"] = None
if "total_hours" not in st.session_state.user_profile:
    st.session_state.user_profile["total_hours"] = 0
if "level" not in st.session_state.user_profile:
    st.session_state.user_profile["level"] = "Beginner"
if "name" not in st.session_state.user_profile:
    st.session_state.user_profile["name"] = "Guest User"

if "module_progress" not in st.session_state:
    st.session_state.module_progress = {}

# Helper functions
def get_module_status(module_id):
    """Determine module status"""
    if module_id in st.session_state.user_profile["completed_modules"]:
        return "completed"
    elif module_id == st.session_state.user_profile.get("current_module"):
        return "in_progress"
    else:
        return "available"

def calculate_overall_progress():
    """Calculate progress percentage"""
    level = st.session_state.user_profile.get("level", "Beginner")
    total_modules = len(MODULES_DATABASE.get(level, []))
    completed = len(st.session_state.user_profile.get("completed_modules", []))
    return (completed / total_modules * 100) if total_modules > 0 else 0

# Header
st.markdown("""
    <div class="modules-header">
        <h1>📚 Your Learning Path</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">
            Personalized modules designed for your learning journey
        </p>
    </div>
""", unsafe_allow_html=True)

# Check if user has completed assessment
assessment_completed = st.session_state.get("assessment_complete", False)

if not assessment_completed:
    # Show error message if assessment not completed
    st.error("### ⚠️ Assessment Required")
    st.markdown("""
    <div style="background: #fff3cd; padding: 2rem; border-radius: 15px; border-left: 5px solid #ffc107; margin: 2rem 0;">
        <h3 style="color: #856404; margin-top: 0;">🚫 Access Restricted</h3>
        <p style="color: #856404; font-size: 1.1rem; line-height: 1.6;">
            You need to complete the <strong>Assessment</strong> first to access your personalized learning modules.
        </p>
        <p style="color: #856404; margin-bottom: 0;">
            The assessment helps us:
        </p>
        <ul style="color: #856404;">
            <li>Identify your current sign language proficiency level</li>
            <li>Understand your learning goals and preferences</li>
            <li>Create a personalized learning path tailored to your needs</li>
            <li>Recommend the most appropriate modules for your skill level</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📋 Ready to Get Started?")
        if st.button("🚀 Take Assessment Now", use_container_width=True, type="primary", key="take_assessment"):
            st.info("📍 Please navigate to the **Assessment** page from the sidebar to begin your personalized learning journey!")
            st.markdown("""
            <div style="background: #d1ecf1; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
                <h4 style="color: #0c5460; margin-top: 0;">What to Expect:</h4>
                <p style="color: #0c5460; margin-bottom: 0.5rem;">
                    ⏱️ <strong>Duration:</strong> 10-15 minutes<br>
                    📝 <strong>Format:</strong> Multiple choice + Short answer questions<br>
                    🎯 <strong>Result:</strong> Personalized learning path with recommended modules
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Show preview of what modules look like
    st.markdown("### 👀 Preview: What You'll Get After Assessment")
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #666; font-style: italic;">
            Once you complete the assessment, you'll receive a customized learning path with modules
            specifically designed for your proficiency level (Beginner, Intermediate, or Advanced).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **🌱 Beginner Level**
        - ASL Alphabet & Fingerspelling
        - Basic Greetings
        - Numbers & Colors
        - Common Phrases
        """)
    with col2:
        st.markdown("""
        **🌿 Intermediate Level**
        - Advanced Conversations
        - Grammar & Structure
        - Storytelling Techniques
        - Regional Variations
        """)
    with col3:
        st.markdown("""
        **🌳 Advanced Level**
        - Professional Signing
        - ASL Literature & Poetry
        - Interpreting Techniques
        - Deaf History & Advocacy
        """)

    # Stop execution here - don't show the rest of the page
    st.stop()

# Get user info (only if assessment completed)
user_level = st.session_state.user_profile.get("level", "Beginner")
user_name = st.session_state.user_profile.get("name", "Guest User")

# Progress Overview
st.markdown("### 📊 Your Progress Overview")

overall_progress = calculate_overall_progress()
completed_count = len(st.session_state.user_profile["completed_modules"])
total_modules = len(MODULES_DATABASE.get(user_level, []))
total_hours = st.session_state.user_profile.get("total_hours", 0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Current Level</div>
            <div class="stat-value" style="font-size: 1.5rem;">{user_level}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Modules Completed</div>
            <div class="stat-value">{completed_count}/{total_modules}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Overall Progress</div>
            <div class="stat-value">{overall_progress:.0f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Learning Hours</div>
            <div class="stat-value">{total_hours}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Module List
st.markdown(f"## 🎓 {user_level} Level Modules")

current_modules = MODULES_DATABASE.get(user_level, [])

if not current_modules:
    st.warning("No modules available. Please take the assessment first!")
else:
    st.info(f"💡 **Welcome, {user_name}!** Complete these modules in order for the best learning experience.")

    for idx, module in enumerate(current_modules, 1):
        module_status = get_module_status(module["id"])

        # Status badge
        if module_status == "completed":
            badge_class = "badge-completed"
            status_icon = "✅"
            status_text = "Completed"
        elif module_status == "in_progress":
            badge_class = f"badge-{module['difficulty'].lower()}"
            status_icon = "🔄"
            status_text = "In Progress"
        else:
            badge_class = f"badge-{module['difficulty'].lower()}"
            status_icon = "📖"
            status_text = "Available"

        # Module card
        with st.container():
            st.markdown(f"""
                <div class="module-card">
                    <div class="module-header">
                        <div>
                            <p style="color: #666; margin: 0; font-size: 0.9rem;">Module {idx}</p>
                            <h3 class="module-title">{status_icon} {module['title']}</h3>
                        </div>
                        <span class="module-badge {badge_class}">{status_text}</span>
                    </div>
                    <p style="color: #555; line-height: 1.6; margin: 1rem 0;">
                        {module['description']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Metadata
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**⏱️ Duration:** {module['duration']}")
            with col2:
                st.markdown(f"**📑 Lessons:** {module['lessons_count']}")
            with col3:
                st.markdown(f"**🎯 Hours:** {module['estimated_hours']}h")
            with col4:
                st.markdown(f"**📊 Level:** {module['difficulty']}")

            # Skills
            st.markdown("**💪 Skills You'll Learn:**")
            skills_cols = st.columns(4)
            for idx_skill, skill in enumerate(module['skills']):
                with skills_cols[idx_skill % 4]:
                    st.markdown(f"• {skill}")

            # Lessons list
            with st.expander(f"📋 View All {module['lessons_count']} Lessons", expanded=False):
                for lesson_idx, lesson in enumerate(module['lessons'], 1):
                    lesson_key = f"{module['id']}_lesson_{lesson_idx}"
                    lesson_completed = st.session_state.module_progress.get(lesson_key, False)

                    col_lesson, col_button = st.columns([4, 1])

                    with col_lesson:
                        status_mark = "✓" if lesson_completed else lesson_idx
                        st.markdown(f"""
                            <div class="lesson-item">
                                <span class="lesson-number {'lesson-completed' if lesson_completed else ''}">
                                    {status_mark}
                                </span>
                                <div class="lesson-content">
                                    <p class="lesson-title">{lesson['title']}</p>
                                    <p class="lesson-duration">{lesson['duration']} • {lesson['type']}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    with col_button:
                        if lesson_completed:
                            st.button("✓ Done", key=f"done_{lesson_key}", disabled=True)
                        else:
                            if st.button("Start", key=f"start_{lesson_key}", type="secondary"):
                                # Store lesson data in session state for the lesson page
                                st.session_state.current_lesson = {
                                    "module_id": module["id"],
                                    "lesson_index": lesson_idx,
                                    "lesson_type": lesson["type"],
                                    "lesson_title": lesson["title"],
                                    "module_title": module["title"],
                                    "lesson_key": lesson_key
                                }
                                # Navigate to lesson page
                                st.switch_page("pages/Lesson.py")

            # Action buttons
            col1, col2 = st.columns(2)

            with col1:
                if module_status != "completed":
                    button_text = "Continue Module" if module_status == "in_progress" else "Start Module"
                    if st.button(f"🚀 {button_text}", key=f"start_mod_{module['id']}",
                               use_container_width=True, type="primary"):
                        st.session_state.user_profile["current_module"] = module['id']
                        st.success(f"Module started: {module['title']}")
                        st.rerun()

            with col2:
                if module_status == "completed":
                    if st.button("📜 Certificate", key=f"cert_{module['id']}", use_container_width=True):
                        st.info("Certificate feature coming soon!")
                elif module_status == "in_progress":
                    if st.button("✅ Complete", key=f"complete_{module['id']}", use_container_width=True):
                        if module['id'] not in st.session_state.user_profile["completed_modules"]:
                            st.session_state.user_profile["completed_modules"].append(module['id'])
                            st.session_state.user_profile["total_hours"] += module['estimated_hours']
                            st.session_state.user_profile["current_module"] = None
                            st.balloons()
                            st.success(f"Module completed: {module['title']}")
                            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Learning Path Status")

    # Show assessment status
    if st.session_state.get("assessment_complete", False):
        st.success("✅ Assessment Completed")
        st.markdown(f"**Level:** {st.session_state.user_profile.get('level', 'Unknown')}")
        st.markdown(f"**Name:** {st.session_state.user_profile.get('name', 'Guest')}")
    else:
        st.warning("⚠️ Assessment Pending")
        st.markdown("Complete the assessment to unlock modules")

    st.markdown("---")

    st.markdown("### 📚 Quick Actions")

    if st.session_state.get("assessment_complete", False):
        if st.button("🔄 Reset Progress", use_container_width=True):
            if st.session_state.get("confirm_reset", False):
                st.session_state.user_profile["completed_modules"] = []
                st.session_state.user_profile["current_module"] = None
                st.session_state.user_profile["total_hours"] = 0
                st.session_state.module_progress = {}
                st.session_state.confirm_reset = False
                st.success("Progress reset!")
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("Click again to confirm")

    st.markdown("---")
    st.markdown("### 💡 Tips")
    if st.session_state.get("assessment_complete", False):
        st.info("""
        - Practice daily
        - Complete in order
        - Review lessons
        - Engage with community
        """)
    else:
        st.info("""
        - Take the assessment first
        - Answer honestly
        - It takes 10-15 minutes
        - Get personalized modules
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p><strong>Poselinguo Learning Modules</strong></p>
        <p style="font-size: 0.9rem;">Keep learning! 🌱</p>
    </div>
""", unsafe_allow_html=True)
