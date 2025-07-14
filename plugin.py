# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import sys
import os
from ctypes import byref, windll, wintypes
from typing import Optional
import requests
import google.generativeai as genai
from logger import get_logger
logger = get_logger("KnowMyGame")

# Load Configuration
def get_config_path():
    if getattr(sys, 'frozen', False):  # True when running as .exe
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "config.json")

CONFIG_PATH = get_config_path()

def load_plugin_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            if "env" in config:
                for k, v in config["env"].items():
                    os.environ[k] = v
            return config
    except Exception as e:
        logger.warning(f"Failed to load config.json: {str(e)}")
        return {}

config = load_plugin_config()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Data Types
Response = dict[bool, Optional[str]]

# LOG_FILE = os.path.join(os.environ.get("USERPROFILE", "."), 'python_plugin.log')
# logger.basicConfig(filename=LOG_FILE, level=logger.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # print("List of models that support generateContent:")
    # for model in genai.list_models():
    #     # The correct attribute is supported_generation_methods
    #     if "generateContent" in model.supported_generation_methods:
    #         print(f"Name: {model.name}")
    #         print(f"Description: {model.description}")
    #         print("-" * 20)

    TOOL_CALLS_PROPERTY = 'tool_calls'
    CONTEXT_PROPERTY = 'messages'
    SYSTEM_INFO_PROPERTY = 'system_info'
    FUNCTION_PROPERTY = 'func'
    PARAMS_PROPERTY = 'properties'
    INITIALIZE_COMMAND = 'initialize'
    SHUTDOWN_COMMAND = 'shutdown'
    ERROR_MESSAGE = 'Plugin Error!'

    commands = {
        'initialize': execute_initialize_command,
        'shutdown': execute_shutdown_command,
        'get_game_price_rating': execute_game_price_rating,
        'recommend_game_settings': execute_game_settings,
        'find_video_walkthrough': execute_video_walkthrough
    }

    cmd = ''
    logger.info('Plugin started')

    while cmd != SHUTDOWN_COMMAND:
        response = None
        input = read_command()
        if input is None:
            logger.error('Error reading command')
            continue

        logger.info(f'Received input: {input}')

        if TOOL_CALLS_PROPERTY in input:
            tool_calls = input[TOOL_CALLS_PROPERTY]
            for tool_call in tool_calls:
                if FUNCTION_PROPERTY in tool_call:
                    cmd = tool_call[FUNCTION_PROPERTY]
                    logger.info(f'Processing command: {cmd}')
                    if cmd in commands:
                        if cmd == INITIALIZE_COMMAND or cmd == SHUTDOWN_COMMAND:
                            response = commands[cmd]()
                        else:
                            response = execute_initialize_command()
                            response = commands[cmd](
                                tool_call.get(PARAMS_PROPERTY),
                                input.get(CONTEXT_PROPERTY),
                                input.get(SYSTEM_INFO_PROPERTY)
                            )
                    else:
                        logger.warning(f'Unknown command: {cmd}')
                        response = generate_failure_response(f'{ERROR_MESSAGE} Unknown command: {cmd}')
                else:
                    logger.warning('Malformed input: missing function property')
                    response = generate_failure_response(f'{ERROR_MESSAGE} Malformed input.')
        else:
            logger.warning('Malformed input: missing tool_calls property')
            response = generate_failure_response(f'{ERROR_MESSAGE} Malformed input.')

        logger.info(f'Sending response: {response}')
        write_response(response)

        if cmd == SHUTDOWN_COMMAND:
            logger.info('Shutdown command received, terminating plugin')
            break

    logger.info('G-Assist Plugin stopped.')
    return 0

