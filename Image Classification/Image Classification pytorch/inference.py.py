import streamlit as st
import torch
from torch import nn
import numpy as np
from PIL import Image
import io

# Page config must be first
st.set_page_config(page_title="Fashion MNIST Inference", layout="centered")

# Class names
class_names = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

# Model definition
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# Main app
def main():
    st.title("👗 Fashion MNIST Classifier")
    
    # Check if we can create a model (basic functionality test)
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        st.write(f"Device: {device}")
        
        # Try to create model instance
        model = NeuralNetwork()
        st.success("✅ Model architecture loaded successfully")
        
    except Exception as e:
        st.error(f"❌ Error creating model: {str(e)}")
        return
    
    # Simple file uploader
    st.write("Upload an image for classification:")
    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        try:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=200)
            
            # Convert to grayscale and resize
            image_gray = image.convert('L')
            image_resized = image_gray.resize((28, 28))
            
            # Convert to tensor
            image_array = np.array(image_resized) / 255.0
            image_tensor = torch.FloatTensor(image_array).unsqueeze(0).unsqueeze(0)
            
            st.write("Image processed successfully!")
            st.write(f"Image tensor shape: {image_tensor.shape}")
            
            # Show processed image
            st.image(image_resized, caption="Processed (28x28 grayscale)", width=100)
            
            # Make a dummy prediction (since we don't have the trained weights)
            with torch.no_grad():
                output = model(image_tensor.view(1, -1))
                predicted_class = torch.argmax(output, dim=1).item()
            
            st.write(f"**Predicted Class:** {class_names[predicted_class]}")
            st.write("(Note: This is using an untrained model, so predictions are random)")
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    # Simple button test
    if st.button("Test Button"):
        st.write("Button clicked successfully!")
    
    # Info section
    st.write("---")
    st.write("**App Status:** Running successfully")
    st.write("**PyTorch Version:**", torch.__version__)

if __name__ == "__main__":
    main()