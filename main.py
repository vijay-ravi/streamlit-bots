import base64
from openai import OpenAI
from os import getenv
from PIL import Image
import io
import streamlit as st

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)           
        

# Function to encode the image
def image_to_base64(image):
    """Converts a PIL image to a base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

system_prompt = """
You are bot who predicts the exact age of the person in an image. 
You must give the exact age and not something like "late 20's" or "early 30s" 

"""

def insultBot(image):
    base64_image = image_to_base64(image)
    completion = client.chat.completions.create(
    model="google/gemini-pro-vision",
    messages=[
        {
        "role": "system",
        "content": system_prompt,
        },
        {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Predict the age of this person. Output an exact number. No guessing. Answer like this: 'You are 35 years old.'"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
    ],
    )
    response = completion.choices[0].message.content

    return response



st.title("🤔 Am I 21?")
st.write("😈 A Google Gemini bot.")

st.markdown("""
Want to learn how to do this? - [Connect with me](https://beacons.ai/vijayxtech) @vijayxtech.
""")


# Streamlit code to upload an image


uploaded_file = st.file_uploader("Upload your image:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(io.BytesIO(uploaded_file.getvalue()))
    st.image(image, caption='Your Image.', use_column_width=True)
    st.write("Processing. Hold on!...")

    response = insultBot(image)
    st.write(response)
    st.write(".....")