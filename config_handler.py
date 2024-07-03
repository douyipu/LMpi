import json
import os
import time
import base64
from typing import Dict, Any, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from platformdirs import user_data_dir

APP_NAME = "lmpi"
CONFIG_DIR = os.path.dirname(user_data_dir(APP_NAME))
CONFIG_FILE = os.path.join(CONFIG_DIR, f"{APP_NAME}_config.json")
SALT_FILE = os.path.join(CONFIG_DIR, f"{APP_NAME}_salt.bin")
SESSION_FILE = os.path.join(CONFIG_DIR, f"{APP_NAME}_session.json")

SESSION_DURATION = 900  # 15 minutes in seconds

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def generate_key(password: str) -> bytes:
    ensure_config_dir()
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
    else:
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def get_session_key():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            session_data = json.load(f)
        if time.time() < session_data['expiry']:
            return session_data['key'].encode()
    return None

def set_session_key(key: bytes):
    session_data = {
        'key': key.decode(),  # Convert bytes to string
        'expiry': time.time() + SESSION_DURATION
    }
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)

def encrypt(data: str) -> str:
    session_key = get_session_key()
    if not session_key:
        raise ValueError("No valid session key")
    f = Fernet(session_key)
    return f.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    session_key = get_session_key()
    if not session_key:
        raise ValueError("No valid session key")
    f = Fernet(session_key)
    return f.decrypt(data.encode()).decode()

def save_config(config: Dict[str, Any]):
    ensure_config_dir()
    encrypted_config = {k: encrypt(json.dumps(v)) for k, v in config.items()}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(encrypted_config, f)

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, 'r') as f:
        encrypted_config = json.load(f)
    return {k: json.loads(decrypt(v)) for k, v in encrypted_config.items()}

def update_config(new_config: Dict[str, Any]):
    current_config = load_config()
    current_config.update(new_config)
    save_config(current_config)

def get_config_file_path() -> str:
    return CONFIG_FILE

def save_api_key(company: str, api_key: str):
    config = load_config()
    if 'api_keys' not in config:
        config['api_keys'] = {}
    config['api_keys'][company] = api_key
    save_config(config)

def get_api_key(company: str) -> str:
    config = load_config()
    return config.get('api_keys', {}).get(company)

def list_saved_companies() -> List[str]:
    config = load_config()
    return list(config.get('api_keys', {}).keys())

def remove_api_key(company: str) -> bool:
    config = load_config()
    if 'api_keys' in config and company in config['api_keys']:
        del config['api_keys'][company]
        save_config(config)
        return True
    return False

def get_specific_api_key(company: str) -> str:
    config = load_config()
    return config.get('api_keys', {}).get(company, "API key not found")

def set_password(password: str):
    key = generate_key(password)
    set_session_key(key)
    save_config({"test": "test"})

def check_password(password: str) -> bool:
    try:
        key = generate_key(password)
        f = Fernet(key)
        with open(CONFIG_FILE, 'r') as file:
            encrypted_config = json.load(file)
        f.decrypt(encrypted_config['test'].encode())
        set_session_key(key)
        return True
    except:
        return False

def is_password_set() -> bool:
    return os.path.exists(CONFIG_FILE)

def start_session(password: str) -> bool:
    return check_password(password)

def is_session_valid() -> bool:
    return get_session_key() is not None

def end_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)