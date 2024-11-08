import streamlit as st
import os
from groq import Groq
from gtts import gTTS
import tempfile
import asyncio

# Initialize the Groq client with API key
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

st.title("Vaccine Info Pakistan Chatbot")

# User input
user_input = st.text_input("Ask about Pakistan's Vaccine Program verified by WHO")

if user_input:
    # Make a chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
            {
                "role": "assistant",
                "content": "Provide brief information in layman language on vaccines available in Pakistan according to WHO standards. Also share the list of Hospitals in Karachi, Pakistan who provide Government Vaccines. If query is not related to vaccine simply say 'I am sorry, I can only provide information regarding vaccines'"
            }
        ],
        model="llama-3.2-11b-text-preview",
    )

    # Retrieve and display the response text
    response_text = chat_completion.choices[0].message.content.strip()
    if response_text:
        st.write("Response:", response_text)
        
    # Define async function for text-to-audio conversion
        async def convert_text_to_audio(text):
            tts = gTTS(text=response_text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                tts.save(temp_audio_file.name)
                temp_audio_file_path = temp_audio_file.name
                return temp_audio_file_path

    # Play the bot's response as audio
        audio_file_path = asyncio.run(convert_text_to_audio(response_text))
        if audio_file_path:
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
                st.audio(audio_data, format="audio/mp3")
        else:
            st.error("Failed to convert text to speech.")
    else:
        st.write("The response was empty. Please try asking your question again.")
