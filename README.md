# Address Parser with GPT-4

## Introduction
This project leverages GPT-4 and DSPy to parse batches of addresses. The input is provided via an Excel document, and the output is stored in a Feather formatted file. The project utilizes the OpenAI API to process the addresses in batches. Users need to create a `secrets.json` file for the API key configuration.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/mkson668/address-parser.git
    cd address-parser
    ```
2. Ensure you have Python 3.10.6 installed.
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Place your input Excel file (`address_full.xlsx`) in the `root/input` folder.
2. Create a `secrets.json` file at the root of the project with your OpenRouter API key:
    ```json
    {
      "OPENROUTER_API_KEY": "your_openrouter_api_key"
    }
    ```
3. Run the main execution script:
    ```sh
    python main.py
    ```
4. The parsed addresses will be saved in the `root/output` folder as `address.feather`.

## Features
- Parses addresses using GPT-4 and DSPy.
- Batch processing of addresses for efficiency.
- Input and output through easily manageable files.

## Dependencies
- Python 3.10.6
- DSPy
- OpenAI API
- Pandas
- Feather-format

## Configuration
The only configuration option available to users is the `MAX_BATCH_SIZE` global variable, which sets the size of each address batch used for parsing. Note that `MAX_BATCH_SIZE` is limited to 45 due to completion token limitations.

## Documentation
### Input File
- The raw address input file should be named `address_full.xlsx` and placed in the `./input` folder.
- The file should contain the addresses to be parsed under the `raw_address` column.

### Output File
- The output file will be named `address.feather` and saved in the `./output` folder.
- The file will contain the parsed addresses dataframe with the following columns:
    - FloorNum: The floor number of the building.
    - FloorDescription: A description or additional details about the floor.
    - UnitDescriptor: The type or descriptor for the unit (e.g., Flat, Apartment, Suite).
    - UnitNo: The unit or apartment number.
    - UnitPortion: Any additional portion or subdivision of the unit.
    - BlockDescriptor: A descriptor or label for the block within the building or complex.
    - BlockNo: The block number within the building or complex.
    - BuildingName: The name of the building or structure.
    - EstateName: The name of the estate or residential complex.
    - PhaseName: The name of the phase or section within the estate or complex.
    - PhaseNo: The phase or section number within the estate or complex.
    - LocationName (under EngVillage): The location name associated with the village.
    - VillageName: The name of the village or residential area.
    - BuildingNoFrom (under EngVillage): The starting building number range for the village.
    - BuildingNoTo (under EngVillage): The ending building number range for the village.
    - LocationName (under EngStreet): The location name associated with the street.
    - StreetName: The name of the street.
    - BuildingNoFrom (under EngStreet): The starting building number range for the street.
    - BuildingNoTo (under EngStreet): The ending building number range for the street.
    - DcDistrict: The name of the district or administrative division.
    - Region: The region code or identifier.
    - county: The county or administrative division.
    - city: The name of the city.
    - state: The name of the state or administrative division.
    - province: The name of the province or administrative division.
    - postalCode: The postal or zip code.
    - country: The name of the country.
    - countryCode: The code or identifier for the country.
    - poBox: A post office box number.
    - attentionLine: An attention line or additional recipient information.
    - careOfLine: A care of line or additional recipient information.
    - confidenceScore: A confidence score or rating associated with the address data.
    - issues: Any issues or problems identified with the address data.

### API Key
- Users need to provide their own OpenRouter API key in a `secrets.json` file at the root of the project.

## Examples
Here is an example output for the address `Flat B, 12/F, Begonia Mansion,Harbour View Gardens (East), Taikoo Shing,8 Taikoo Wan Road, Taikoo, Eastern District,Hong Kong Island, Hong Kong SAR, China`:

```json
{
  "EngFloor": {
    "FloorNum": "12",
    "FloorDescription": ""
  },
  "EngUnit": {
    "UnitDescriptor": "Flat",
    "UnitNo": "B",
    "UnitPortion": ""
  },
  "EngBlock": {
    "BlockDescriptor": "",
    "BlockNo": ""
  },
  "BuildingName": "Begonia Mansion",
  "EngEstate": {
    "EstateName": "Harbour View Gardens (East)"
  },
  "EngPhase": {
    "PhaseName": "",
    "PhaseNo": ""
  },
  "EngVillage": {
    "LocationName": "",
    "VillageName": "Taikoo Shing",
    "BuildingNoFrom": "",
    "BuildingNoTo": ""
  },
  "EngStreet": {
    "LocationName": "Taikoo",
    "StreetName": "Taikoo Wan Road",
    "BuildingNoFrom": "8",
    "BuildingNoTo": ""
  },
  "EngDistrict": {
    "DcDistrict": "Eastern District",
    "Region": "HK"
  },
  "county": "",
  "city": "Hong Kong Island",
  "state": "",
  "province": "",
  "postalCode": "",
  "country": "Hong Kong SAR, China",
  "countryCode": "",
  "poBox": "",
  "attentionLine": "",
  "careOfLine": "",
  "confidenceScore": "0.9",
  "issues": ""
}
```

## Troubleshooting

## Contributors

## License
This project is licensed under the MIT License.