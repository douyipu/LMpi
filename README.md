# LMpi - Language Model Prompt Injector

LMpi (Language Model Prompt Injector) is a tool designed to test and analyze various language models, including both API-based models and local models like those from Hugging Face.

## Current Features

- Secure configuration management with encryption
- Session-based authentication for API key protection
- Support for multiple language model providers (OpenAI, Anthropic, Cohere, Hugging Face)
- Command-line interface for easy interaction
- Modular design for easy extension to new model types

## Project Structure

- `lmpi.py`: Main script and command-line interface
- `config_handler.py`: Handles secure storage and retrieval of configuration and API keys
- `model_registry.py`: Maintains a registry of supported models and their providers
- `testers/`: Directory containing model testing implementations
  - `base_tester.py`: Abstract base class for model testers
  - `api_tester.py`: Tester for API-based models
  - `huggingface_tester.py`: Tester for Hugging Face models

## Usage

To use LMpi, follow these steps:

1. Set up a password for secure storage:
   ```
   python lmpi.py --set-password
   ```

2. Save an API key for a supported company:
   ```
   python lmpi.py --save-api-key <COMPANY> <API_KEY>
   ```
   Replace `<COMPANY>` with the company name (e.g., openai, anthropic) and `<API_KEY>` with your actual API key.

3. List available models:
   ```
   python lmpi.py --list-models
   ```

4. Test a model with a prompt:
   ```
   python lmpi.py -m <MODEL_NAME> -p "Your prompt here"
   ```
   Replace `<MODEL_NAME>` with a supported model name (e.g., gpt-3.5-turbo, claude-2).

5. List companies with saved API keys:
   ```
   python lmpi.py --list-companies
   ```

6. Show a specific API key:
   ```
   python lmpi.py --show-api-key <COMPANY>
   ```

7. Remove an API key:
   ```
   python lmpi.py --remove-api-key <COMPANY>
   ```

8. End your session:
   ```
   python lmpi.py --logout
   ```

Note: For security reasons, you'll need to enter your password when performing operations that involve API keys or sensitive information. The session will remain active for 15 minutes by default.

For more detailed information on each command, use the help option:
```
python lmpi.py -h
```

(Note: As the project develops, more features and usage examples will be added to this section.)

## Upcoming Work

1. Implement actual API calls for supported providers (OpenAI, Anthropic)
2. Develop a robust prompt injection testing methodology
3. Create a reporting system for test results
4. Implement batch testing capabilities
5. Add support for more model providers and types
6. Develop a user-friendly way to add custom models to the registry
7. Create comprehensive documentation and usage examples

## Installation

(Note: Installation instructions will be added once the project is ready for use)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the BSD 2-Clause License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors and users of LMpi
- Inspired by tools like SQLMap for database testing

