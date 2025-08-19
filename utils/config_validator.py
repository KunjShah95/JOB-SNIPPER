import yaml
import sys
from utils import error_handler

def validate_config(config_path='utils/config.yaml'):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        # Example validation: check for required keys
        required_keys = ['database', 'logging']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
        print("Config validation passed.")
        return True
    except Exception as e:
        error_handler.handle_exception(e)
        print(f"Config validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_config()
