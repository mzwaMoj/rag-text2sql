# utils/mlflow_logger.py
import mlflow
import json

def start_chat_run(user_input):
    mlflow.set_experiment("Chatbot_Tracing")
    mlflow.start_run(nested=True)
    mlflow.log_param("user_input", user_input)

def log_router_response(message):
    mlflow.log_text(str(message), "router_response.json")

def log_sql_code(sql_code):
    mlflow.log_text(sql_code, "generated_sql.sql")

def log_sql_results(results):
    mlflow.log_text(json.dumps(results, indent=2), "sql_results.json")

def log_product_info(info):
    mlflow.log_text(json.dumps(info, indent=2), "product_info.json")

def log_validation_result(result, filename="validation_result.txt"):
    mlflow.log_text(str(result), filename)

def log_final_response(response):
    mlflow.log_text(response, "final_response.txt")

def end_chat_run():
    mlflow.end_run()
