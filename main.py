import openai
import os
from dotenv import find_dotenv, load_dotenv
import json
import re
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from contextlib import nullcontext
import openai
from config import load_question_config  # Updated import

load_dotenv(override=True)
client = openai.OpenAI()

function_map = {
    "text_input": st.text_input,
    "text_area": st.text_area,
    "warning": st.warning,
    "button": st.button,
    "radio": st.radio,
    "markdown": st.markdown,
    "selectbox": st.selectbox
}

user_input = {}

# Load question configuration from command line or Streamlit sidebar
def get_question_id():
    """Get question ID from URL params or sidebar"""
    query_params = st.experimental_get_query_params()
    if 'question' in query_params:
        return int(query_params['question'][0])
    else:
        return st.sidebar.selectbox("Select Question", options=[1, 2, 3, 4, 5, 6], index=0)

class AssistantManager:
    def __init__(self, question_config):
        self.client = openai
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None
        self.config = question_config
        
        # Use assistant ID from config (loaded from environment)
        self.assistant_id = question_config['assistant_id']
        self.llm_configuration = question_config['llm_config']["gpt-4o"]  # Default to gpt-4o
        
        self.load_assistant()

    def load_assistant(self):
        """Load existing assistant or create new one"""
        if self.assistant_id:
            try:
                self.assistant = self.client.beta.assistants.retrieve(
                    assistant_id=self.assistant_id
                )
            except Exception as e:
                st.error(f"Error retrieving assistant: {e}")
        else:
            self.create_assistant()

    def create_assistant(self):
        """Create new assistant if needed"""
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=self.config["assistant_name"],
                instructions=self.config["assistant_instructions"],
                tools=[{"type": "file_search"}],
                model=self.llm_configuration["model"]
            )
            self.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            st.session_state["assistant_id"] = assistant_obj.id
            st.warning(f"Created new assistant: {assistant_obj.id}")

    # ... rest of AssistantManager methods remain the same ...
    # (create_thread, add_message_to_thread, run_assistant, calculate_cost)

def build_phases_dict(question_config):
    """Convert YAML config to the PHASES format expected by existing code"""
    phases_dict = {}
    
    for attempt_num in [1, 2, 3]:
        attempt_key = f"attempt{attempt_num}"
        phase_config = question_config['phases'][attempt_key]
        
        # Build the instruction text
        attempt_info = question_config['base_config']['attempt_structure'][attempt_key]
        instructions = f"""The student was asked to {question_config['question_text'].lower()}.
        
        The correct answer is:
        {question_config['correct_answer']}
        
        Compare the following student submission with the correct answer above. 
        Provide feedback on the student submission if their solution is not correct. 
        Do not provide the correct answer. Instead, provide guidance to help the 
        student identify where they might be missing something in their code. 
        
        This is the student's {attempt_info['follow_up_text']}"""
        
        # Build label
        if attempt_num == 1:
            label = question_config['question_text']
        else:
            label = attempt_info['label_suffix']
        
        phases_dict[attempt_key] = {
            "type": phase_config['type'],
            "height": phase_config['height'],
            "label": label,
            "instructions": instructions,
            "value": " ",
            "scored_phase": phase_config['scored_phase'],
            "rubric": "None",
            "minimum_score": phase_config['minimum_score']
        }
    
    return phases_dict

def main():
    # Get question configuration
    question_id = get_question_id()
    
    try:
        question_config = load_question_config(question_id)
    except Exception as e:
        st.error(f"Error loading question {question_id}: {e}")
        return
    
    # Set up app title and intro from config
    if question_config.get('title'):
        st.title(question_config['title'])
    if question_config.get('intro'):
        st.markdown(question_config['intro'])
    
    # Build PHASES dict from config
    PHASES = build_phases_dict(question_config)
    
    # Get completion message from config
    COMPLETION_MESSAGE = question_config.get('completion_message', "Thank you!")
    COMPLETION_CELEBRATION = question_config.get('completion_celebration', False)
    
    # Create the assistant with question-specific config
    openai_assistant = AssistantManager(question_config)
    
    # ... rest of the main() function remains exactly the same ...
    # (all the phase processing, submit button logic, etc.)

if __name__ == "__main__":
    main()
