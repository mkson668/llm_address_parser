import dspy
from .utilities import stringify_json


class AddressParserSignature(dspy.Signature):
    """
    Parse the provided list of addresses and format them as a seperate key-value pairs. No additional text is allowed.

    Please note that the majority of the addresses you will be analysing will be from Hong Kong, but the system should also be able to handle addresses from other countries. When analysing Hong Kong addresses, pay special attention to the following common features and conventions:

    1. District and area names, such as "Kowloon," "Wan Chai," or "Tsim Sha Tsui."
    2. Estate and phase names, such as "Taikoo Shing" or "Mei Foo Sun Chuen." Estate names often appear before building names and numbers, and they typically represent larger residential or commercial developments. 
    3. Building names and numbers, such as "Harbour Centre" or "Tower 2." Building names and numbers refer to specific structures within an estate.
    4. Floor and unit numbers, which may be presented in a combined format, such as "12/F" for "12th Floor" or "5A" for "Unit 5A." Carefully analyse the address to correctly separate the floor and unit information.

    When analysing addresses, be sure to:

    - Correctly identify and separate unit and floor information, even if they are presented in a combined format (e.g., "9F" should be analysed as floor "9" and unit "F").
    - Pay attention to the order and formatting of the address components to accurately determine their roles (e.g., in "9G, Tower 1," "9" is the floor and "G" is the unit).
    - Distinguish between estate and building names. If an address includes both an estate name and a building name or number, make sure to assign them to the correct fields in the analysed output.

    For addresses outside of Hong Kong, the analyser should still attempt to identify and structure the key components, such as street name, building name or number, and postcode, even if they do not follow Hong Kong-specific conventions.

    When analysing ambiguous or incomplete addresses, take a conservative approach. Do not make excessive assumptions or inferences about missing or unclear information. Focus on extracting and structuring the address components that are explicitly provided, and use the 'issues,' 'confidence,' and 'remarks' fields to clearly indicate any uncertainties, missing information, or potential errors in the analysed output. If an address component is missing or cannot be confidently determined, leave the corresponding field empty or mark it as 'unknown.' 
    """

    raw_address_list = dspy.InputField(desc="A list of addresses that should be parsed into key-value pairs", format=list)
    #parsing_constaints = dspy.InputField(desc="these are the constraints when parsing the address")
    json_structure_definition = dspy.InputField(desc="The definitions of the key-value pairs")
    json_structure = dspy.InputField(desc="The output key-value pairs format structure", format=stringify_json)
    json_addresses = dspy.OutputField(desc="A list of key-value pairs objects, no leading or trailing strings are permitted", format=list)
