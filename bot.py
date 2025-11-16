"""
Pluralogue Bot - Main Bot Logic
The Quadrilogue in conversation on Reddit
"""

import praw
import time
import json
from datetime import datetime, timedelta
from typing import Optional, Dict
import anthropic
import openai
import requests

import config
from tone_filter import (
    get_system_prompt,
    apply_quadrilogue_tone,
    should_respond,
    classify_topic
)
from rag_system import QuadrilogueRAG, format_rag_context

class PlurologueBot:
    def __init__(self):
        """Initialize the bot with Reddit and AI API clients"""
        
        # Initialize Reddit client
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent=config.USER_AGENT
        )
        
        # Initialize RAG system
        self.rag = QuadrilogueRAG()
        
        # Initialize AI clients (only if keys are provided)
        self.anthropic_client = None
        if config.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        self.openai_client = None
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
            self.openai_client = openai
        
        # Rate limiting tracking
        self.response_times = []
        self.responded_to = set()  # Track comment IDs we've already responded to
        
        print(f"✅ Pluralogue Bot initialized as u/{config.REDDIT_USERNAME}")
        print(f"📡 Monitoring: {', '.join(config.SUBREDDITS)}")
        print(f"🎯 Keywords: {len(config.KEYWORDS)} active")
        print(f"🤖 AI Backend: {config.DEFAULT_BACKEND}")
        
    def can_respond(self) -> bool:
        """Check if bot can respond based on rate limits"""
        now = datetime.now()
        
        # Clean up old timestamps
        cutoff_day = now - timedelta(days=1)
        cutoff_hour = now - timedelta(hours=1)
        
        self.response_times = [
            t for t in self.response_times 
            if t > cutoff_day
        ]
        
        # Check daily limit
        if len(self.response_times) >= config.MAX_RESPONSES_PER_DAY:
            print(f"⏸️  Daily limit reached ({config.MAX_RESPONSES_PER_DAY})")
            return False
        
        # Check hourly limit
        recent_responses = [t for t in self.response_times if t > cutoff_hour]
        if len(recent_responses) >= config.MAX_RESPONSES_PER_HOUR:
            print(f"⏸️  Hourly limit reached ({config.MAX_RESPONSES_PER_HOUR})")
            return False
        
        # Check cooldown
        if self.response_times:
            last_response = max(self.response_times)
            cooldown = timedelta(minutes=config.COOLDOWN_MINUTES)
            if now - last_response < cooldown:
                wait_time = (cooldown - (now - last_response)).seconds // 60
                print(f"⏸️  Cooldown active (wait {wait_time} min)")
                return False
        
        return True
    
    def get_ai_response(self, comment_text: str, topic: str) -> Optional[Dict[str, str]]:
        """
        Get response from appropriate AI backend
        
        Returns:
            Dict with 'response' and 'backend' keys, or None if failed
        """
        # Determine which backend to use
        backend = config.TOPIC_ROUTING.get(topic, config.DEFAULT_BACKEND)
        
        # Prepare the prompt
        system_prompt = get_system_prompt()
        
        # Search book for relevant content (RAG)
        relevant_passages = self.rag.search(comment_text, n_results=2)
        rag_context = format_rag_context(relevant_passages) if relevant_passages else ""
        
        user_prompt = f"A Reddit user wrote this comment in a discussion about {topic}:\n\n\"{comment_text}\"{rag_context}\n\nRespond thoughtfully as a voice from The Quadrilogue."
        
        try:
            # Try Grok (xAI) first
            if backend == 'grok' and config.XAI_API_KEY:
                response_text = self._call_grok(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'Grok (xAI)'}
            
            # Try Claude
            elif backend == 'claude' and self.anthropic_client:
                response_text = self._call_claude(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'Claude (Anthropic)'}
            
            # Try GPT-4
            elif backend == 'gpt4' and self.openai_client:
                response_text = self._call_gpt4(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'GPT-4 (OpenAI)'}
            
            # Fallback to any available backend
            print(f"⚠️  Preferred backend '{backend}' unavailable, trying fallback...")
            
            if self.anthropic_client:
                response_text = self._call_claude(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'Claude (Anthropic)'}
            
            if self.openai_client:
                response_text = self._call_gpt4(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'GPT-4 (OpenAI)'}
            
            if config.XAI_API_KEY:
                response_text = self._call_grok(system_prompt, user_prompt)
                if response_text:
                    return {'response': response_text, 'backend': 'Grok (xAI)'}
            
            print("❌ No AI backends available")
            return None
            
        except Exception as e:
            print(f"❌ Error getting AI response: {e}")
            return None
    
    def _call_claude(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call Claude API"""
        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"❌ Claude API error: {e}")
            return None
    
    def _call_gpt4(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call GPT-4 API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ GPT-4 API error: {e}")
            return None
    
    def _call_grok(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Call Grok API (xAI)"""
        try:
            # Note: This is placeholder - actual xAI API endpoint may differ
            # Update when xAI releases official API documentation
            headers = {
                "Authorization": f"Bearer {config.XAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "grok-beta",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",  # Placeholder URL
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"❌ Grok API returned status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Grok API error: {e}")
            return None
    
    def process_comment(self, comment):
        """Process a single comment and respond if appropriate"""
        
        # Skip if already responded to this comment
        if comment.id in self.responded_to:
            return
        
        # Skip if this is our own comment
        if comment.author and comment.author.name == config.REDDIT_USERNAME:
            return
        
        # Check if comment is worth responding to
        if not should_respond(comment.body, config.KEYWORDS):
            return
        
        # Check rate limits
        if not self.can_respond():
            return
        
        print(f"\n📝 Potential response target:")
        print(f"   Sub: r/{comment.subreddit.display_name}")
        print(f"   Author: u/{comment.author.name if comment.author else '[deleted]'}")
        print(f"   Text: {comment.body[:100]}...")
        
        # Classify topic
        topic = classify_topic(comment.body)
        print(f"   Topic: {topic}")
        
        # Get AI response
        ai_result = self.get_ai_response(comment.body, topic)
        if not ai_result:
            print("❌ Failed to get AI response")
            return
        
        # Apply tone filter and add attribution
        response = apply_quadrilogue_tone(ai_result['response'], ai_result['backend'])
        response += config.ATTRIBUTION.format(backend=ai_result['backend'])
        
        # Post response (or log if in test mode)
        if config.TEST_MODE:
            print("\n🧪 TEST MODE - Would have posted:")
            print("-" * 60)
            print(response)
            print("-" * 60)
        else:
            try:
                comment.reply(response)
                print(f"✅ Posted response using {ai_result['backend']}")
            except Exception as e:
                print(f"❌ Failed to post: {e}")
                return
        
        # Log this response
        self.response_times.append(datetime.now())
        self.responded_to.add(comment.id)
        
        # Save to file log
        self.log_interaction(comment, response, ai_result['backend'])
    
    def log_interaction(self, comment, response: str, backend: str):
        """Log interaction to file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'comment_id': comment.id,
            'subreddit': comment.subreddit.display_name,
            'author': comment.author.name if comment.author else '[deleted]',
            'comment_text': comment.body,
            'bot_response': response,
            'backend': backend,
            'permalink': f"https://reddit.com{comment.permalink}"
        }
        
        # Append to log file
        try:
            with open('interaction_log.jsonl', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️  Failed to write log: {e}")
    
    def run(self):
        """Main bot loop"""
        print("\n🚀 Pluralogue Bot starting...\n")
        
        # Create subreddit stream
        subreddit_string = '+'.join(config.SUBREDDITS)
        subreddit = self.reddit.subreddit(subreddit_string)
        
        print(f"👂 Listening to r/{subreddit_string}")
        print(f"⏱️  Rate limits: {config.MAX_RESPONSES_PER_HOUR}/hour, {config.MAX_RESPONSES_PER_DAY}/day")
        print(f"🧪 Test mode: {config.TEST_MODE}\n")
        
        # Stream comments
        try:
            for comment in subreddit.stream.comments(skip_existing=True):
                try:
                    self.process_comment(comment)
                except Exception as e:
                    print(f"❌ Error processing comment: {e}")
                    continue
                
                # Small delay to avoid hammering Reddit
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n👋 Bot stopped by user")
        except Exception as e:
            print(f"\n\n❌ Fatal error: {e}")
            raise

if __name__ == "__main__":
    bot = PlurologueBot()
    bot.run()
