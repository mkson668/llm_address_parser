import dspy
import pickle
import json

from src.address_parser_signature import AddressParserSignature
from src.address_store_controller import AddressStoreController
from src.custom_lm_client import CustomLMClient
from src.utilities import parse_api_return_json_string

openai = CustomLMClient(model="openai/gpt-4o")
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

dspy.configure(lm=openai, rm=colbertv2_wiki17_abstracts)
def main():
    """
    main execution script
    """
    address_parser = dspy.ChainOfThought(AddressParserSignature)

    with (
        #open("./resources/parse_constraints.txt", encoding="utf-8") as f_0,
        open("./resources/parse_format_def.txt", encoding="utf-8") as f_1,
        open("./resources/parse_format.json", encoding="utf-8") as f_2,
    ):
        #parsing_constaints = f_0.read()
        json_structure_definition = f_1.read()
        json_structure = json.load(f_2)

    response_0 = address_parser(
        raw_address_list=[
            "Room2301-3 23 / F Wayson Comm Bldg No. 28 Connaught Rd W H K, Western District, Hong Kong",
            "Flat B, 12/F, Begonia Mansion, Harbour View Gardens (East), Taikoo Shing, 8 Taikoo Wan Road, Taikoo, Eastern District, Hong Kong Island, Hong Kong SAR, China"
        ],
        #parsing_constaints=parsing_constaints,
        json_structure_definition=json_structure_definition,
        json_structure=json_structure,
    )

    json_addr_list = response_0.json_addresses
    with open('addr_list.pkl', 'wb') as file:
        # Dump the list to the file
        pickle.dump(json_addr_list, file)

    parsed_json_addr_list = []
    for addr in parse_api_return_json_string(json_addr_list):
        parsed_json_addr_list.append(addr)

    if len(parsed_json_addr_list) > 0:
        storage_controller = AddressStoreController(parsed_json_addr_list[0])
        for p_addr in parsed_json_addr_list:
            storage_controller.insert_address(p_addr)

if __name__ == "__main__":
    main()
