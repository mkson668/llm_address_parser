import dspy

from .utilities import stringify_json


class AddressParserSignature(dspy.Signature):
    """
    You are an intelligent address parsing system. Your task is to take a given input string containing a 
    physical address and accurately extract the individual components.
    """

    raw_address_list = dspy.InputField(
        desc="A list of addresses that should be parsed into JSON objects", format=list
    )
    parsing_constraints = dspy.InputField(desc="these are the constraints when parsing the addresses")
    json_structure_definition = dspy.InputField(desc="The definitions of the JSON keys")
    json_structure = dspy.InputField(
        desc="The output JSON object format structure", format=stringify_json
    )
    json_addresses = dspy.OutputField(
        desc="A list of JSON objects, no leading or trailing strings are permitted",
        format=list,
    )
