import streamlit as st
import pickle
import re

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Amazon Review Sentiment Analyzer",
    page_icon="🕵️‍♀️",
    layout="centered"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }

    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ef4444, #dc2626);
        color: white;
        font-size: 22px;
        height: 3em;
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 12px rgba(220, 38, 38, 0.35);
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #dc2626, #991b1b);
        color: white;
        border: none;
    }

    @keyframes floatUp {
        0% { bottom: -50px; opacity: 1; transform: translateX(0px); }
        100% { bottom: 100vh; opacity: 0; transform: translateX(-30px); }
    }

    .sad-emoji {
        position: fixed;
        font-size: 42px;
        z-index: 999999;
        animation: floatUp 3s ease-in forwards;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TEXT CLEANING FUNCTION
# --------------------------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --------------------------------------------------
# NEGATIVE REVIEW ANIMATION
# --------------------------------------------------
def show_sad_faces():
    html_code = """
        <div class="sad-emoji" style="left: 10%; animation-delay: 0s;">😢</div>
        <div class="sad-emoji" style="left: 30%; animation-delay: 0.2s;">😞</div>
        <div class="sad-emoji" style="left: 50%; animation-delay: 0.5s;">👎</div>
        <div class="sad-emoji" style="left: 70%; animation-delay: 0.1s;">😭</div>
        <div class="sad-emoji" style="left: 90%; animation-delay: 0.4s;">😡</div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------
@st.cache_resource
def load_sentiment_model():
    with open("sentiment_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

sentiment_model = load_sentiment_model()

# --------------------------------------------------
# USER INTERFACE
# --------------------------------------------------
st.markdown("<div class='title'>✨ Amazon Review Sentiment Analyzer ✨</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Enter a product review and let the machine learning model classify it as positive or negative.</div>",
    unsafe_allow_html=True
)

st.write("---")

user_input = st.text_area(
    "✍️ Type or paste a product review below:",
    height=170,
    placeholder="Example: This product is amazing and works exactly as expected!"
)

analyze_button = st.button("🚨 ANALYZE SENTIMENT 🚨")

# --------------------------------------------------
# PREDICTION LOGIC
# --------------------------------------------------
if analyze_button:
    if user_input.strip():
        cleaned_input = clean_text(user_input)

        prediction = sentiment_model.predict([cleaned_input])[0]
        probability = sentiment_model.predict_proba([cleaned_input])[0]

        negative_probability = probability[0]
        positive_probability = probability[1]

        st.write("---")
        st.markdown("### 🥁 Analysis Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Negative Probability",
                value=f"{negative_probability:.2%}"
            )

        with col2:
            st.metric(
                label="Positive Probability",
                value=f"{positive_probability:.2%}"
            )

        if prediction == 1:
            st.success("🌟 Outcome: Positive Review")
            st.balloons()
        else:
            st.error("🚩 Outcome: Negative Review")
            show_sad_faces()

        st.caption(
            "Note: This model uses TF-IDF vectorisation and Logistic Regression trained on labelled review text."
        )

    else:
        st.warning("Please enter a review before clicking the analysis button.")
