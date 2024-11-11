import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to generate session note based on chosen format
def generate_note(input_text, format_type):
    # Set up the OpenAI API key (ensure you have an appropriate API key)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    openai.api_key = api_key

    # Define prompt for the specific note type
    if format_type == "DAP":
        prompt_content = (
            f"Take the following psychotherapy session note and convert it to a {format_type} formatted session note.\n\n"
            f"The format should consist of the following parts:\n"
            f"1. Data: Description of the client's presentation, statements, and observations.\n"
            f"2. Assessment: Your clinical assessment of the situation, including the client's progress and response to treatment.\n"
            f"3. Plan: The plan for future treatment or actions.\n\n"
            f"Session Note:\n{input_text}"
        )
    elif format_type == "SIRP":
        prompt_content = (
            f"Take the following psychotherapy session note and convert it to a {format_type} formatted session note.\n\n"
            f"The format should consist of the following parts:\n"
            f"1. Situation: The primary issues or concerns discussed during the session.\n"
            f"2. Intervention: The interventions or techniques used during the session.\n"
            f"3. Response: The client's response to the interventions.\n"
            f"4. Plan: The plan for the next steps in treatment.\n\n"
            f"Session Note:\n{input_text}"
        )
    elif format_type == "SOAP":
        prompt_content = (
            f"Take the following psychotherapy session note and convert it to a {format_type} formatted session note.\n\n"
            f"The format should consist of the following parts:\n"
            f"1. Subjective: The client's subjective experience, including their statements and concerns.\n"
            f"2. Objective: Observable facts, including the clinician's observations and measurable data.\n"
            f"3. Assessment: The clinician's assessment of the client's progress, symptoms, and overall status.\n"
            f"4. Plan: The future plan for treatment, including any homework or follow-up steps.\n\n"
            f"Session Note:\n{input_text}"
        )
    elif format_type == "BS":
        prompt_content = (
            f"Take the following psychotherapy session note and convert it to a {format_type} formatted session note.\n\n"
            f"The format should consist of the following parts:\n"
            f"1. Presenting Issues: The primary issues or concerns presented by the client during the session.\n"
            f"2. Response to Treatment: The client's response to the interventions or techniques used during the session.\n\n"
            f"Session Note:\n{input_text}"
        )
    else:
        prompt_content = (
            f"Take the following psychotherapy session note and convert it to a {format_type} formatted session note:\n\n{input_text}"
        )

    messages = [
        {"role": "system", "content": "You are a helpful assistant that formats psychotherapy session notes."},
        {"role": "user", "content": prompt_content}
    ]

    # Make the call to OpenAI GPT-3.5 Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    # Get the response text and return it
    return response.choices[0].message['content'].strip()

# Streamlit App GUI
st.title('Psychotherapy Session Note Formatter')

# Text input for the original session note
input_text = st.text_area("Enter the psychotherapy session note:", height=200)

# Dropdown menu to select the output format type
format_type = st.selectbox("Select the output format for the session note:", ["DAP", "SIRP", "SOAP", "BS"])

# Generate button
if st.button("Generate Formatted Note"):
    if input_text.strip() == "":
        st.warning("Please enter a session note to proceed.")
    else:
        try:
            # Generate and display formatted session note
            formatted_note = generate_note(input_text, format_type)
            st.subheader("Formatted Session Note:")
            st.text_area("Generated Note", formatted_note, height=200, label_visibility='hidden')
        except ValueError as e:
            st.error(str(e))
        except openai.error.AuthenticationError:
            st.error("Authentication failed. Please check your OpenAI API key.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# Streamlit sidebar info for users
st.sidebar.title("About")
st.sidebar.info(
    "This app allows you to take a basic psychotherapy session note and convert it into a structured note format such as DAP, SIRP, SOAP, or BS. "
    "Simply enter your session note, select the desired format, and generate the formatted note.")
 
