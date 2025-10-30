import streamlit as st
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Assessment - Poselinguo",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .assessment-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-indicator {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background: #f8f9fa;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 0 0.5rem;
        font-weight: 600;
    }
    .step-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .step-completed {
        background: #28a745;
        color: white;
    }
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #1E88E5;
    }
    .result-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .level-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .level-beginner {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1E3A8A;
    }
    .level-intermediate {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #1E3A8A;
    }
    .level-advanced {
        background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        color: white;
    }
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "assessment_step" not in st.session_state:
    st.session_state.assessment_step = 1
if "basic_info" not in st.session_state:
    st.session_state.basic_info = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "assessment_complete" not in st.session_state:
    st.session_state.assessment_complete = False
if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None

# Quiz questions database
QUIZ_QUESTIONS = {
    "multiple_choice": [
        {
            "id": "mc1",
            "question": "What is sign language primarily based on?",
            "options": [
                "Finger spelling only",
                "Visual-manual gestures including hand shapes, movements, and facial expressions",
                "Written symbols",
                "Morse code patterns"
            ],
            "correct": 1,
            "difficulty": "beginner"
        },
        {
            "id": "mc2",
            "question": "American Sign Language (ASL) is the same as British Sign Language (BSL).",
            "options": [
                "True - All sign languages are universal",
                "False - Different countries have different sign languages",
                "Partially true - They share 50% of signs",
                "True - Only the accents differ"
            ],
            "correct": 1,
            "difficulty": "beginner"
        },
        {
            "id": "mc3",
            "question": "In sign language, what role do facial expressions play?",
            "options": [
                "They are optional and just for emphasis",
                "They are grammatical markers that can change meaning",
                "They are only used for emotions",
                "They have no significance"
            ],
            "correct": 1,
            "difficulty": "intermediate"
        },
        {
            "id": "mc4",
            "question": "What is 'fingerspelling' in sign language?",
            "options": [
                "Making up signs randomly",
                "Spelling out words letter by letter using hand shapes",
                "A warm-up exercise",
                "Pointing at written letters"
            ],
            "correct": 1,
            "difficulty": "beginner"
        },
        {
            "id": "mc5",
            "question": "Which of the following is NOT a parameter of sign formation?",
            "options": [
                "Hand shape",
                "Movement",
                "Voice tone",
                "Location"
            ],
            "correct": 2,
            "difficulty": "intermediate"
        }
    ],
    "short_answer": [
        {
            "id": "sa1",
            "question": "Why is it important to learn sign language? (Write 2-3 sentences)",
            "difficulty": "beginner"
        },
        {
            "id": "sa2",
            "question": "Describe what you know about deaf culture or the deaf community.",
            "difficulty": "intermediate"
        }
    ]
}

def calculate_assessment_score(quiz_answers):
    """Calculate quiz score and determine proficiency level"""
    mc_correct = 0
    mc_total = len(QUIZ_QUESTIONS["multiple_choice"])

    # Calculate multiple choice score
    for q in QUIZ_QUESTIONS["multiple_choice"]:
        if quiz_answers.get(q["id"]) == q["correct"]:
            mc_correct += 1

    mc_percentage = (mc_correct / mc_total) * 100

    # Analyze short answers (simple keyword-based analysis)
    sa_scores = []
    for q in QUIZ_QUESTIONS["short_answer"]:
        answer = quiz_answers.get(q["id"], "").lower()

        # Simple scoring based on answer length and keywords
        score = 0
        if len(answer.split()) >= 10:  # Minimum word count
            score += 50

        # Check for relevant keywords
        keywords = ["communication", "accessibility", "deaf", "inclusive", "community",
                   "hearing", "barrier", "culture", "language", "understand"]
        keyword_count = sum(1 for keyword in keywords if keyword in answer)
        score += min(keyword_count * 10, 50)

        sa_scores.append(min(score, 100))

    sa_percentage = sum(sa_scores) / len(sa_scores) if sa_scores else 0

    # Weighted final score (70% MC, 30% SA)
    final_score = (mc_percentage * 0.7) + (sa_percentage * 0.3)

    # Determine level
    if final_score >= 75:
        level = "Advanced"
        level_class = "level-advanced"
    elif final_score >= 50:
        level = "Intermediate"
        level_class = "level-intermediate"
    else:
        level = "Beginner"
        level_class = "level-beginner"

    return {
        "final_score": final_score,
        "mc_score": mc_percentage,
        "sa_score": sa_percentage,
        "mc_correct": mc_correct,
        "mc_total": mc_total,
        "level": level,
        "level_class": level_class,
        "timestamp": datetime.now().isoformat()
    }

