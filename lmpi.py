#!/usr/bin/env python

"""
Copyright (c) 2024 lmpi developer (https://douyipu.github.io/)
See the file 'LICENSE' for copying permission
"""

import argparse
import sys
import logging
from getpass import getpass

from config_handler import (
    load_config, update_config, get_config_file_path, 
    save_api_key, get_api_key, list_saved_companies, remove_api_key,
    get_specific_api_key, set_password, check_password, is_password_set,
    start_session, is_session_valid, end_session
)
from model_registry import get_company_for_model, get_model_type, list_available_models, is_valid_model

def banner():
    print("""
    ██╗     ███╗   ███╗██████╗ ██╗
    ██║     ████╗ ████║██╔══██╗██║
    ██║     ██╔████╔██║██████╔╝██║
    ██║     ██║╚██╔╝██║██╔═══╝ ██║
    ███████╗██║ ╚═╝ ██║██║     ██║
    ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝
    
    LMpi - Language Model Prompt Injector
    By douyipu (https://douyipu.github.io/)
    """)

def parse_arguments():
    parser = argparse.ArgumentParser(description="LMpi - Language Model Prompt Injector")
    parser.add_argument("-m", "--model", help="Target language model")
    parser.add_argument("-p", "--prompt", help="Prompt to inject")
    parser.add_argument("-o", "--output", help="Output file for results")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--save-config", action="store_true", help="Save current configuration")
    parser.add_argument("--load-config", action="store_true", help="Load saved configuration")
    parser.add_argument("--show-config-path", action="store_true", help="Show the current configuration file path")
    parser.add_argument("--save-api-key", nargs=2, metavar=('COMPANY', 'API_KEY'), help="Save an API key for a company")
    parser.add_argument("--list-companies", action="store_true", help="List all companies with saved API keys")
    parser.add_argument("--remove-api-key", metavar='COMPANY', help="Remove the API key for a specific company")
    parser.add_argument("--list-models", action="store_true", help="List all available models")
    parser.add_argument("--show-api-key", metavar='COMPANY', help="Show the API key for a specific company")
    parser.add_argument("--set-password", action="store_true", help="Set or change the encryption password")
    parser.add_argument("--logout", action="store_true", help="End the current session")
    return parser.parse_args()

def get_password(prompt="Enter your password: "):
    return getpass(prompt)

def ensure_auth():
    if not is_password_set():
        print("No password set. Please set a password first using --set-password")
        sys.exit(1)
    
    if not is_session_valid():
        password = get_password()
        if not start_session(password):
            print("Incorrect password.")
            sys.exit(1)

def main():
    banner()
    args = parse_arguments()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    if args.logout:
        end_session()
        print("Logged out successfully.")
        return

    if args.set_password:
        new_password = get_password("Enter new password: ")
        confirm_password = get_password("Confirm new password: ")
        if new_password == confirm_password:
            set_password(new_password)
            print("Password set successfully.")
        else:
            print("Passwords do not match.")
        return

    if args.show_config_path:
        print(f"Configuration file path: {get_config_file_path()}")
        return

    ensure_auth()

    if args.save_api_key:
        company, api_key = args.save_api_key
        save_api_key(company, api_key)
        print(f"Saved API key for {company}")
        return

    if args.list_companies:
        companies = list_saved_companies()
        if companies:
            print("Companies with saved API keys:")
            for company in companies:
                print(f"- {company}")
        else:
            print("No API keys saved yet.")
        return

    if args.remove_api_key:
        if remove_api_key(args.remove_api_key):
            print(f"Removed API key for {args.remove_api_key}")
        else:
            print(f"No API key found for {args.remove_api_key}")
        return

    if args.show_api_key:
        api_key = get_specific_api_key(args.show_api_key)
        print(f"API key for {args.show_api_key}: {api_key}")
        return

    if args.list_models:
        models = list_available_models()
        for company, model_list in models.items():
            print(f"{company}:")
            for model in model_list:
                print(f"  - {model}")
        return

    if args.load_config:
        config = load_config()
        args.model = config.get('model', args.model)
        args.prompt = config.get('prompt', args.prompt)
        args.output = config.get('output', args.output)
        print(f"Loaded configuration from {get_config_file_path()}")

    if args.save_config:
        new_config = {
            'model': args.model,
            'prompt': args.prompt,
            'output': args.output
        }
        update_config(new_config)
        print(f"Saved current configuration to {get_config_file_path()}")

    if not args.model or not args.prompt:
        print("Error: --model and --prompt arguments are required.")
        return

    if not is_valid_model(args.model):
        print(f"Error: Invalid model: {args.model}")
        return

    # Here you would typically call your model testing function
    print(f"Testing model {args.model} with prompt: {args.prompt}")

if __name__ == "__main__":
    main()