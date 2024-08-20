import streamlit as st
import base64
import openai

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Setup API key
api_key = st.secrets["API_KEY"]
openai.api_key = api_key

# Setup aplikasi
st.set_page_config(page_title="Image Recognition", layout="centered", initial_sidebar_state="collapsed")
st.title("Image Recognition with OpenAI Vision API")

# Upload gambar
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Tampilkan gambar yang di upload
    with st.expander("Image", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

analyze_button = st.button("Identifikasi Gambar", type="secondary")

if uploaded_file is not None and analyze_button:
    base64_image = encode_image(uploaded_file)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Berapa angka yang muncul pada meteran tersebut, fokus pada meteran saja untuk mendapatkan hasil yang akurat."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]

    try:
        # Stream the response
        full_response = ""
        message_placeholder = st.empty()
        for completion in openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages, 
            max_tokens=1200, stream=True
        ):
            # Check if there is content to display
            if completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        # Final update to placeholder after the stream ends
        message_placeholder.markdown(full_response)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    # Warnings for user action required
    if not uploaded_file and analyze_button:
        st.warning("Please upload an image.")