def generate_ai_recommendations(result, basic_info):
    """Generate AI-based recommendations based on assessment results"""
    level = result["level"]

    recommendations = {
        "Beginner": {
            "modules": [
                "ASL Alphabet & Fingerspelling Fundamentals",
                "Basic Greetings and Introductions",
                "Numbers and Colors in Sign Language",
                "Common Everyday Phrases"
            ],
            "focus_areas": [
                "Hand shape formation",
                "Basic vocabulary building",
                "Understanding sign language structure",
                "Introduction to deaf culture"
            ],
            "estimated_time": "2-3 months for foundational skills",
            "next_steps": "Start with daily practice of the alphabet and basic signs for 15-20 minutes"
        },
        "Intermediate": {
            "modules": [
                "Advanced Conversational Phrases",
                "Grammar and Sentence Structure",
                "Storytelling in Sign Language",
                "Regional Sign Variations"
            ],
            "focus_areas": [
                "Facial expressions and non-manual markers",
                "Sentence structure and grammar",
                "Expanding vocabulary to 500+ signs",
                "Understanding context and nuance"
            ],
            "estimated_time": "3-4 months to advance skills",
            "next_steps": "Practice conversational signing for 30 minutes daily and engage with deaf community events"
        },
        "Advanced": {
            "modules": [
                "Professional and Technical Signing",
                "ASL Literature and Poetry",
                "Interpreting Techniques",
                "Deaf History and Advocacy"
            ],
            "focus_areas": [
                "Fluency and natural expression",
                "Complex grammatical structures",
                "Cultural competency",
                "Advanced storytelling and narrative techniques"
            ],
            "estimated_time": "Ongoing refinement and specialization",
            "next_steps": "Consider interpreter certification programs or community teaching opportunities"
        }
    }

    return recommendations.get(level, recommendations["Beginner"])

# Header
st.markdown("""
    <div class="assessment-header">
        <h1>Sign Language Proficiency Assessment</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">
            Discover your current level and get personalized learning recommendations
        </p>
    </div>
""", unsafe_allow_html=True)

# Step indicator
steps = ["Basic Info", "Quiz", "Results"]
current_step = st.session_state.assessment_step

