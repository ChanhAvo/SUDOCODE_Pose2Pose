import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add backend directory to path for imports
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.functions import query_rag_system, get_rag_stats

# Page configuration
st.set_page_config(
    page_title="Chat - Poselinguo",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .chat-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.95;
    }
    .source-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    .source-card:hover {
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .source-title {
        font-weight: bold;
        color: #667eea;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .source-detail {
        color: #495057;
        margin: 0.3rem 0;
    }
    .example-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    .stats-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .stats-label {
        color: #6c757d;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

# Header
st.markdown("""
    <div class="chat-header">
        <h1>💬 Chat với Trợ lý VSL</h1>
        <p>Hỏi bất cứ điều gì về Ngôn ngữ Ký hiệu Việt Nam</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Thống kê")

    # Get RAG stats
    try:
        stats = get_rag_stats()
        if stats.get("initialized"):
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{stats.get('document_count', 0):,}</div>
                    <div class="stats-label">Từ vựng trong cơ sở dữ liệu</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Đang khởi tạo hệ thống...")
    except Exception as e:
        st.warning("Không thể tải thống kê")

    st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.query_count}</div>
            <div class="stats-label">Câu hỏi trong phiên này</div>
        </div>
    """, unsafe_allow_html=True)

    # Session duration
    duration = datetime.now() - st.session_state.session_start
    minutes = int(duration.total_seconds() / 60)
    st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{minutes}</div>
            <div class="stats-label">Phút trò chuyện</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 💡 Mẹo sử dụng")
    st.markdown("""
    - Hỏi về nghĩa của các từ ký hiệu
    - Tìm kiếm từ theo mô tả
    - Hỏi về từ loại và cách sử dụng
    - Yêu cầu mã video để xem hướng dẫn
    """)

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.session_start = datetime.now()
        st.rerun()

# Main chat area
st.markdown("### 💬 Trò chuyện")

# Example questions
with st.expander("✨ Câu hỏi mẫu - Click để thử ngay!", expanded=len(st.session_state.messages) == 0):
    col1, col2 = st.columns(2)

    example_questions = [
        "Từ 'xin chào' có nghĩa là gì?",
        "Làm thế nào để biểu đạt 'cảm ơn'?",
        "Tìm từ ký hiệu về gia đình",
        "Từ 'yêu' được ký hiệu như thế nào?",
    ]

    for i, question in enumerate(example_questions):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(f"📝 {question}", key=f"example_{i}", use_container_width=True):
                # Add to messages and process
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display sources if available
        if message["role"] == "assistant" and "sources" in message:
            sources = message["sources"]
            if sources:
                with st.expander(f"📚 Xem {len(sources)} nguồn tham khảo"):
                    for j, source in enumerate(sources, 1):
                        metadata = source.get("metadata", {})
                        video_url = metadata.get("video_url")
                        has_video = metadata.get("has_video", False)
                        video_id = metadata.get("video_id", "N/A")

                        st.markdown(f"""
                            <div class="source-card">
                                <div class="source-title">[{j}] {metadata.get('word', 'N/A')}</div>
                                <div class="source-detail"><strong>Nghĩa:</strong> {metadata.get('description', 'N/A')}</div>
                                <div class="source-detail"><strong>Từ loại:</strong> {metadata.get('part_of_speech', 'N/A')}</div>
                                <div class="source-detail"><strong>Mã video:</strong> {video_id}</div>
                                <div class="source-detail"><strong><a href="{video_url}" target="_blank">Link Video Hướng Dẫn</a></strong> {video_id}</div>
                            </div>
                        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Đang suy nghĩ..."):
            try:
                # Query RAG system
                result = query_rag_system(
                    question=prompt,
                    include_sources=True,
                    top_k=3
                )

                if result["success"]:
                    # Display answer
                    answer = result["answer"]
                    st.markdown(answer)

                    # Store message with sources
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": result.get("sources", [])
                    })

                    # Display sources
                    sources = result.get("sources", [])
                    if sources:
                        with st.expander(f"📚 Xem {len(sources)} nguồn tham khảo"):
                            for j, source in enumerate(sources, 1):
                                metadata = source.get("metadata", {})
                                video_url = metadata.get("video_url")
                                has_video = metadata.get("has_video", False)
                                video_id = metadata.get("video_id", "N/A")

                                # Display source information with video link
                                video_link_html = ""
                                if has_video and video_url:
                                    view_url = metadata.get("video_view_url", video_url)
                                    video_link_html = f"""
                                        <div class="source-detail">
                                            <a href="{view_url}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">
                                                🎥 Xem video hướng dẫn →
                                            </a>
                                        </div>
                                    """
                                elif video_id != "N/A":
                                    video_link_html = f"""
                                        <div class="source-detail" style="color: #856404; font-style: italic;">
                                            ℹ️ Video {video_id} chưa có sẵn. Đang cập nhật...
                                        </div>
                                    """

                                st.markdown(f"""
                                    <div class="source-card">
                                        <div class="source-title">[{j}] {metadata.get('word', 'N/A')}</div>
                                        <div class="source-detail"><strong>Nghĩa:</strong> {metadata.get('description', 'N/A')}</div>
                                        <div class="source-detail"><strong>Từ loại:</strong> {metadata.get('part_of_speech', 'N/A')}</div>
                                        <div class="source-detail"><strong>Mã video:</strong> {video_id}</div>
                                        {video_link_html}
                                    </div>
                                """, unsafe_allow_html=True)

                    # Increment query count
                    st.session_state.query_count += 1

                else:
                    # Display error
                    error_msg = f"❌ Xin lỗi, đã xảy ra lỗi: {result.get('error', 'Unknown error')}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

            except Exception as e:
                error_msg = f"❌ Xin lỗi, đã xảy ra lỗi: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>💡 <strong>Lưu ý:</strong> Trợ lý AI chỉ cung cấp thông tin dựa trên cơ sở dữ liệu hiện có.</p>
        <p>Để có kết quả tốt nhất, hãy đặt câu hỏi rõ ràng và cụ thể.</p>
    </div>
""", unsafe_allow_html=True)
