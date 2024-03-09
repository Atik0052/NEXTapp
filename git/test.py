import base64
import pandas as pd
import streamlit as st
import openai
import os
import time
import json
import PyPDF2
import docx
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import GPT2Config
import torch



# Set up OpenAI GPT-3.5 API
openai.api_key = "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"  # Replace with your API key\

# Specify the path
model_path = "D:\\AISHA\\fine_tuned_gpt2"

# Load configuration and model
config = GPT2Config.from_json_file(os.path.join(model_path, 'config.json'))
model = GPT2LMHeadModel(config)
model.load_state_dict(torch.load(os.path.join(model_path, 'pytorch_model.bin')))

# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2') 


# SessionState class to maintain state across reruns
class SessionState(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
# Function to save conversation to a file

def get_session_state():
    if not hasattr(st, '_session_state'):
        st._session_state = SessionState(conversations=[])
    if not hasattr(st._session_state, 'uploaded_file'):
        st._session_state.uploaded_file = None
    if not hasattr(st._session_state, 'file_uploader_key'):
        st._session_state.file_uploader_key = 0  # Initialize with any number
    if not hasattr(st._session_state, 'show_feedback_bar'):
        st._session_state.show_feedback_bar = False  # Initialize as False
    return st._session_state

# Initialize conversation with ChatGPT
def initialize_conversation(text):
    conversation = [
        {"role": "system", "content": "You are AISHA, sales assistant for Message Central."},
        {"role": "user", "content": text + "Don't use words like Virtual AI while describing about aisha"+"Always behave as a human(individual person) Aisha gupta who works as a sales assistent at message central"   }
    ]

    return conversation   

def save_conversation_to_file(state, file_path):
    conversation_data = {"messages": []}

    for i in range(0, len(state.conversations), 3):
        user_message = state.conversations[i]
        if i + 1 < len(state.conversations):  # Check if index is valid
            assistant_message = state.conversations[i + 1]
        else:
            break  # Exit the loop if the index is not valid

        
        # Only proceed if feedback is available
        if i + 2 < len(state.conversations) and state.conversations[i + 2]["role"] == "feedback":
            feedback_message = state.conversations[i + 2]
            
            # Include the user's question
            conversation_data["messages"].append({"role": "user", "content": user_message["content"]})
            
            # Combine the assistant's response with feedback
            content = assistant_message["content"] + "\nFeedback: " + feedback_message["content"]
            conversation_data["messages"].append({"role": "assistant", "content": content})

    # Save the structured data to a file
    # with open(file_path, "w") as file:
    #     json.dump(conversation_data, file)


    try:
        with open(file_path, "w") as file:
            json.dump(conversation_data, file)
        st.write(f"File saved to {file_path}")
    except Exception as e:
        st.write(f"Error saving file: {e}")


def get_bot_response(conversation, temperature=0.7, max_length=50):

    input_text = conversation[-1]["content"]  # Get the last user message
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_length, temperature=temperature, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)  # Decode and skip the input part
    return response

def chat_with_bot(question, state, feedback=None):
    # Retrieve the existing context
    existing_context = st.session_state.get("context", "")
    
    # Create a new conversation with the current question
    conversation = initialize_conversation(question)
    
    # If feedback is provided, add it to the conversation as a user message
    if feedback:
        conversation.append({"role": "user", "content": feedback})
    
    # Break the input into smaller chunks (using a simple approach of just limiting string length for now)
    max_chunk_length = 4000  # Set a safe number slightly lower than 4097 tokens
    chunks = [question[i:i+max_chunk_length] for i in range(0, len(question), max_chunk_length)]
    
    all_responses = []

    for chunk in chunks:
        conversation[-1]["content"] = chunk  # Replace the last user message with the current chunk
        chat_response = get_bot_response(conversation)  # Removed extra arguments here
        all_responses.append(chat_response)

    # Join all responses to get the final response
    final_response = " ".join(all_responses)
    
    # Append only the assistant's response to the conversation
    state.conversations.append({"role": "assistant", "content": final_response})


    # Check if there's an uploaded file and append its content and name to the conversation
    uploaded_file = st.session_state.get("uploaded_file")
    if uploaded_file:
        state.conversations.append({"role": "user", "content": uploaded_file.name})
        state.conversations.append({"role": "assistant", "content": final_response})  # Here, final_response will have the file content

    # Update the context for the session with the combined content (including feedback)
    combined_content = question + " " + final_response
    if feedback:
        combined_content += " " + feedback
    st.session_state.context = combined_content

    # Save the conversation to file
    save_conversation_to_file(state, "D:\AISHA\cpaas-tools\conversation.json")


