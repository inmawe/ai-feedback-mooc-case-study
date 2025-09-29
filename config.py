import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()

# Base configuration shared across all questions
BASE_CONFIG = {
    "completion_celebration": False,
    "scoring_debug_mode": False,
    "attempt_structure": {
        "attempt1": {"label_suffix": "", "follow_up_text": "first submission. They can follow up two more times."},
        "attempt2": {"label_suffix": "Do you want to try again?", "follow_up_text": "second submission. They can follow up one more time."},
        "attempt3": {"label_suffix": "Do you want to try one more time?", "follow_up_text": "last submission. They can't ask again."}
    }
}

# LLM Configuration (shared)
ASSISTANT_BASE_INSTRUCTIONS = "You are an expert in SQL and the instructor of a course where students are learning the basics of SQL."

LLM_CONFIGURATION = {
    "gpt-4-turbo": {
        "tools": [{"type": "file_search"}],
        "model": "gpt-4-turbo",
        "temperature": 0,
        "price_per_1k_prompt_tokens": .01,
        "price_per_1k_completion_tokens": .03
    },
    "gpt-4o": {
        "tools": [{"type": "file_search"}],
        "model": "gpt-4o",
        "temperature": 0,
        "price_per_1k_prompt_tokens": .0025,
        "price_per_1k_completion_tokens": .010
    },
    "gpt-3.5-turbo": {
        "tools": [{"type": "file_search"}],
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0,
        "price_per_1k_prompt_tokens": 0.0005,
        "price_per_1k_completion_tokens": 0.0015
    }
}

def load_question_config(question_id):
    """Load configuration for a specific question."""
    config_path = Path(f"questions/question_{question_id}/config.yaml")
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        question_config = yaml.safe_load(f)
    
    # Get assistant ID from environment
    assistant_id = os.getenv(f"ASSISTANT_ID_Q{question_id}")
    if not assistant_id:
        raise ValueError(f"ASSISTANT_ID_Q{question_id} not found in environment variables")
    
    question_config['assistant_id'] = assistant_id
    question_config['base_config'] = BASE_CONFIG
    question_config['llm_config'] = LLM_CONFIGURATION
    
    return question_config
