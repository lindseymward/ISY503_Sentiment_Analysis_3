import streamlit as st
import pickle
import re

st.set_page_config(page_title="Review Checker", page_icon="🕵️‍♀️", layout="centered")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        font-size: 22px;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        border: 2px solid #cc0000;
    }
    div.stButton > button:hover {
        background-color: #cc0000;
        border: 2px solid #990000;
    }
    </style>
""", unsafe_allow_html=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

@st.cache_resource
def load_model():
    with open("sentiment_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

sentiment_model = load_model()

st.markdown("<h1 style='text-align: center;'>✨ Amazon Review Sentiment Analyzer ✨</h1>", unsafe_allow_html=True)
st.subheader("Did they love it or hate it? Let the AI decide! 🤖")
st.write("---")

user_input = st.text_area("✍️ Type or paste a product review below:", height=150)

if st.button("🚨 ANALYZE SENTIMENT 🚨"):
    if user_input.strip():
        cleaned_input = clean_text(user_input)

        prediction = sentiment_model.predict([cleaned_input])[0]
        probability = sentiment_model.predict_proba([cleaned_input])[0]

        st.write("---")
        st.markdown("### 🥁 Result")

        st.write(f"Negative probability: {probability[0]:.4f}")
        st.write(f"Positive probability: {probability[1]:.4f}")

        if prediction == 1:
            st.success("🌟 Outcome: Positive review")
            st.balloons()
        else:
            st.error("🚩 Outcome: Negative review")

    else:
        st.warning("Oops! 🛑 Please enter a review first!")
