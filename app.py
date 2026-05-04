import streamlit as st
import keras                                              # ✅ FIXED: use keras directly
import pickle
from keras.preprocessing.sequence import pad_sequences   # ✅ FIXED: from keras, not tensorflow.keras

# --- 1. TAB SETTINGS ---
# This changes what the tab looks like at the very top of your web browser.
st.set_page_config(page_title="Review Checker", page_icon="🕵️‍♀️", layout="centered")

# --- 2. BACKGROUND DESIGN STUFF ---
# This section holds the design instructions to make our button big and red, 
# and creates the animation for the floating sad faces. 
st.markdown("""
    <style>
    /* Making the "Analyze" button massive and red */
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
    
    /* Creating the rules for how the sad faces float up the screen */
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

# --- 3. OUR CUSTOM SAD FACE LAUNCHER ---
# When we run this block, it drops five sad faces at the bottom of the screen 
# and tells them to float up at slightly different speeds.
def show_sad_faces():
    html_code = """
        <div class="sad-emoji" style="left: 10%; animation-delay: 0s;">😢</div>
        <div class="sad-emoji" style="left: 30%; animation-delay: 0.2s;">😞</div>
        <div class="sad-emoji" style="left: 50%; animation-delay: 0.5s;">👎</div>
        <div class="sad-emoji" style="left: 70%; animation-delay: 0.1s;">😭</div>
        <div class="sad-emoji" style="left: 90%; animation-delay: 0.4s;">😡</div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# --- 4. THE REAL AI BRAIN TRANSPLANT ---
# This connects the website to the files your teammate baked in Google Colab!

@st.cache_resource 
def load_brain():
    # ✅ FIXED: use keras.models instead of tf.keras.models
    model = keras.models.load_model('my_model.keras')
    
    # This connects the dictionary file:
    with open('tokenizer.pkl', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    return model, tokenizer

# Wake up the brain!
real_model, real_tokenizer = load_brain()

def analyze_sentiment(user_text):
    # Turn the user's text into numbers
    sequence = real_tokenizer.texts_to_sequences([user_text])
    
    # Pad it so it's exactly 200 numbers long to match the AI's brain!
    padded_sequence = pad_sequences(sequence, maxlen=200, padding='post')
    
    # Ask the AI to grade it!
    prediction = real_model.predict(padded_sequence)[0][0]
    
    if prediction >= 0.5:
        return "Positive review"
    else:
        return "Negative review"

# --- 5. BUILDING THE ACTUAL WEBSITE INTERFACE ---
st.markdown("<h1 style='text-align: center;'>✨ Amazon Review Sentiment Analyzer ✨</h1>", unsafe_allow_html=True)
st.subheader("Did they love it or hate it? Let the AI decide! 🤖")
st.write("---") 

user_input = st.text_area("✍️ Type or paste a product review below:", height=150)

if st.button("🚨 ANALYZE SENTIMENT 🚨"):
    if user_input: 
        result = analyze_sentiment(user_input)
        
        st.write("---")
        st.markdown("### 🥁 Drumroll please...")
        
        if result == "Positive review":
            st.success("🌟 Outcome: Positive review") 
            st.balloons() 
        else:
            st.error("🚩 Outcome: Negative review") 
            show_sad_faces() 
    else:
        st.warning("Oops! 🛑 Please enter a review first!")
