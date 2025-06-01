import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Page config
st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾")

# Simple styling
st.markdown("""
<style>
.prediction-box {
    background: #f0f2f6;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
    margin: 1rem 0;
}
.confidence-high { color: #28a745; }
.confidence-medium { color: #ffc107; }
.confidence-low { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_classifier_model():
    try:
        return load_model("cat_vs_dog.h5")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model = load_classifier_model()

# Main UI
st.title("🐾 Cat vs Dog Classifier")
st.write("Upload an image and get instant AI prediction")

# File upload
uploaded_file = st.file_uploader(
    "Choose an image", 
    type=["jpg", "jpeg", "png"],
    help="Upload a clear photo of a cat or dog"
)

if uploaded_file is not None:
    # Display image
    img = Image.open(uploaded_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(img, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        # Process image
        with st.spinner("Analyzing..."):
            # Preprocess
            img_resized = img.resize((224, 224))
            img_array = image.img_to_array(img_resized)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Predict
            prediction = model.predict(img_array, verbose=0)
            class_names = ["Cat", "Dog"]
            class_index = np.argmax(prediction)
            confidence = float(np.max(prediction)) * 100
            
            # Display result
            animal = class_names[class_index]
            emoji = "🐱" if animal == "Cat" else "🐶"
            
            # Confidence styling
            if confidence > 80:
                conf_class = "confidence-high"
                conf_text = "High"
            elif confidence > 60:
                conf_class = "confidence-medium"  
                conf_text = "Medium"
            else:
                conf_class = "confidence-low"
                conf_text = "Low"
        
        # Result display
        st.markdown(f"""
        <div class="prediction-box">
            <h2>{emoji} {animal}</h2>
            <p>Confidence: <span class="{conf_class}">{confidence:.1f}% ({conf_text})</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick probabilities
        st.progress(confidence/100)
        
        cat_prob = prediction[0][0] * 100
        dog_prob = (100 - cat_prob) if len(prediction[0]) == 1 else prediction[0][1] * 100
        
        st.write(f"🐱 Cat: {cat_prob:.1f}%")
        st.write(f"🐶 Dog: {dog_prob:.1f}%")