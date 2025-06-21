import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Configure page
st.set_page_config(
    page_title="Cat & Dog Classifier",
    page_icon="🐱🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Consistent color scheme
st.markdown(
    """
    <style>
    :root {
        --primary: #4A6FA5;
        --secondary: #166088;
        --accent: #4FC3F7;
        --background: #F8F9FA;
        --text: #333333;
    }
    
    body {
        background-color: var(--background);
    }
    
    .uploadedImage {
        border-radius: 12px;
        border: 2px solid var(--secondary);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 0 auto;
        display: block;
        max-width: 100%;
    }
    
    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: white;
        color: var(--text);
        text-align: center;
        margin: 1.5rem auto;
        border: 2px solid var(--accent);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 400px;
    }
    
    .title {
        text-align: center;
        margin-bottom: 1.5rem;
        color: var(--primary);
    }
    
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: var(--secondary);
        font-size: 0.9rem;
    }
    
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    .stFileUploader>div>div>div>div {
        border: 2px dashed var(--secondary);
        border-radius: 8px;
        background: rgba(74, 111, 165, 0.05);
    }
    
    .stSpinner>div>div {
        border-top-color: var(--accent);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load model
@st.cache_resource
def load_model_cached():
    try:
        return load_model("cat_dog_model.keras")
    except Exception as e:  
        st.error(f"Failed to load model: {e}")
        return None

model = load_model_cached()
if model is None:
    st.stop()

# Title
st.markdown('<h1 class="title">🐱 Cat vs Dog Classifier 🐶</h1>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload a cat or dog image",
    type=["jpg", "jpeg", "png"],
    help="Supports JPG, JPEG, PNG formats"
)

if uploaded_file:
    try:
        img = Image.open(uploaded_file)
        
        # Display image with consistent styling
        st.image(img, caption="Uploaded Image", use_container_width=True, output_format="JPEG")
        
        # Preprocess image for model
        img_resized = img.convert('RGB').resize((160, 160))
        arr = np.array(img_resized) / 255.0
        arr = arr[np.newaxis, ...]
        
        # Predict
        with st.spinner("Analyzing image..."):
            score = float(model.predict(arr)[0][0])
        
        label = "Dog 🐶" if score > 0.5 else "Cat 🐱"
        confidence = score * 100 if score > 0.5 else (1 - score) * 100
        
        # Display result
        st.markdown(
            f"""
            <div class="result-card">
                <h3 style="color: var(--primary); margin-bottom: 0.5rem;">{label}</h3>
                <p style="color: var(--secondary); font-size: 1.1rem;">Confidence: <strong>{confidence:.1f}%</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
else:
    st.info("Upload an image to classify")

# Footer
st.markdown('<div class="footer">ResNet50 model | Threshold: 0.5</div>', unsafe_allow_html=True)