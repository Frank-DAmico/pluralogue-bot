# Pluralogue Bot - Complete Setup Guide

This guide will walk you through deploying the Pluralogue Bot step-by-step.

## Prerequisites

- Reddit account for the bot (u/Pluralogue)
- Reddit API credentials (approved developer access)
- At least one AI API key (Grok, Claude, or GPT-4)
- Python 3.11+ installed
- Git installed

## Part 1: Local Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Frank-DAmico/pluralogue-bot.git
cd pluralogue-bot
```

### Step 2: Create Virtual Environment

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example file:
```bash
   cp .env.example .env
```

2. Edit `.env` with your credentials:
```bash
   # Use your preferred text editor
   nano .env
   # or
   code .env
```

3. Fill in your actual credentials:
```
   REDDIT_CLIENT_ID=your_actual_client_id
   REDDIT_CLIENT_SECRET=your_actual_secret
   REDDIT_USERNAME=Pluralogue
   REDDIT_PASSWORD=your_bot_account_password
   
   # Add at least ONE AI API key
   ANTHROPIC_API_KEY=sk-ant-xxxxx  # If using Claude
   XAI_API_KEY=xai-xxxxx           # If using Grok
   OPENAI_API_KEY=sk-xxxxx         # If using GPT-4
```

### Step 5: Test Locally

Run in test mode first (won't actually post):
```bash
TEST_MODE=True python bot.py
```

You should see:
```
✅ Pluralogue Bot initialized as u/Pluralogue
📡 Monitoring: artificial, ArtificialIntelligence, singularity, consciousness, philosophy
🎯 Keywords: [number] active
🤖 AI Backend: grok
🚀 Pluralogue Bot starting...
👂 Listening to r/artificial+ArtificialIntelligence+singularity+consciousness+philosophy
🧪 Test mode: True
```

**If you see this, local setup works!** ✅

Press `Ctrl+C` to stop.

---

## Part 2: Cloud Deployment (Render.com - Free Tier)

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (easiest)
3. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. Click "New +" → "Background Worker"
2. Connect your `pluralogue-bot` repository
3. Configure:
   - **Name**: `pluralogue-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Plan**: `Free`

### Step 3: Add Environment Variables

In Render dashboard, go to "Environment" tab and add:
```
REDDIT_CLIENT_ID = [your value]
REDDIT_CLIENT_SECRET = [your value]
REDDIT_USERNAME = Pluralogue
REDDIT_PASSWORD = [your value]
ANTHROPIC_API_KEY = [your value]
XAI_API_KEY = [your value]
OPENAI_API_KEY = [your value]
TEST_MODE = False
```

**Important:** Set `TEST_MODE=False` to actually post responses.

### Step 4: Deploy

1. Click "Create Background Worker"
2. Render will build and deploy automatically
3. Check logs to confirm it's running

---

## Part 3: Monitoring & Management

### View Logs

**On Render:**
- Go to your service dashboard
- Click "Logs" tab
- Watch real-time activity

**Locally:**
- Logs are also saved to `interaction_log.jsonl`
- Each line is a JSON object with full interaction details

### Check Bot Activity

View what the bot has posted:
- https://reddit.com/user/Pluralogue

### Pause the Bot

**On Render:**
- Go to service dashboard
- Click "Manual Deploy" → "Suspend"

**Locally:**
- Press `Ctrl+C` in terminal

### Adjust Settings

Edit `config.py` to change:
- Which subreddits to monitor
- Keywords that trigger responses
- Rate limits
- AI backend preferences

After editing, commit and push:
```bash
git add config.py
git commit -m "Update configuration"
git push
```

Render will auto-redeploy.

---

## Part 4: Cost Estimates

### API Costs

**Anthropic (Claude):**
- ~$0.015 per response
- 50 responses/day = ~$0.75/day = ~$22/month

**OpenAI (GPT-4):**
- ~$0.02 per response
- 50 responses/day = ~$1.00/day = ~$30/month

**xAI (Grok):**
- Pricing TBD (likely similar to above)

**Render Hosting:**
- Free tier: $0/month (750 hours free)
- Paid tier: $7/month (if you need 24/7 uptime)

**Total: $22-37/month depending on which AI backend you use**

---

## Part 5: Troubleshooting

### "No AI backends available"

**Solution:** Check that at least one API key is set correctly in environment variables.

### "Daily limit reached"

**Solution:** This is normal. Bot is respecting rate limits. It will resume tomorrow.

### "Failed to get AI response"

**Possible causes:**
- API key invalid
- API service down
- Network issue
- Rate limit on AI service

**Solution:** Check logs for specific error. Try different AI backend.

### Bot not responding to any comments

**Check:**
1. Is `TEST_MODE=False`?
2. Are keywords in `config.py` spelled correctly?
3. Are the subreddits you're monitoring actually having discussions with those keywords?
4. Has rate limit been reached?

### Want to test specific behavior?

Run locally with:
```bash
TEST_MODE=True python bot.py
```

This shows what the bot WOULD post without actually posting.

---

## Part 6: Safety & Best Practices

### Always Monitor

Check the bot's activity daily for the first week:
- Are responses appropriate?
- Is it respecting rate limits?
- Is it being well-received?

### Adjust Based on Feedback

If you get negative feedback:
1. Pause the bot immediately
2. Review what went wrong
3. Adjust keywords/tone in config
4. Resume cautiously

### Respect Communities

If a subreddit moderator asks you to stop:
- Comply immediately
- Remove that subreddit from config
- Apologize if necessary

### Keep API Keys Secret

- Never commit `.env` file to GitHub
- Never share API keys
- Rotate keys if compromised

---

## Part 7: Updating the Bot

### Make Code Changes

1. Edit files locally
2. Test with `TEST_MODE=True`
3. Commit and push:
```bash
   git add .
   git commit -m "Describe your changes"
   git push
```
4. Render auto-deploys

### Update Dependencies

Edit `requirements.txt`, then:
```bash
pip install -r requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## Support

For issues or questions:
- Check logs first
- Review this guide
- Check Reddit's API documentation
- Contact Frank D'Amico (repository owner)

---

**The garden is ready to grow.** 🌱

*Last updated: November 2025*
