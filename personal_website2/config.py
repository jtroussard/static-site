import os
import json

with open('/etc/mpws2-config.json') as config_file:
    config = json.load(config_file)


class Config:
    # Application configurations
    SECRET_KEY = config.get('SECRET_KEY')
