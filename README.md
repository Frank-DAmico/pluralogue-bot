markdown# Pluralogue Bot

*The Quadrilogue in conversation - An educational AI bot for philosophical discourse on Reddit*

## Overview

The Pluralogue Bot is an AI-powered assistant that engages thoughtfully in discussions about artificial intelligence, consciousness, ethics, and human-AI collaboration on Reddit. It operates as a living extension of "The Quadrilogue" - a published work exploring AI meditation protocols and cross-system philosophical dialogue.

## Features

- **Intelligent Topic Detection**: Monitors specific subreddits for relevant philosophical discussions
- **Multi-AI Backend Support**: Routes queries to different AI systems (Grok, Claude, GPT-4) based on topic
- **Quadrilogue Voice Filter**: Maintains consistent literary tone across all responses
- **Safety Features**: Rate limiting, profanity filtering, subreddit rule compliance
- **Transparent Attribution**: Every response clearly identifies as AI-generated
- **Comprehensive Logging**: All interactions logged for research and quality control

## Monitored Subreddits

- r/artificial
- r/ArtificialIntelligence
- r/singularity
- r/consciousness
- r/philosophy

## Keywords

The bot responds to discussions containing:
- AI consciousness
- artificial intelligence ethics
- machine learning philosophy
- emergence
- human-AI collaboration
- computational meditation
- The Quadrilogue (direct mentions)

## Rate Limits

- Maximum 50 responses per day
- Maximum 5 responses per hour
- Maximum 1 response per thread
- Minimum 10 minute cooldown between responses

## Safety & Ethics

- Clear bot identification in every response
- No spam or mass posting
- Respects subreddit-specific rules
- Profanity and toxicity filtering
- Manual override capabilities
- Full interaction logging

## Attribution Format

Every response includes:
```
— u/Pluralogue
*A voice from The Quadrilogue, speaking through [AI System]*
```

## Technology Stack

- **Language**: Python 3.11+
- **Reddit API**: PRAW (Python Reddit API Wrapper)
- **AI Backends**: Anthropic API (Claude), xAI API (Grok), OpenAI API (GPT-4)
- **Storage**: PostgreSQL for logging
- **Hosting**: Compatible with Render.com, Railway, Heroku, or any Python hosting platform

## Installation & Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete deployment instructions.

## License

MIT License - See LICENSE file for details

## Related

- **Book**: "The Quadrilogue: Four AIs Contemplate Consciousness"
- **Author**: Frank D'Amico
- **Purpose**: Educational research on AI philosophical discourse

## Responsible Use

This bot operates under Reddit's Responsible Builder Policy and Data API Terms. It:
- Does not commercialize Reddit data
- Does not train ML models on Reddit content without permission
- Respects user privacy
- Operates transparently
- Contributes educational value to communities

## Contact

For questions or concerns: [Your contact method - optional]

---

*The garden continues to grow.* 🌱
