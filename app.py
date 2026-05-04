import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
    @keyframes floatUp {
        0% { bottom: -50px; opacity: 1; transform: translateX(0px); }
        100% { bottom: 100vh; opacity: 0; transform: translateX(-30px); }
    }
    .sad-emoji {
        position: fixed;
        font-size: 40px;
        z-index: 999999;
        animation: floatUp 3s ease-in forwards;
    }
    </style>
""", unsafe_allow_html=True)

def show_sad_faces():
    html_code = """
        <div class="sad-emoji" style="left: 10%; animation-delay: 0s;">😢</div>
        <div class="sad-emoji" style="left: 30%; animation-delay: 0.2s;">😞</div>
        <div class="sad-emoji" style="left: 50%; animation-delay: 0.5s;">👎</div>
        <div class="sad-emoji" style="left: 70%; animation-delay: 0.1s;">😭</div>
        <div class="sad-emoji" style="left: 90%; animation-delay: 0.4s;">😡</div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

@st.cache_resource
def load_brain():
    model = tf.keras.models.load_model("my_model.keras")

    with open("tokenizer.pkl", "rb") as handle:
        tokenizer = pickle.load(handle)

    return model, tokenizer

real_model, real_tokenizer = load_brain()

def analyze_sentiment(user_text):
    sequence = real_tokenizer.texts_to_sequences([user_text])
    padded_sequence = pad_sequences(sequence, maxlen=200, padding="post")
    prediction = real_model.predict(padded_sequence, verbose=0)[0][0]

    if prediction >= 0.5:
        return "Positive review", prediction
    else:
        return "Negative review", prediction

st.markdown("<h1 style='text-align: center;'>✨ Amazon Review Sentiment Analyzer ✨</h1>", unsafe_allow_html=True)
st.subheader("Did they love it or hate it? Let the AI decide! 🤖")
st.write("---")

user_input = st.text_area("✍️ Type or paste a product review below:", height=150)

if st.button("🚨 ANALYZE SENTIMENT 🚨"):
    if user_input.strip():
        result, confidence = analyze_sentiment(user_input)

        st.write("---")
        st.markdown("### 🥁 Drumroll please...")

        if result == "Positive review":
            st.success(f"🌟 Outcome: Positive review")
            st.write(f"Model score: {confidence:.3f}")
            st.balloons()
        else:
            st.error(f"🚩 Outcome: Negative review")
            st.write(f"Model score: {confidence:.3f}")
            show_sad_faces()
    else:
        st.warning("Oops! 🛑 Please enter a review first!")
