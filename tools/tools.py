# Tool definitions for Azure OpenAI API with proper schema

# SQL Analysis Tool
tool_sql_analysis = {
    "type": "function",
    "function": {
        "name": "agent_sql_analysis",
        "description": (
            "Generates executable Microsoft SQL Server (MSSQL) queries based on user requests for database operations. "
            "The 'user_request' parameter can be any data type (string, list, dictionary, tuple, JSON object, etc.), "
            "including natural language, structured instructions, or outputs from other agents. "
            "The function should interpret the intent and generate an appropriate SQL query."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_request": {
                    "type": "string", 
                    "description": (
                        "The user's request, which can be any data type (string, list, dictionary, tuple, JSON object, etc.), "
                        "including natural language, structured input, or the output from the router agent about what database operation to perform."
                    )
                },
                "identifier": {
                    "type": "string",
                    "description": "Optional: The customer ID or account number if specified in the request"
                }
            },
            "required": ["user_request"]
        }
    }
}

# Product Offerings Tool
tool_product_offerings = {
    "type": "function",
    "function": {
        "name": "agent_others",
        "description": (
            "Retrieves product offerings based on user input. "
            "The 'user_request' parameter can be any data type (string, list, dictionary, tuple, JSON object, etc.), "
            "including natural language, structured instructions, or outputs from other agents. "
            "The function should interpret the intent and generate an appropriate or relevant product offering."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_request": {
                    "type": "string", 
                    "description": (
                        "The user's request, which can be any data type (string, list, dictionary, tuple, JSON object, etc.), "
                        "including natural language, structured input, or the output from the router agent about what database operation to perform."
                    )
                },
                "identifier": {
                    "type": "string",
                    "description": "Optional: The customer ID or account number if specified in the request"
                }
            },
            "required": ["user_request"]
        }
    }
}

# File Validation Tool
tool_file_validation = {
    "type": "function",
    "function": {
        "name": "agent_file_validation",
        "description": (
            "Processes loan application documents by extracting their contents and validating them against requirements. "
            "This tool handles PDF documents, extracts all relevant information, and validates if the application meets "
            "all banking requirements for loan processing."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string", 
                    "description": "Path to the document file (PDF) that needs to be processed and validated"
                },
                "validation_type": {
                    "type": "string",
                    "enum": ["standard", "strict"],
                    "description": "Optional: The validation strictness level. 'standard' for basic validation, 'strict' for comprehensive validation",
                    "default": "standard"
                }
            },
            "required": ["file_path"]
        }
    }
}

# File Comparison Tool
tool_compare_files = {
    "type": "function",
    "function": {
        "name": "agent_compare_files",
        "description": (
            "Compares two documents by analyzing the data in both and validating if the information matches. "
            "This tool takes two file paths or JSON objects, with one serving as the verification baseline. "
            "It identifies discrepancies in values regardless of key naming differences across documents."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "baseline_data": {
                    "type": "string",
                    "description": "The baseline document that serves as the source of truth. Can be a file path or a JSON object."
                },
                "comparison_data": {
                    "type": "string",
                    "description": "The document to validate against the baseline. Can be a file path or a JSON object."
                },
                "comparison_type": {
                    "type": "string",
                    "enum": ["standard", "strict", "semantic"],
                    "description": "Optional: The comparison strictness level. 'standard' for basic matching, 'strict' for exact matching, 'semantic' for meaning-based matching.",
                    "default": "standard"
                }
            },
            "required": ["baseline_data", "comparison_data"]
        }
    }
}

tools = [ tool_sql_analysis]

def tools_definitions():
    """
    Defines the available tools (functions) for the language model
    in the latest OpenAI API format.

    Returns:
        list: A list of tool definitions, each structured for the API.
    """
    return tools
