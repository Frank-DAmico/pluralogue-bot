"""
Configuration settings for Pluralogue Bot
Edit these settings to customize bot behavior
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME', 'Pluralogue')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
USER_AGENT = 'Pluralogue Bot v1.0 by u/Pluralogue (Educational AI Philosophy Bot)'

# AI API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
XAI_API_KEY = os.getenv('XAI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Default AI Backend (grok, claude, or gpt4)
DEFAULT_BACKEND = 'grok'

# Subreddits to Monitor
SUBREDDITS = [
    'artificial',
    'ArtificialIntelligence',
    'singularity',
    'consciousness',
    'philosophy'
]

# Keywords that trigger responses (case-insensitive)
KEYWORDS = [
    'ai consciousness',
    'artificial intelligence ethics',
    'machine learning philosophy',
    'ai meditation',
    'computational consciousness',
    'emergence',
    'human-ai collaboration',
    'the quadrilogue',
    'pluralogue'
]

# Topics for AI Backend Routing
TOPIC_ROUTING = {
    'ethics': 'claude',
    'consciousness': 'claude',
    'meditation': 'grok',
    'emergence': 'grok',
    'systems': 'gpt4',
    'science': 'gpt4',
    'philosophy': 'claude'
}

# Rate Limiting
MAX_RESPONSES_PER_DAY = int(os.getenv('MAX_RESPONSES_PER_DAY', 50))
MAX_RESPONSES_PER_HOUR = int(os.getenv('MAX_RESPONSES_PER_HOUR', 5))
COOLDOWN_MINUTES = int(os.getenv('COOLDOWN_MINUTES', 10))

# Safety Settings
PROFANITY_FILTER = True
MIN_COMMENT_LENGTH = 10  # Don't reply to very short comments
MAX_RESPONSE_LENGTH = 1500  # Keep responses concise

# Attribution Signature
ATTRIBUTION = "\n\n— u/Pluralogue\n*A voice from The Quadrilogue, speaking through {backend}*"

# Logging
LOG_TO_DATABASE = os.getenv('DATABASE_URL') is not None
DATABASE_URL = os.getenv('DATABASE_URL')

# Test Mode (set to True to log but not actually post)
TEST_MODE = os.getenv('TEST_MODE', 'False').lower() == 'true'