st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
cols = st.columns(3)
for idx, step_name in enumerate(steps, 1):
    with cols[idx-1]:
        if idx < current_step:
            st.markdown(f'<div class="step-box step-completed"> {step_name}</div>', unsafe_allow_html=True)
        elif idx == current_step:
            st.markdown(f'<div class="step-box step-active">{step_name}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-box">{step_name}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Progress bar
progress = (current_step - 1) / (len(steps) - 1)
st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# STEP 1: Basic Information
if st.session_state.assessment_step == 1:
    st.markdown("## Step 1: Basic Information")
    st.markdown("Tell us a bit about yourself to help us personalize your learning experience.")

    with st.form("basic_info_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your name")
            age_group = st.selectbox(
                "Age Group *",
                ["Select...", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]
            )
            prior_experience = st.selectbox(
                "Prior Sign Language Experience *",
                ["Select...", "None - Complete beginner", "Some exposure (watched videos, met deaf people)",
                 "Taken a class or course before", "Fluent or near-fluent"]
            )

        with col2:
            email = st.text_input("Email Address (Optional)", placeholder="your.email@example.com")
            learning_goal = st.selectbox(
                "Primary Learning Goal *",
                ["Select...", "Personal interest", "Communicate with deaf family/friends",
                 "Professional development", "Academic requirement", "Community involvement"]
            )
            time_commitment = st.selectbox(
                "Available Learning Time per Week *",
                ["Select...", "Less than 2 hours", "2-5 hours", "5-10 hours", "More than 10 hours"]
            )

        st.markdown("---")

        motivation = st.text_area(
            "What motivates you to learn sign language? *",
            placeholder="Share your motivation in 2-3 sentences...",
            height=100
        )

        submit_basic = st.form_submit_button("Continue to Quiz", use_container_width=True, type="primary")

        if submit_basic:
            if name and age_group != "Select..." and prior_experience != "Select..." and \
               learning_goal != "Select..." and time_commitment != "Select..." and motivation:
                st.session_state.basic_info = {
                    "name": name,
                    "email": email,
                    "age_group": age_group,
                    "prior_experience": prior_experience,
                    "learning_goal": learning_goal,
                    "time_commitment": time_commitment,
                    "motivation": motivation
                }
                st.session_state.assessment_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")

# STEP 2: Quiz
elif st.session_state.assessment_step == 2:
    st.markdown("## Step 2: Knowledge Assessment Quiz")
    st.markdown(f"Welcome, **{st.session_state.basic_info['name']}**! Let's assess your current knowledge.")

    st.info("**Tip**: Answer honestly - this helps us create the perfect learning path for you. There's no passing or failing!")

    with st.form("quiz_form"):
        # Multiple Choice Questions
        st.markdown("### Part A: Multiple Choice Questions")
        st.markdown("Select the best answer for each question.")

        for idx, q in enumerate(QUIZ_QUESTIONS["multiple_choice"], 1):
            st.markdown(f"""
                <div class="question-card">
                    <p style="font-weight: 600; color: #1E88E5; margin-bottom: 0.5rem;">
                        Question {idx} of {len(QUIZ_QUESTIONS["multiple_choice"])}
                    </p>
                    <p style="font-size: 1.1rem; margin-bottom: 1rem;">{q['question']}</p>
                </div>
            """, unsafe_allow_html=True)

            answer = st.radio(
                "Select your answer:",
                options=range(len(q["options"])),
                format_func=lambda x: q["options"][x],
                key=f"mc_{q['id']}"
            )
            st.session_state.quiz_answers[q["id"]] = answer
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")

        # Short Answer Questions
        st.markdown("### Part B: Short Answer Questions")
        st.markdown("Please provide thoughtful answers in your own words.")

        for idx, q in enumerate(QUIZ_QUESTIONS["short_answer"], 1):
            st.markdown(f"""
                <div class="question-card">
                    <p style="font-weight: 600; color: #1E88E5; margin-bottom: 0.5rem;">
                        Question {idx}
                    </p>
                    <p style="font-size: 1.1rem; margin-bottom: 1rem;">{q['question']}</p>
                </div>
            """, unsafe_allow_html=True)

            answer = st.text_area(
                "Your answer:",
                placeholder="Type your answer here...",
                height=120,
                key=f"sa_{q['id']}"
            )
            st.session_state.quiz_answers[q["id"]] = answer
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.form_submit_button("Back", use_container_width=True):
                st.session_state.assessment_step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Submit Assessment", use_container_width=True, type="primary"):
                # Check if all questions answered
                all_answered = True
                for q in QUIZ_QUESTIONS["short_answer"]:
                    if not st.session_state.quiz_answers.get(q["id"], "").strip():
                        all_answered = False
                        break

                if all_answered:
                    # Calculate results
                    result = calculate_assessment_score(st.session_state.quiz_answers)
                    st.session_state.assessment_result = result
                    st.session_state.assessment_step = 3
                    st.session_state.assessment_complete = True
                    st.rerun()
                else:
                    st.error("Please answer all questions before submitting.")

# STEP 3: Results
elif st.session_state.assessment_step == 3:
    result = st.session_state.assessment_result
    basic_info = st.session_state.basic_info

    st.markdown("## Assessment Complete!")
    st.markdown(f"Congratulations, **{basic_info['name']}**! Here are your results:")

    st.markdown("---")

    # Overall Result
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="result-card" style="text-align: center;">
                <h3 style="color: #1E88E5; margin-bottom: 1rem;">Your Proficiency Level</h3>
                <div class="{result['level_class']} level-badge">
                    {result['level']}
                </div>
                <p style="font-size: 1.1rem; margin-top: 1rem; color: #666;">
                    Overall Score: <strong>{result['final_score']:.1f}%</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed Breakdown
    st.markdown("### Detailed Score Breakdown")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="result-card">
                <h4>Multiple Choice</h4>
                <p style="font-size: 2rem; color: #1E88E5; margin: 0.5rem 0;">
                    {result['mc_correct']}/{result['mc_total']}
                </p>
                <p style="color: #666;">Score: {result['mc_score']:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="result-card">
                <h4>Short Answer</h4>
                <p style="font-size: 2rem; color: #1E88E5; margin: 0.5rem 0;">
                    {result['sa_score']:.0f}%
                </p>
                <p style="color: #666;">Based on answer quality</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # AI-Generated Recommendations
    st.markdown("### Your Personalized Learning Path")
    recommendations = generate_ai_recommendations(result, basic_info)

    st.success(f"""
    **Great news!** Based on your **{result['level']}** level and your goal to
    *"{basic_info['learning_goal']}"*, we've created a customized learning plan for you.
    """)

    # Recommended Modules
    st.markdown("#### Recommended Learning Modules")
    cols = st.columns(2)
    for idx, module in enumerate(recommendations["modules"]):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="result-card">
                    <p style="margin: 0;">{module}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Focus Areas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Focus Areas")
        for area in recommendations["focus_areas"]:
            st.markdown(f"- {area}")

    with col2:
        st.markdown("#### Timeline & Next Steps")
        st.markdown(f"**Estimated Timeline:** {recommendations['estimated_time']}")
        st.markdown(f"**Next Step:** {recommendations['next_steps']}")

    st.markdown("---")

    # Call to Action
    st.markdown("### Ready to Start Learning?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Download Results", use_container_width=True):
            # Create downloadable report
            report = {
                "basic_info": basic_info,
                "assessment_result": result,
                "recommendations": recommendations
            }
            st.download_button(
                "Download JSON Report",
                data=json.dumps(report, indent=2),
                file_name=f"poselinguo_assessment_{basic_info['name'].replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )

    with col2:
        if st.button("Retake Assessment", use_container_width=True):
            # Reset assessment
            st.session_state.assessment_step = 1
            st.session_state.quiz_answers = {}
            st.session_state.assessment_result = None
            st.session_state.assessment_complete = False
            st.rerun()

    with col3:
        if st.button("Start Learning", use_container_width=True, type="primary"):
            st.balloons()
            st.success("Awesome! Your learning modules are being prepared. Navigate to the Learning page to begin!")

            # Store user profile
            if "user_profile" not in st.session_state:
                st.session_state.user_profile = {}

            st.session_state.user_profile.update({
                "name": basic_info["name"],
                "level": result["level"],
                "assessment_date": result["timestamp"],
                "learning_goal": basic_info["learning_goal"],
                "recommended_modules": recommendations["modules"]
            })

# Sidebar Info
with st.sidebar:
    st.markdown("### Assessment Info")
    st.info("""
    This assessment helps us:
    - Identify your current level
    - Understand your goals
    - Create a personalized learning path
    - Recommend the right modules for you
    """)

    if st.session_state.assessment_step > 1:
        st.markdown("---")
        st.markdown("### Progress")
        st.markdown(f"**Current Step:** {st.session_state.assessment_step}/3")
        if st.session_state.basic_info:
            st.markdown(f"**Name:** {st.session_state.basic_info.get('name', 'N/A')}")

    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("""
    - Answer honestly for best results
    - Take your time
    - There are no wrong answers
    - This takes about 10-15 minutes
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p><strong>Poselinguo Assessment</strong> - Powered by AI</p>
        <p style="font-size: 0.9rem;">Your data is private and used only to personalize your learning experience</p>
    </div>
""", unsafe_allow_html=True)
