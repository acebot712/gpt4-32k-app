# GPT-4 32K App
This project provides a basic implementation of a text to text application using Azure OpenAI's GPT-4 32K model. The application can generate textual responses to user inputs using a REST API. This application also includes an interface for serving the model over a web interface with Streamlit.

In addition, the application remotely calls DuckDuckGo Instant Answer API to do a quick search and provide a summary of the search query. This allows user to make external API calls directly from the OpenAI chat model.

## Features
- Text to Text Generation: Integrates with Azure OpenAI and get responses based on the user prompt.
- Python File Reader: A feature to read python files from a local directory and incorporate the file content into the conversation history.
- Interactive UI: Streamlit web app offering a clean and simplistic UI making it user friendly.
- Internet Access: It combines web search with Duck Duck Go to provide more nuanced responses to the user.

## Installation
1. Clone the repository:
```sh
git clone https://github.com/acebot712/gpt-4-32k-app.git
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