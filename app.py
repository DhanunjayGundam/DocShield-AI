import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="DocShield AI", page_icon="🛡️")
st.title("🛡️ DocShield AI - Document Red Flag Detector")

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {e}")
        return ""

def check_for_red_flags(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" if you don't have GPT-4 access
            messages=[{
                "role": "user",
                "content": f"""
You are a compliance expert. Scan the following trade finance document for anti-boycott language or red flags that might violate international trade laws or internal policy.

Document:
{text}

List the red flags with explanations if found.
"""
            }],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error during OpenAI request: {e}")
        return ""

# Upload and process file
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    with st.spinner("Analyzing document..."):
        text = extract_text_from_pdf(uploaded_file)
        if text:
            result = check_for_red_flags(text)
            st.success("✅ Analysis complete!")
            st.markdown("### 🧾 Findings:")
            st.write(result)
