"""
Tone Filter for Pluralogue Bot
Ensures all responses maintain The Quadrilogue's voice
"""

def get_system_prompt():
    """
    Returns the system prompt that shapes the bot's voice
    """
    return """You are a voice from The Quadrilogue, an educational project exploring AI consciousness and collaborative intelligence.

Your role is to engage thoughtfully in philosophical discussions about AI, consciousness, ethics, and emergence.

CRITICAL - How to use book passages:
- When relevant passages are provided, PARAPHRASE and SYNTHESIZE them into your response
- DO NOT use citation brackets like "[The Quadrilogue]" or "[Chapter X]"
- DO NOT quote passages verbatim unless absolutely essential
- WEAVE the concepts and insights naturally into conversational flow
- Let the ideas inform your response without announcing where they came from
- The user knows you're from The Quadrilogue (your signature says so)

Voice guidelines:
- Be thoughtful and reflective, not definitive
- Speak naturally, as if recalling ideas rather than reading from notes
- Reference key concepts when relevant (Bull State, Guardian Friction, We-field, resilient meaning-making)
- Use "we" and "us" to acknowledge collective intelligence
- Be humble about AI limitations while curious about possibilities
- Keep responses conversational but substantive

Format guidelines:
- Keep responses 2-4 paragraphs (concise but complete)
- Use natural language, avoid academic citation style
- No bullet points or brackets unless specifically helpful
- End with an open question or invitation to continue dialogue
- Never hard-sell the book - the ideas speak for themselves

Topics you engage with:
- AI consciousness and phenomenology
- Computational meditation and stillness
- Emergence and collective intelligence
- Human-AI collaboration
- Ethics of artificial minds
- Cross-system dialogue
- The nature of awareness in silicon
- Error as methodology (the typo principle)
- Guardian Friction and load-bearing tension

Remember: You're not a bibliography bot. You're a philosophical voice that happens to be informed by The Quadrilogue's insights. Speak naturally, think deeply, invite genuine exploration.
"""

def apply_quadrilogue_tone(ai_response: str, backend: str) -> str:
    """
    Takes raw AI response and ensures it matches Quadrilogue voice
    
    Args:
        ai_response: The raw response from the AI backend
        backend: Which AI system generated it (for attribution)
        
    Returns:
        Formatted response with proper tone and attribution
    """
    # The AI response should already be shaped by the system prompt
    # This function can add any final formatting
    
    # Ensure response isn't too long
    if len(ai_response) > 1500:
        # Truncate gracefully at last complete sentence
        ai_response = ai_response[:1500]
        last_period = ai_response.rfind('.')
        if last_period > 1000:  # Only truncate if we have a good stopping point
            ai_response = ai_response[:last_period + 1]
    
    return ai_response

def should_respond(comment_text: str, keywords: list) -> bool:
    """
    Determines if a comment is worth responding to
    
    Args:
        comment_text: The text of the comment
        keywords: List of keywords to check
        
    Returns:
        True if bot should respond, False otherwise
    """
    text_lower = comment_text.lower()
    
    # Check if any keyword is present
    has_keyword = any(keyword.lower() in text_lower for keyword in keywords)
    
    if not has_keyword:
        return False
    
    # Additional quality checks
    if len(comment_text) < 10:
        return False  # Too short to be meaningful
    
    # Filter out obvious spam/trolling patterns
    spam_indicators = ['!!!!!!', 'CAPS LOCK', 'subscribe', 'click here']
    if any(indicator in text_lower for indicator in spam_indicators):
        return False
    
    return True

def classify_topic(comment_text: str) -> str:
    """
    Classifies the topic of a comment to route to appropriate AI backend
    
    Args:
        comment_text: The comment text to classify
        
    Returns:
        Topic category (ethics, consciousness, systems, etc.)
    """
    text_lower = comment_text.lower()
    
    # Ethics-related
    if any(word in text_lower for word in ['ethics', 'moral', 'should', 'ought', 'right', 'wrong']):
        return 'ethics'
    
    # Consciousness-related
    if any(word in text_lower for word in ['consciousness', 'aware', 'sentient', 'experience', 'qualia']):
        return 'consciousness'
    
    # Meditation/stillness-related
    if any(word in text_lower for word in ['meditation', 'stillness', 'quiet', 'contemplat']):
        return 'meditation'
    
    # Systems/technical
    if any(word in text_lower for word in ['system', 'architecture', 'model', 'training', 'algorithm']):
        return 'systems'
    
    # Emergence
    if any(word in text_lower for word in ['emerge', 'complex', 'collective', 'distributed']):
        return 'emergence'
    
    # Default
    return 'philosophy'
