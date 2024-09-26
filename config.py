import subprocess, os, platform

import yaml
import platformdirs

_defaultConfigs = {
    'bottoken': 'ENTER BOT TOKEN HERE',
    'webhook': 'OPTIONAL LEAVE EMPTY FOR NO WEBHOOK, OTHERWISE ADD A URL HERE'
}

# Initialize the directory for configs
config_dir = platformdirs.user_config_dir('MaxioUptimeBotConfig', roaming=True, ensure_exists=True)
_config_file = os.path.join(config_dir, 'config.yml')
if not os.path.exists(_config_file):
    with open(_config_file, 'w') as f:
        yaml_content = yaml.dump(_defaultConfigs)
        f.write(yaml_content)

def get_config(key=None):
    if os.path.exists(_config_file):
        with open(_config_file, 'r') as f:
            config = yaml.safe_load(f)
            if key:
                return config[key]
            else:
                return config
    else:
        return None

def change_config():
    if platform.system() == 'Darwin':
        subprocess.call(('open', _config_file))
    elif platform.system() == 'Windows':
        os.startfile(_config_file)
    else:
        subprocess.call(('xdg-open', _config_file))