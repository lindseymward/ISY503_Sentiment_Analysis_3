import streamlit as st

# --- 1. TAB SETTINGS ---
# This changes what the tab looks like at the very top of your web browser.
st.set_page_config(page_title="Review Checker", page_icon="🕵️‍♀️", layout="centered")

# --- 2. BACKGOUND DESIGN STUFF ---
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


# --- 4. THE TEMPORARY "DUMMY" BRAIN ---
# Because your teammate is still building the real AI, we are using this fake one.
# It just looks at the user's text and searches for happy words. 
def analyze_sentiment(user_text):
    # Make the user's text all lowercase so it's easier to check
    text_to_check = user_text.lower()
    
    if "good" in text_to_check or "love" in text_to_check or "great" in text_to_check:
        return "Positive review"
    else:
        return "Negative review"

# --- 5. BUILDING THE ACTUAL WEBSITE ---

# We use a little design trick here to force the main title to sit directly in the center
st.markdown("<h1 style='text-align: center;'>✨ Amazon Review Sentiment Analyzer ✨</h1>", unsafe_allow_html=True)

# Add a smaller subtitle directly below it
st.subheader("Did they love it or hate it? Let the AI decide! 🤖")
st.write("---") 

# Create the text box for people to type their reviews into
user_input = st.text_area("✍️ Type or paste a product review below:", height=150)

# Create the button, and check if someone clicked it
if st.button("🚨 ANALYZE SENTIMENT 🚨"):
    
    # If they clicked the button AND typed something in the box...
    if user_input: 
        
        # Send their text to our dummy brain to get an answer
        result = analyze_sentiment(user_input)
        
        st.write("---")
        st.markdown("### 🥁 Drumroll please...")
        
        # If the brain says it's positive, show a green message and launch balloons!
        if result == "Positive review":
            st.success("🌟 Outcome: Positive review") 
            st.balloons() 
            
        # If the brain says it's negative, show a red message and launch sad faces!
        else:
            st.error("🚩 Outcome: Negative review") 
            show_sad_faces() 
            
    # If they clicked the button but left the text box empty...
    else:
        st.warning("Oops! 🛑 Please enter a review first!")