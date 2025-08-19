import streamlit_authenticator as stauth
import yaml
import os
from yaml.loader import SafeLoader
from utils.config import COOKIE_KEY


def get_authenticator():
    # Try multiple possible paths for config.yaml
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml"),
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "utils",
            "config.yaml",
        ),
        "utils/config.yaml",
        "config.yaml",
    ]

    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            break

    if config_path is None:
        raise FileNotFoundError("config.yaml not found in any expected location")

    print(f"Using config file at: {config_path}")

    with open(config_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        COOKIE_KEY,
        config["cookie"]["expiry_days"],
        config.get("preauthorized", []),
    )

    return authenticator
