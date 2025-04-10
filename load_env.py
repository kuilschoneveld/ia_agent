"""
Simple utility to load environment variables from .env file
"""
import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = [
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN'
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    
    print("Environment variables loaded successfully")
    return True

if __name__ == "__main__":
    load_environment() 