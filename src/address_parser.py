from typing import List

import dspy

from src.address_parser_signature import AddressParserSignature


class AddressParser(dspy.Module):
    """
    putting things together to form the module
    """
    def __init__(self):
        self.generate_answer = dspy.ChainOfThought(AddressParserSignature)

    def forward(self, raw_address_list: List[str], json_structure_definition: str, json_structure: str):
        """
        forward call for inherited function
        """
        pred = self.generate_answer(
            raw_address_list=raw_address_list,
            json_structure_definition=json_structure_definition,
            json_structure=json_structure
            )
        print(type(pred.json_addresses))
        dspy.Suggest(
            result=isinstance(pred.json_addresses, str), 
            msg="the parsed answer should be a JSON string"
            )
        return pred
