# GPT-4 32K App
This repository contains the codebase for a streamline web app that communicates with Azure OpenAI to get responses based on a provided prompt. It's a simple and interactive way to harness the power of GPT-4 in your applications. The app also has a feature to read the contents of python files from a local path and feed it into the conversation history.

## Features
- Text to Text Generation: Integrates with Azure OpenAI and get responses based on the user prompt.
- Python File Reader: A feature to read python files from a local directory and incorporate the file content into the conversation history.
- Interactive UI: Streamlit web app offering a clean and simplistic UI making it user friendly.

## Installation
1. Clone the repository:
```sh
git clone https://github.com/<username>/gpt-4-32k-app.git
```

2. Change into the directory:
```sh
cd gpt-4-32k-app
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Create a .env file at the root and add your azure credentials:
```sh
API_VERSION=<your_api_version>
AZURE_ENDPOINT=<your_azure_endpoint>
OPENAI_API_KEY=<your_openai_api_key>
MODEL=<your_model>
```

5. Finally, start the server:
```sh
streamlit run app.py
```

## Usage
Simply enter your prompt and (optionally) a local path to python files and then click on the "Generate Response" button.

The response from Azure OpenAI will be generated and displayed on the screen. The python files content (if any) will also be appended into the conversation history.

## Contributing
Contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

## Support
If you have any questions or run into any bugs, please file an issue on this repository.