def display_chat(state):
    st.markdown("### Chat History")
    
    for message in state.conversations:
        # st.markdown('---') 
        if message["role"] == "user":
            st.markdown(f'**You:** {message["content"]}')
        elif message["role"] == "assistant":
            st.markdown(f'**AISHA:** {message["content"]}')
        elif message["role"] == "feedback":
            st.markdown(f'**Feedback:** {message["content"]}')
            st.markdown('---') 
        
    st.markdown('---') 
            # feedback_message = message["content"]

    

def main():
    state = get_session_state()

    st.title("Chat with AISHA")

    display_chat(state)

    feedback_input_container = st.empty()  # Create an empty container for feedback input
    feedback_bar_container = st.empty()  # Create an empty container for the feedback bar
    
    # Check if it's a refresh
    if st.session_state.get('refresh'):
        # Anchor to jump to upon refresh
        st.markdown("<a id='user_input'></a>", unsafe_allow_html=True)

    # Use the session_state to keep the user input
    user_input = st.text_input("You:", value=st.session_state.get("user_input_state", ""), key="user_input")
    
    # Store the current user input in session state for future reference
    st.session_state.user_input_state = user_input

    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"], key=f"file_uploader_{state.file_uploader_key}")

    ask_button = st.button("Ask", key="ask_button")

    if state.show_feedback_bar:
        # Feedback input
        feedback_input = feedback_input_container.text_area("Provide feedback or corrections to the bot's response:")
        feedback_submit = feedback_bar_container.button("Provide Feedback")

        if feedback_submit:
            if feedback_input:
                feedback_message = feedback_input
                state.conversations.append({"role": "feedback", "content": feedback_message})
                feedback_input = "" 
            state.show_feedback_bar = False  # Hide the feedback bar after providing feedback

    if ask_button:
        combined_input = ""

        context = st.session_state.get("context", "")  # Get stored context

        if uploaded_file:
            if uploaded_file.type == "text/plain":  # For text files
                file_contents = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":  # For PDF files
                # Use PyPDF2 to extract text from the PDF
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                file_contents = ""
                for page in pdf_reader.pages:
                    file_contents += page.extract_text()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # For .docx files
                doc = docx.Document(uploaded_file)
                file_contents = " ".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                file_contents = ""

            # Add the extracted content to the combined_input
            if combined_input:
                combined_input += "\n"  # Separate the user input and file content by a newline
            combined_input += file_contents

            context += " " + file_contents  # Add file contents to context
            st.session_state.context = context  # Store context in session state

        if user_input:
            if combined_input:
                combined_input += ", "  # Separate the file content and user input with a comma
            combined_input += user_input

        # Append the combined_input to the state.conversations list once
        if combined_input:
            state.conversations.append({"role": "user", "content": combined_input})
            
            # Generate a unique key based on the question or timestamp
            unique_key = f"feedback_input_{int(time.time())}"  # Use timestamp as a unique key
            # Check if feedback is provided
            feedback_input = st.text_area("Provide feedback or corrections to the bot's response:", key=unique_key)
            if feedback_input:
                chat_with_bot(combined_input, state, feedback_input, temperature=0.15)
                save_conversation_to_file(state, "D:\AISHA\cpaas-tools\conversation.json")  # Pass context to the chat function
            else:
                chat_with_bot(combined_input, state)  # Pass context to the chat function

        # Show the feedback input bar
        state.show_feedback_bar = True

        # Reset the user input and the file uploader
        st.session_state.user_input_state = " "
        state.file_uploader_key += 1  # Change the key to reset the file uploader

        # Reset the user input and uploaded file by rerunning the Streamlit app
        st.experimental_rerun()

if __name__ == "__main__":
    main()