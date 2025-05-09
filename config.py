import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Create directories if they don't exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Model parameters
MODEL_CONFIG = {
    'intent_classifier': {
        'model_type': 'naive_bayes',
        'num_classes': 5,
        'min_samples_per_class': 5
    },
    'openai': {
        'model': 'gpt-4',
        'temperature': 0.7,
        'max_tokens': 500
    }
}

# Dataset configuration
DATASET_CONFIG = {
    'restaurants_file': RAW_DATA_DIR / 'restaurants.csv'
}

# API configurations
API_CONFIG = {
    'open_street_map': {
        'api_key': os.getenv('OPENSTREETMAP_API_KEY', ''),
        'base_url': 'https://api.openstreetmap.org/'
    }
}

# Application settings
APP_CONFIG = {
    'debug': True,
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 7860)),
    'share': True
}

# NLP settings
NLP_CONFIG = {
    'spacy_model': 'en_core_web_sm',
    'min_confidence': 0.7,
    'max_tokens': 1000
}