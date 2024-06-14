import functools
import json
import pickle
import logging

import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler

from src.address_parser import AddressParser
from src.address_parser_signature import AddressParserSignature
from src.address_store_controller import AddressStoreController
from src.custom_lm_client import CustomLMClient
from src.utilities import load_stringified_json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

openai = CustomLMClient(model="openai/gpt-4o")
dspy.configure(lm=openai)
def main():
    """
    main execution script
    """
    address_parser = dspy.ChainOfThought(AddressParserSignature)

    with (
        #open("./resources/parse_constraints.txt", encoding="utf-8") as f_0,
        open("./resources/parse_format_custom_def.txt", encoding="utf-8") as f_1,
        open("./resources/parse_format_custom.json", encoding="utf-8") as f_2,
    ):
        #parsing_constaints = f_0.read()
        json_structure_definition = f_1.read()
        json_structure = json.load(f_2)

    # backtrack_handler is parameterized over a few settings for the backtracking mechanism
    # To change the number of max retry attempts, you can do
    address_parser = assert_transform_module(AddressParser(),functools.partial(backtrack_handler, max_backtracks=1))

    # address_parser = AddressParser()
    # 
    # 2 addresses = {'prompt_tokens': 2215, 'completion_tokens': 159, 'total_tokens': 2374}
    # prompt cost (gpt-4o) per token 0.000005/ completion cost per token 0.000015 USD!!!
    # one address ~ 80 tokens
    # max prompt + completion context 128000 tokens
    # max completion context 4096 tokens
    # leaving 10% headroom for completion tokens ~ 46 addresses per run

    json_addr_list = address_parser(
        raw_address_list=[
            "Flat B, 12/F, Begonia Mansion, Harbour View Gardens (East), Taikoo Shing, 8 Taikoo Wan Road, Taikoo, Eastern District, Hong Kong Island, Hong Kong SAR, China",
            "NO.3, TAK WING STREET, CITY ONE, SHATIN"
        ],
        #parsing_constaints=parsing_constaints,
        json_structure_definition=json_structure_definition,
        json_structure=json_structure,
    )

    with open('addr_list.pkl', 'wb') as file:
        # Dump the list to the file
        pickle.dump(json_addr_list, file)
    
    # with open('addr_list.pkl', 'rb') as file:
    #     # Dump the list to the file
    #     json_addr_list = pickle.load(file)

    parsed_json_addr_list = []
    for addr in json_addr_list:
        parsed_json_addr_list.append(load_stringified_json(addr))

    if len(parsed_json_addr_list) > 0:
        storage_controller = AddressStoreController(parsed_json_addr_list[0]["addresses"]["Eng3dAddress"])
        for p_addr in parsed_json_addr_list:
            storage_controller.insert_address(p_addr["addresses"]["Eng3dAddress"])
    else:
        logger.warning("completions with size 0 was detected exiting...")

if __name__ == "__main__":
    main()
