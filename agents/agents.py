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
from prompts.prompt_agent_router import prompt_agent_router
from prompts.prompt_agent_sql_analysis import prompt_agent_sql_analysis
from prompts.prompt_agent_final_response import prompt_agent_final_response
from tools.tools import tools_definitions
warnings.filterwarnings("ignore")
import ssl
import urllib3
import httpx

# Disable SSL certificate verification globally (for development only!)
ssl._create_default_https_context = ssl._create_unverified_context
# For requests and urllib3, suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
MODEL_REASONING = "o3-mini" # Model for reasoning tasks

# On windows
# Create httpx client with SSL verification disabled
http_client = httpx.Client(verify=False)

# Create client with custom http_client
client = AzureOpenAI(
    api_key=API_KEY,
    azure_endpoint=API_ENDPOINT,
    api_version=API_VERSION,
    http_client=http_client
)

# Create client
# client = AzureOpenAI(
#   default_headers={"Ocp-Apim-Subscription-Key": API_KEY},
#   api_key=API_KEY,
#   azure_endpoint=API_ENDPOINT,
#   azure_deployment= AZURE_DEPLOYMENT,
#   api_version=API_VERSION, 
# )

# def create_chat_completion(model, messages, tools=None, tool_choice=None):
#     """
#     Generic function to create chat completions with consistent parameters.
    
#     Args:
#         model: The model to use for completion
#         messages: List of message objects for the conversation
#         tools: Optional tools definitions to provide
#         tool_choice: Optional tool selection strategy
        
#     Returns:
#         The raw response from OpenAI API
#     """
#     kwargs = {
#         "model": model,
#         "messages": messages
#     }
    
#     # Only add tools and tool_choice if they are provided
#     if tools:
#         kwargs["tools"] = tools
#     if tool_choice:
#         kwargs["tool_choice"] = tool_choice
        
#     return client.chat.completions.create(**kwargs)


# def prepare_messages(system_prompt, user_input, chat_history=None):
#     """
#     Prepare messages for an OpenAI API call with proper handling of chat history.
    
#     Args:
#         system_prompt: The system prompt to use
#         user_input: The user's input message
#         chat_history: Optional chat history list
        
#     Returns:
#         List of message objects ready for API call
#     """
#     messages = [{"role": "system", "content": system_prompt}]
    
#     # Add chat history if provided
#     if chat_history:
#         messages.extend(chat_history)
        
#         # Ensure latest user message is not duplicated
#         if chat_history[-1]["role"] != "user" or chat_history[-1]["content"] != user_input:
#             messages.append({"role": "user", "content": user_input})
#     else:
#         # No chat history, simply add the user message
#         messages.append({"role": "user", "content": user_input})
            
#     return messages


# def routing_agent(user_request, chat_history):
#     """Routes the user request to the appropriate function/tool, using chat history for context."""
#     messages = prepare_messages(
#         system_prompt=prompt_agent_router(),
#         user_input=user_request,
#         chat_history=chat_history
#     )
    
#     # Return the complete response object as the original function did
#     return create_chat_completion(
#         model=MODEL,
#         messages=messages,
#         tools=tools_definitions(),
#         tool_choice="auto"
#     )


    
# def agent_sql_analysis(user_input):
#     """
#     Processes SQL query-related requests.
    
#     Args:
#         user_input: String or JSON-serializable input from the user
        
#     Returns:
#         str: The generated response text
#     """
#     # Convert non-string input to JSON string
#     if not isinstance(user_input, str):
#         user_input = json.dumps(user_input)
    
#     messages = prepare_messages(
#         system_prompt=prompt_agent_sql_analysis(),
#         user_input=user_input
#     )
    
#     # Return only the message content as the original function did
#     response = create_chat_completion(model=MODEL, messages=messages)
#     return response.choices[0].message.content


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

def agent_final_response(user_request, chat_history):
    """Routes the user request to the appropriate function/tool, using chat history for context."""
    prompt = prompt_agent_final_response()

    messages = [{"role": "system", "content": prompt}]
    messages.extend(chat_history)

    # Ensure latest user message is not duplicated
    if not chat_history or chat_history[-1]["role"] != "user" or chat_history[-1]["content"] != user_request:
        messages.append({"role": "user", "content": user_request})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
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



# def agent_others(user_input):
#     """
#     Processes SQL query-related requests.
    
#     Args:
#         user_input: String or JSON-serializable input from the user
        
#     Returns:
#         str: The generated response text
#     """
#     # Accepts any data type: string, dict, list, etc.
#     # If not string, convert to JSON string for the LLM
#     if not isinstance(user_input, str):
#         user_input_serialized = json.dumps(user_input)
#     else:
#         user_input_serialized = user_input

#     completions = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": prompt_agent_sql_analysis()},
#             {"role": "user", "content": user_input_serialized}
#         ],
#     )
#     return completions.choices[0].message.content