import requests
import streamlit as st
import json

def get_groq_response(user_input, target_language):
    chain_input = {
        "language": target_language,  
        "text": user_input     
    }

    json_body = {
        "input": chain_input,
        "config": {},
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/chain/invoke",
            json=json_body
        )

        if response.status_code != 200:
            st.error(f"API Error: Status Code {response.status_code}")
            st.json(response.json())
            return {"output": "Error: Check API server logs and the JSON body format."}

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("Connection Error: The LangServe API server is not running or is inaccessible.")
        return {"output": "Error: API server connection failed."}

st.title("LLM Language Translator (LCEL API)")

target_language = st.selectbox(
    "Select the language you want to translate to:",
    ("French", "Spanish", "German", "Japanese", "Hindi", "English")
)

input_text = st.text_area("Enter the text you want to translate:", height=100)

if st.button("Translate"):
    if input_text:
        with st.spinner(f'Translating to {target_language}...'):
            result = get_groq_response(input_text, target_language)
            
            if 'output' in result:
                st.success(f"Translation in {target_language}:")
                st.write(result['output'])
            else:
                st.error("Received unexpected response format from API.")
                st.json(result)
    else:
        st.warning("Please enter some text to translate.")
