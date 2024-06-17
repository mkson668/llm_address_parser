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
    git clone https://github.com/yourusername/address-parser.git
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
- The input file should be named `address_full.xlsx` and placed in the `root/input` folder.
- The file should contain the addresses to be parsed.

### Output File
- The output file will be named `address.feather` and saved in the `root/output` folder.
- The file will contain the parsed addresses.

### API Key
- Users need to provide their own OpenRouter API key in a `secrets.json` file at the root of the project.

## Examples
Here is an example of how to set up the `secrets.json` file:
```json
{
  "OPENROUTER_API_KEY": "your_openrouter_api_key"
}
```

## Troubleshooting

## Contributors

## License
This project is licensed under the MIT License.