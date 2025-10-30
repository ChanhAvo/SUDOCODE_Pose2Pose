# -*- coding: utf-8 -*-
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Lesson - Poselinguo",
    page_icon="📖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .lesson-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .breadcrumb {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .lesson-progress-bar {
        background: rgba(255, 255, 255, 0.3);
        height: 8px;
        border-radius: 4px;
        margin-top: 1rem;
        overflow: hidden;
    }
    .lesson-progress-fill {
        background: white;
        height: 100%;
        transition: width 0.3s ease;
    }
    .content-section {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .video-container {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
    .camera-placeholder {
        background: linear-gradient(145deg, #e9ecef, #f8f9fa);
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 4rem 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .quiz-option {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
    }
    .quiz-option:hover {
        background: #e9ecef;
        border-color: #1E88E5;
        transform: translateX(5px);
    }
    .quiz-option-selected {
        background: #e3f2fd;
        border-color: #1E88E5;
        font-weight: 600;
    }
    .quiz-option-correct {
        background: #d4edda;
        border-color: #28a745;
    }
    .quiz-option-incorrect {
        background: #f8d7da;
        border-color: #dc3545;
    }
    .feedback-box {
        background: #e3f2fd;
        border-left: 4px solid #1E88E5;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    .score-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    .challenge-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    .nav-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .key-point {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy lesson content database
LESSON_CONTENT = {
    "Video": {
        "template": "video_template",
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "transcript": """
        Welcome to this lesson on American Sign Language!

        In this video, you'll learn the fundamental hand shapes and movements
        needed to communicate effectively in sign language. Pay close attention
        to the positioning of fingers and the direction of movement.

        Remember: Sign language is a complete language with its own grammar and syntax!
        """,
        "key_points": [
            "Hand shape is crucial for accuracy",
            "Movement direction changes meaning",
            "Facial expressions are part of grammar",
            "Practice slowly at first for precision"
        ]
    },
    "Interactive": {
        "template": "interactive_template",
        "demo_video": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "instructions": "Watch the demonstration carefully, then practice the sign yourself using your camera.",
        "sign_name": "Hello",
        "feedback_tips": [
            "Keep your hand at chest level",
            "Move your hand forward smoothly",
            "Maintain eye contact",
            "Smile naturally"
        ]
    },
    "Practice": {
        "template": "practice_template",
        "challenges": [
            {"sign": "Hello", "difficulty": "Easy", "points": 10},
            {"sign": "Thank You", "difficulty": "Easy", "points": 10},
            {"sign": "Please", "difficulty": "Medium", "points": 15},
            {"sign": "Sorry", "difficulty": "Medium", "points": 15},
            {"sign": "Help", "difficulty": "Hard", "points": 20}
        ]
    },
    "Quiz": {
        "template": "quiz_template",
        "questions": [
            {
                "question": "What is the most important aspect of sign language?",
                "options": [
                    "Speed of signing",
                    "Hand shape, movement, and location",
                    "Looking serious",
                    "Speaking while signing"
                ],
                "correct": 1,
                "explanation": "Sign language relies on precise hand shapes, movements, and locations. All three parameters must be correct for the sign to be understood."
            },
            {
                "question": "True or False: Facial expressions are optional in sign language.",
                "options": ["True", "False"],
                "correct": 1,
                "explanation": "False! Facial expressions are grammatical markers in sign language and can change the meaning of signs."
            },
            {
                "question": "Which of these is NOT a parameter of sign formation?",
                "options": [
                    "Hand shape",
                    "Movement",
                    "Voice tone",
                    "Location"
                ],
                "correct": 2,
                "explanation": "Voice tone is not a parameter of sign formation. Sign language is visual, not auditory."
            }
        ]
    }
}

# Initialize lesson state
if "lesson_state" not in st.session_state:
    st.session_state.lesson_state = {
        "current_step": 1,
        "total_steps": 1,
        "quiz_answers": {},
        "quiz_submitted": {},
        "quiz_score": 0,
        "practice_index": 0,
        "practice_score": 0
    }

# Check if we have lesson data in session state
if "current_lesson" not in st.session_state or not st.session_state.current_lesson:
    st.warning("No lesson selected. Redirecting to Modules page...")
    st.info("Please select a lesson from the Modules page.")
    if st.button("← Back to Modules", type="primary"):
        st.switch_page("pages/Modules.py")
    st.stop()

# Extract lesson info from session state
lesson_data = st.session_state.current_lesson
module_id = lesson_data.get("module_id", "")
lesson_index = lesson_data.get("lesson_index", 0)
lesson_type = lesson_data.get("lesson_type", "Video")
lesson_title = lesson_data.get("lesson_title", "Lesson")
module_title = lesson_data.get("module_title", "Module")
lesson_key = lesson_data.get("lesson_key", "")

# Get lesson content
content = LESSON_CONTENT.get(lesson_type, LESSON_CONTENT["Video"])

# Header with breadcrumb and progress
st.markdown(f"""
    <div class="lesson-header">
        <div class="breadcrumb">
            {module_title} > Lesson {lesson_index + 1}
        </div>
        <h1 style="margin: 0.5rem 0;">📖 {lesson_title}</h1>
        <p style="margin: 0.5rem 0; opacity: 0.9;">Type: {lesson_type}</p>
    </div>
""", unsafe_allow_html=True)

# Back button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Back to Modules", key="back_button"):
        st.switch_page("pages/Modules.py")

st.markdown("---")

# Render content based on template type
template = content.get("template", "video_template")

if template == "video_template":
    # VIDEO LESSON TEMPLATE
    st.markdown("## 🎥 Video Lesson")

    # Video player
    st.markdown(f"""
        <div class="video-container">
            <iframe src="{content['video_url']}" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

    # Transcript
    with st.expander("📄 View Transcript", expanded=False):
        st.markdown(content["transcript"])

    # Key points
    st.markdown("### 💡 Key Points to Remember")
    for idx, point in enumerate(content["key_points"], 1):
        st.markdown(f"""
            <div class="key-point">
                <strong>{idx}.</strong> {point}
            </div>
        """, unsafe_allow_html=True)

elif template == "interactive_template":
    # INTERACTIVE LESSON TEMPLATE
    st.markdown("## 🎯 Interactive Practice")

    st.info(f"**Instructions:** {content['instructions']}")

    st.markdown(f"### Sign to practice: `{content['sign_name']}`")

    # Split view: Demo video and camera
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📹 Demo Video**")
        st.markdown(f"""
            <div class="video-container">
                <iframe src="{content['demo_video']}" allowfullscreen></iframe>
            </div>
        """, unsafe_allow_html=True)

        # Playback controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.button("⏮️ Replay", use_container_width=True)
        with col_b:
            st.button("⏸️ Pause", use_container_width=True)
        with col_c:
            st.selectbox("Speed", ["0.5x", "0.75x", "1x", "1.25x", "1.5x"], index=2)

    with col2:
        st.markdown("**📷 Your Camera**")
        st.markdown("""
            <div class="camera-placeholder">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                <h3>Camera Integration Coming Soon</h3>
                <p style="color: #666;">
                    Real-time pose detection and comparison will be available here
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Action buttons
        col_x, col_y = st.columns(2)
        with col_x:
            st.button("🔄 Try Again", use_container_width=True, type="secondary")
        with col_y:
            st.button("✓ Continue", use_container_width=True, type="primary")

    # Tips section
    st.markdown("### 💬 Tips for Success")
    for tip in content["feedback_tips"]:
        st.markdown(f"- {tip}")

    # Simulated feedback
    st.markdown("""
        <div class="feedback-box">
            <strong>🤖 AI Feedback (Simulated):</strong><br>
            Great job! Your hand shape is accurate. Try to make your movement a bit smoother.
            <br><br><strong>Estimated Accuracy:</strong> 87%
        </div>
    """, unsafe_allow_html=True)

elif template == "practice_template":
    # PRACTICE LESSON TEMPLATE
    st.markdown("## ✍️ Practice Session")

    # Get current challenge
    current_idx = st.session_state.lesson_state["practice_index"]
    challenges = content["challenges"]

    if current_idx < len(challenges):
        challenge = challenges[current_idx]

        # Challenge card
        st.markdown(f"""
            <div class="challenge-card">
                <h2>Sign: {challenge['sign']}</h2>
                <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                    Difficulty: <strong>{challenge['difficulty']}</strong>
                </p>
                <p style="font-size: 1.1rem;">
                    Points: <strong>{challenge['points']}</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Progress indicator
        st.progress((current_idx + 1) / len(challenges))
        st.markdown(f"**Progress:** {current_idx + 1} / {len(challenges)} signs")

        # Camera placeholder
        st.markdown("""
            <div class="camera-placeholder">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                <h3>Perform the Sign</h3>
                <p style="color: #666;">
                    Position yourself in front of the camera and perform the sign
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Retry", key="retry_btn", use_container_width=True):
                st.info("Try the sign again!")
                st.rerun()

        with col2:
            if st.button("⏭️ Skip", key="skip_btn", use_container_width=True):
                st.session_state.lesson_state["practice_index"] += 1
                st.rerun()

        with col3:
            if st.button("✓ Submit", key="submit_btn", use_container_width=True, type="primary"):
                import random
                points_earned = int(challenge['points'] * random.uniform(0.7, 1.0))
                st.session_state.lesson_state["practice_score"] += points_earned
                st.session_state.lesson_state["practice_index"] += 1
                st.success(f"Great! You earned {points_earned} points!")
                st.rerun()

    else:
        # Practice complete
        total_score = st.session_state.lesson_state["practice_score"]
        max_score = sum(c["points"] for c in challenges)
        percentage = (total_score / max_score * 100) if max_score > 0 else 0

        st.markdown(f"""
            <div class="score-card">
                <h2>🎉 Practice Complete!</h2>
                <div style="font-size: 3rem; margin: 1.5rem 0;">
                    {'★' * int(percentage // 20)}{'☆' * (5 - int(percentage // 20))}
                </div>
                <h3>Score: {total_score} / {max_score} points</h3>
                <p style="font-size: 1.3rem; color: #1E88E5; font-weight: 600;">
                    Accuracy: {percentage:.0f}%
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Practice Again", use_container_width=True):
                st.session_state.lesson_state["practice_index"] = 0
                st.session_state.lesson_state["practice_score"] = 0
                st.rerun()
        with col2:
            if st.button("✅ Mark as Complete", use_container_width=True, type="primary"):
                # Mark lesson complete
                if "module_progress" not in st.session_state:
                    st.session_state.module_progress = {}
                st.session_state.module_progress[lesson_key] = True
                st.balloons()
                st.success("Lesson completed! Returning to modules...")
                st.switch_page("pages/Modules.py")

elif template == "quiz_template":
    # QUIZ LESSON TEMPLATE
    st.markdown("## 📝 Quiz")

    questions = content["questions"]
    current_q = st.session_state.lesson_state.get("current_question", 0)

    # Initialize quiz state
    if "current_question" not in st.session_state.lesson_state:
        st.session_state.lesson_state["current_question"] = 0

    if current_q < len(questions):
        question = questions[current_q]

        # Progress
        st.progress((current_q + 1) / len(questions))
        st.markdown(f"**Question {current_q + 1} of {len(questions)}**")

        # Question
        st.markdown(f"### {question['question']}")

        # Check if submitted
        submitted = st.session_state.lesson_state["quiz_submitted"].get(current_q, False)

        # Options
        for idx, option in enumerate(question["options"]):
            option_key = f"q{current_q}_opt{idx}"
            is_selected = st.session_state.lesson_state["quiz_answers"].get(current_q) == idx
            is_correct = idx == question["correct"]

            if not submitted:
                # Before submission - show as buttons
                button_type = "primary" if is_selected else "secondary"
                if st.button(f"{chr(65 + idx)}. {option}", key=option_key,
                           use_container_width=True, type=button_type):
                    st.session_state.lesson_state["quiz_answers"][current_q] = idx
                    st.rerun()
            else:
                # After submission - show with colors
                if is_correct:
                    st.success(f"✓ {chr(65 + idx)}. {option}")
                elif is_selected and not is_correct:
                    st.error(f"✗ {chr(65 + idx)}. {option}")
                else:
                    st.markdown(f"{chr(65 + idx)}. {option}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Check/Next buttons
        col1, col2 = st.columns(2)
        with col1:
            if not submitted and current_q in st.session_state.lesson_state["quiz_answers"]:
                if st.button("Check Answer", key="check_btn", use_container_width=True, type="primary"):
                    st.session_state.lesson_state["quiz_submitted"][current_q] = True
                    # Update score
                    if st.session_state.lesson_state["quiz_answers"][current_q] == question["correct"]:
                        st.session_state.lesson_state["quiz_score"] += 1
                    st.rerun()

        with col2:
            if submitted and current_q < len(questions) - 1:
                if st.button("Next Question →", key="next_btn", use_container_width=True, type="primary"):
                    st.session_state.lesson_state["current_question"] += 1
                    st.rerun()

        # Show explanation if submitted
        if submitted:
            st.markdown(f"""
                <div class="feedback-box">
                    <strong>💡 Explanation:</strong><br>
                    {question['explanation']}
                </div>
            """, unsafe_allow_html=True)

    else:
        # Quiz complete
        score = st.session_state.lesson_state["quiz_score"]
        total = len(questions)
        percentage = (score / total * 100) if total > 0 else 0

        st.markdown(f"""
            <div class="score-card">
                <h2>📊 Quiz Complete!</h2>
                <div style="font-size: 4rem; margin: 1.5rem 0; color: #1E88E5;">
                    {percentage:.0f}%
                </div>
                <h3>{score} / {total} Correct</h3>
                <p style="font-size: 1.2rem; color: #666; margin-top: 1rem;">
                    {'🎉 Excellent work!' if percentage >= 80 else '👍 Good effort!' if percentage >= 60 else '💪 Keep practicing!'}
                </p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.lesson_state["current_question"] = 0
                st.session_state.lesson_state["quiz_answers"] = {}
                st.session_state.lesson_state["quiz_submitted"] = {}
                st.session_state.lesson_state["quiz_score"] = 0
                st.rerun()
        with col2:
            if st.button("✅ Mark as Complete", use_container_width=True, type="primary"):
                # Mark lesson complete
                if "module_progress" not in st.session_state:
                    st.session_state.module_progress = {}
                st.session_state.module_progress[lesson_key] = True
                st.balloons()
                st.success("Lesson completed! Returning to modules...")
                st.switch_page("pages/Modules.py")

# Footer navigation
st.markdown("---")
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Back to Modules", key="back_footer", type="secondary", use_container_width=True):
        st.switch_page("pages/Modules.py")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 Lesson Info")
    st.markdown(f"**Module:** {module_title}")
    st.markdown(f"**Lesson:** {lesson_title}")
    st.markdown(f"**Type:** {lesson_type}")

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info("""
    - Take your time
    - Practice makes perfect
    - Review if needed
    - Ask questions
    """)
