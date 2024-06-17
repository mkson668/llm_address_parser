import json
import logging
import re
import sys
import os

import pandas as pd

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
        logger.error("Failed to parse JSON: %s with format %s", e, modified_str)
        sys.exit(1)


def load_stringified_json(json_string):
    """
    jsonify string based json and catch exceptions for formatting
    """

    try:
        ret_json = json.loads(json_string)
        return ret_json
    except json.JSONDecodeError as e:
        logger.error(f"json load failed: {e} with format {json_string}")
        sys.exit(1)


def read_data(file_path):
    """
    read file
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".csv":
        data = pd.read_csv(file_path)
    elif ext == ".pkl":
        data = pd.read_pickle(file_path)
    elif ext == ".xlsx" or ext == ".xls":
        data = pd.read_excel(file_path)
    elif ext == ".feather":
        data = pd.read_feather(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return data
