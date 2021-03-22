import os
import json
import platform

file = "mpws2-config.json"

if platform.system().lower() == "windows":
    win_dir = "C:/Users/Public/appdata"
    win_path = os.path.join(win_dir, file)
    with open(win_path) as config_file:
        config = json.load(config_file)
else:
    with open(file) as config_file:
        config = json.load(config_file)


class Config:
    # Application configurations
    SECRET_KEY = config.get('SECRET_KEY')
