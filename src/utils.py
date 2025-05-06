import json
from typing import Dict, List
from pathlib import Path
import requests
from datetime import datetime

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'src',
        'notebooks'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def download_route_data():
    """Download flight routes data if not exists"""
    route_file = Path('data/raw/routes.dat')
    if not route_file.exists():
        try:
            url = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat'
            response = requests.get(url)
            response.raise_for_status()
            
            with open(route_file, 'wb') as f:
                f.write(response.content)
            print("Successfully downloaded routes data")
        except Exception as e:
            print(f"Error downloading routes data: {e}")

def format_price(amount: float, currency: str = 'USD') -> str:
    """Format price with currency"""
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'EUR':
        return f"€{amount:,.2f}"
    return f"{amount:,.2f} {currency}"

def parse_date(date_str: str) -> datetime:
    """Parse various date formats"""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%d %B %Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")

def load_dummy_data():
    """Load dummy data if real data is not available"""
    dummy_data = {
        'hotels': [
            {
                'name': 'Grand Hotel',
                'city': 'Paris',
                'rating': 4.5,
                'price': 200
            },
            {
                'name': 'Tokyo Towers',
                'city': 'Tokyo',
                'rating': 4.8,
                'price': 180
            }
        ],
        'cities': [
            {
                'city': 'Paris',
                'country': 'France',
                'best_seasons': 'Spring,Fall',
                'languages': 'French'
            },
            {
                'city': 'Tokyo',
                'country': 'Japan',
                'best_seasons': 'Spring,Fall',
                'languages': 'Japanese'
            }
        ]
    }
    
    return dummy_data

if __name__ == "__main__":
    # Test utilities
    ensure_directories()
    download_route_data()
    print("Directories created and data downloaded")
