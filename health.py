from dotenv import load_dotenv
load_dotenv()  # loads all environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get a response
def get_response(input_text, image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Calling model
    # Sending image and prompt to the model
    response = model.generate_content([input_text, image_data, prompt])
    return response.text

# Function to handle image upload and conversion to base64
def input_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Resize the image to a smaller size (e.g., 224x224)
        resized_image = image.resize((224, 224))
        
        # Convert image to bytes in a proper format (JPEG)
        buffered = io.BytesIO()
        resized_image.save(buffered, format="JPEG")
        bytes_data = buffered.getvalue()

        # Convert bytes to base64 string
        base64_image = base64.b64encode(bytes_data).decode("utf-8")

        image_parts = {
            "mime_type": "image/jpeg",
            "data": base64_image
        }
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Calorie Counter")

input_text = st.text_input("Input prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

submit = st.button("Tell me the amount of calories included")

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image,
calculate the total calories, and provide details of each food item with calorie intake
in the following format:
1. Item 1 name = number of calories
2. Item 2 name = number of calories
3. Item 3 name = number of calories
---
---
"""

# If the submit button is clicked
if submit:
    image_data = input_image(uploaded_file)
    response = get_response(input_text, image_data, input_prompt)
    st.subheader("The response is")
    st.write(response)
