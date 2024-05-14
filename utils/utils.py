import os
from dotenv import load_dotenv


class Config:

    @staticmethod
    def get_config():
        # Load .env file
        load_dotenv()

        # Get database config
        config_data = {
            'DB_HOST': os.getenv('DB_HOST'),
            'DB_NAME': os.getenv('DB_NAME'),
            'DB_USER': os.getenv('DB_USER'),
            'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        }

        return config_data
