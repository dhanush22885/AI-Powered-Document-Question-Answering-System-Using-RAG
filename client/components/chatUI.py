
import streamlit as st
from utils.api import ask_question


def apply_custom_styles():
    st.markdown(
        """
        <style>
        /* Overall application */
        .stApp {
            background: #ffffff;
            color: #172b4d;
        }

        [data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.95);
        }

        [data-testid="stAppViewContainer"] {
            background: #ffffff;
        }

        .block-container {
            max-width: 1000px;
            padding: 2rem 2rem 7rem 2rem;
        }

        /* Main heading */
        .medical-header {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 10px 0 24px 0;
            border-bottom: 1px solid #e8edf3;
            margin-bottom: 26px;
        }

        .medical-icon {
            width: 54px;
            height: 54px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            background: #e8f7f4;
            color: #087f72;
            font-size: 28px;
            flex-shrink: 0;
        }

        .medical-title {
            font-size: clamp(22px, 4vw, 30px);
            font-weight: 750;
            color: #17324d;
            line-height: 1.25;
            margin: 0;
        }

        .medical-subtitle {
            color: #718096;
            font-size: 14px;
            margin-top: 5px;
            line-height: 1.5;
        }

        /* Welcome card */
        .welcome-card {
            padding: 22px;
            background: #f7fbfa;
            border: 1px solid #e0efeb;
            border-radius: 16px;
            margin: 18px 0 24px 0;
        }

        .welcome-title {
            color: #17324d;
            font-size: 19px;
            font-weight: 650;
            margin-bottom: 8px;
        }

        .welcome-text {
            color: #617386;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            background: #ffffff;
            border: 1px solid #edf0f4;
            border-radius: 16px;
            padding: 16px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(25, 45, 70, 0.035);
        }

        [data-testid="stChatMessage"] p {
            color: #26384d;
            font-size: 15px;
            line-height: 1.75;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            background: #ffffff;
        }

        [data-testid="stChatInput"] textarea {
            color: #17324d !important;
            background: #ffffff !important;
            font-size: 15px !important;
        }

        [data-testid="stChatInput"] > div {
            border: 1px solid #dce5ec !important;
            border-radius: 18px !important;
            background: #ffffff !important;
            box-shadow: 0 5px 20px rgba(25, 45, 70, 0.07);
        }

        [data-testid="stChatInput"] > div:focus-within {
            border-color: #0d9488 !important;
            box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.10);
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            border: 1px solid #dce5ec;
            background: #ffffff;
            color: #334b62;
            font-weight: 500;
        }

        .stButton > button:hover {
            border-color: #0d9488;
            color: #087f72;
        }

        /* Error messages */
        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        /* Mobile layout */
        @media (max-width: 640px) {
            .block-container {
                padding: 1rem 0.8rem 6rem 0.8rem;
            }

            .medical-header {
                gap: 11px;
                padding-bottom: 18px;
                margin-bottom: 18px;
            }

            .medical-icon {
                width: 44px;
                height: 44px;
                font-size: 23px;
                border-radius: 12px;
            }

            .medical-subtitle {
                font-size: 12px;
            }

            .welcome-card {
                padding: 16px;
                border-radius: 13px;
            }

            [data-testid="stChatMessage"] {
                padding: 11px;
                border-radius: 13px;
            }

            [data-testid="stChatMessage"] p {
                font-size: 14px;
            }
        }
        
        /* Force chat responses and text to black */
        [data-testid="stChatMessage"],
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] div,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] h1,
        [data-testid="stChatMessage"] h2,
        [data-testid="stChatMessage"] h3,
        [data-testid="stChatMessage"] strong,
        [data-testid="stChatMessage"] em {
            color: #000000 !important;
        }

        /* Make code and inline code readable */
        [data-testid="stChatMessage"] code,
        [data-testid="stChatMessage"] pre {
            color: #000000 !important;
            background-color: #f3f4f6 !important;
        }

        /* Keep chat input text black */
        [data-testid="stChatInput"] textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
        }

        /* Keep placeholder text visible */
        [data-testid="stChatInput"] textarea::placeholder {
            color: #666666 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_chat():
    apply_custom_styles()

    # Professional header
    st.markdown(
        """
        <div class="medical-header">
            <div class="medical-icon">✚</div>
            <div>
                <div class="medical-title">RAG Based Assistant</div>
                <div class="medical-subtitle">
                    Your intelligent assistant for uploaded information
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Welcome screen for a new conversation
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="welcome-card">
                <div class="welcome-title">
                    Hello! How can I help you today?
                </div>
                <p class="welcome-text">
                    Ask a question about your uploaded documents.
                    I'll use the available document information to help
                    you understand the answer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Start by asking a question below.")

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Question input
    user_input = st.chat_input(
        "Ask a question about your uploaded documents..."
    )

    if user_input:
        # Display and save user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Call existing FastAPI integration
        with st.chat_message("assistant"):
            with st.spinner("Reviewing your question..."):
                try:
                    response = ask_question(user_input)

                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get(
                            "response",
                            "I couldn't generate an answer."
                        )

                        st.markdown(answer)

                        sources = data.get("sources", [])
                        if sources:
                            with st.expander("View sources"):
                                for src in sources:
                                    st.markdown(f"- {src}")

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )
                    else:
                        st.error(
                            f"Unable to get an answer "
                            f"(HTTP {response.status_code})."
                        )
                        st.caption(response.text)

                except Exception as e:
                    st.error(
                        "Unable to connect to the Assistant. "
                        "Please check that the backend is running."
                    )
                    st.caption(str(e))
