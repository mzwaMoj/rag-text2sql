"""
Consolidated agents module that combines functionality from separate agent scripts.
This module provides three agent functions:
- routing_agent: Routes user requests to appropriate functions/tools
- agent_sql_queries: Processes SQL query-related requests
- agent_product_offerings: Processes product offering-related requests
"""

from pathlib import Path
import sys
import os
import json
import warnings

# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

# Update import statement to use the new OpenAI API format
from openai import AzureOpenAI

# Import prompts
from prompts.prompt_agent_router import prompt_agent_router
from prompts.prompt_agent_sql_analysis import prompt_agent_sql_analysis

from tools.tools import tools_definitions

# Suppress warnings
warnings.filterwarnings("ignore")

# Try to load environment variables, but don't crash if module is missing
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    print("Warning: python-dotenv not found. Please set OPENAI_API_KEY manually.")
# Get the Keys
API_KEY = os.environ.get("AZURE_OPENAI_KEY") 
API_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
API_VERSION = os.environ.get("AZURE_OPENAI_VERSION")
MODEL = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

# Create client
client = AzureOpenAI(
  # default_headers={"Ocp-Apim-Subscription-Key": API_KEY},
  api_key=API_KEY,
  azure_endpoint=API_ENDPOINT,
  azure_deployment= AZURE_DEPLOYMENT,
  api_version=API_VERSION, 
)


MODEL_REASONING = "o3-mini" # Model for reasoning tasks

def routing_agent(user_request, chat_history):
    """Routes the user request to the appropriate function/tool, using chat history for context."""
    prompt = prompt_agent_router()

    messages = [{"role": "system", "content": prompt}]
    messages.extend(chat_history)

    # Ensure latest user message is not duplicated
    if not chat_history or chat_history[-1]["role"] != "user" or chat_history[-1]["content"] != user_request:
        messages.append({"role": "user", "content": user_request})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools_definitions(),
        tool_choice="auto"
    )
    return response


def agent_sql_analysis(user_input):
    """
    Processes SQL query-related requests.
    
    Args:
        user_input: String or JSON-serializable input from the user
        
    Returns:
        str: The generated response text
    """
    # Accepts any data type: string, dict, list, etc.
    # If not string, convert to JSON string for the LLM
    if not isinstance(user_input, str):
        user_input_serialized = json.dumps(user_input)
    else:
        user_input_serialized = user_input

    completions = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_agent_sql_analysis()},
            {"role": "user", "content": user_input_serialized}
        ],
    )
    return completions.choices[0].message.content



def agent_others(user_input):
    """
    Processes SQL query-related requests.
    
    Args:
        user_input: String or JSON-serializable input from the user
        
    Returns:
        str: The generated response text
    """
    # Accepts any data type: string, dict, list, etc.
    # If not string, convert to JSON string for the LLM
    if not isinstance(user_input, str):
        user_input_serialized = json.dumps(user_input)
    else:
        user_input_serialized = user_input

    completions = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt_agent_sql_analysis()},
            {"role": "user", "content": user_input_serialized}
        ],
    )
    return completions.choices[0].message.content