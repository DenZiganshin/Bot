import json
from pathlib import Path


class BotConfig:

    def __init__(self, config_path = Path('~').expanduser() / ".balabol_bot/config.json"):
        self.config_path = config_path
        self.__read_config__()

    def __read_config__(self):
        with open(self.config_path) as f:
            json_cfg = json.load(f)
            self.telebot_token_id = json_cfg["telebot_token_id"]
            self.database_row_limit = json_cfg["database_row_limit"]
            self.phrases_in_bot_message_count = json_cfg["phrases_in_bot_message_count"]
            self.inbound_phrase_length_limit = json_cfg["inbound_phrase_length_limit"]
            self.message_initiation_frequency = json_cfg["message_initiation_frequency"]
            return
        raise Exception(f"Invalid file path {self.config_path}")