def read_command() -> dict | None:
    try:
        STD_INPUT_HANDLE = -10
        pipe = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        chunks = []

        while True:
            BUFFER_SIZE = 4096
            message_bytes = wintypes.DWORD()
            buffer = bytes(BUFFER_SIZE)
            success = windll.kernel32.ReadFile(
                pipe,
                buffer,
                BUFFER_SIZE,
                byref(message_bytes),
                None
            )

            if not success:
                logger.error('Error reading from command pipe')
                return None

            chunk = buffer.decode('utf-8')[:message_bytes.value]
            chunks.append(chunk)

            if message_bytes.value < BUFFER_SIZE:
                break

        retval = ''.join(chunks)
        return json.loads(retval)

    except json.JSONDecodeError:
        logger.error('Failed to decode JSON input')
        return None
    except Exception as e:
        logger.error(f'Unexpected error in read_command: {str(e)}')
        return None

def write_response(response: Response) -> None:
    try:
        STD_OUTPUT_HANDLE = -11
        pipe = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        json_message = json.dumps(response)
        message_bytes = json_message.encode('utf-8')
        message_len = len(message_bytes)

        bytes_written = wintypes.DWORD()
        windll.kernel32.WriteFile(
            pipe,
            message_bytes,
            message_len,
            bytes_written,
            None
        )
    except Exception as e:
        logger.error(f'Failed to write response: {str(e)}')

def generate_failure_response(message: str = None) -> Response:
    response = {'success': False}
    if message:
        response['message'] = message
    return response

def generate_success_response(message: str = None) -> Response:
    response = {'success': True}
    if message:
        response['message'] = message
    return response

def execute_initialize_command() -> dict:
    logger.info('Initializing plugin')
    return generate_success_response('initialize success.')

def execute_shutdown_command() -> dict:
    logger.info('Shutting down plugin')
    return generate_success_response('shutdown success.')

def execute_game_price_rating(params: dict = None, context: dict = None, system_info: dict = None) -> dict:
    game_name = params.get("game_name")
    if not game_name:
        return generate_failure_response("Missing 'game_name' parameter.")

    try:
        search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us&l=en"
        result = requests.get(search_url).json()
        if not result["items"]:
            return generate_failure_response("Game not found on Steam.")

        app_id = result["items"][0]["id"]
        details_url = f"https://store.steampowered.com/api/appdetails/?appids={app_id}"
        details = requests.get(details_url).json()
        game_data = details[str(app_id)]["data"]

        price_info = game_data.get("price_overview", {})
        price = price_info.get("final_formatted", "Free" if game_data.get("is_free") else "N/A")
        rating = game_data.get("metacritic", {}).get("score", "No rating")

        return generate_success_response(f"Game: {game_name}\\nPrice: {price}\\nRating: {rating}")
    except Exception as e:
        return generate_failure_response(str(e))

def execute_game_settings(params: dict = None, context: dict = None, system_info: dict = None) -> dict:
    game_name = params.get("game_name")
    if not game_name or not system_info:
        return generate_failure_response("Missing 'game_name' or 'system_info'.")

    try:
        prompt = (
            f"Given the following system specs:\\n"
            f"CPU: {system_info.get('cpu')}\\n"
            f"GPU: {system_info.get('gpu')}\\n"
            f"RAM: {system_info.get('ram')}\\n"
            f"Recommend optimal graphics settings for the game '{game_name}' "
            f"that balance visual quality and performance."
        )

        model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")
        response = model.generate_content(prompt)

        return generate_success_response(response.text.strip())
    except Exception as e:
        return generate_failure_response(str(e))

def execute_video_walkthrough(params: dict = None, context: dict = None, system_info: dict = None) -> dict:
    game_name = params.get("game_name")
    question = params.get("question")

    if not game_name or not question:
        return generate_failure_response("Missing 'game_name' or 'question'.")

    try:
        search_query = f"{game_name} walkthrough {question}"
        prompt = f"Find the best YouTube video for this game query: '{search_query}'. Include a timestamp and video link."

        model = genai.GenerativeModel("models/gemini-2.0-flash-thinking-exp-1219")
        ai_response = model.generate_content(prompt)

        return generate_success_response(ai_response.text.strip())
    except Exception as e:
        return generate_failure_response(str(e))

if __name__ == '__main__':
    main()