import json
import logging
import re
import sys

logger = logging.getLogger(__name__)


def stringify_json(data):
    """
    simple wrapper for json stringify
    """
    s_data = json.dumps(data)
    return s_data


def clean_json_string(json_string):
    """quick json removal"""
    pattern = r"^```json\s*(.*?)\s*```$"
    cleaned_string = ""
    try:
        cleaned_string = re.sub(pattern, r"\1", json_string, flags=re.DOTALL)
    except json.JSONDecodeError as e:
        logger.warning("parsing error detected: %s", str(e))
        cleaned_string = json_string
    return cleaned_string.strip()


def parse_api_return_json_string(json_string):
    """
    parse dirty json string returned after calling LLM api
    """

    modified_str = clean_json_string(json_string)
    # Parse the cleaned string into a Python dictionary
    try:
        data = json.loads(modified_str)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e} with format {modified_str}")
        sys.exit(1)
