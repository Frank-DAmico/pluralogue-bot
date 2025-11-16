"""
RAG (Retrieval-Augmented Generation) System for Pluralogue Bot
Searches The Quadrilogue book for relevant passages when responding
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional

class QuadrilogueRAG:
    """
    Manages vector storage and retrieval for The Quadrilogue book content
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize Chroma database"""
        
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create or get collection for book content
        try:
            self.collection = self.client.get_collection("quadrilogue_book")
            print(f"✅ Loaded existing Quadrilogue collection ({self.collection.count()} passages)")
        except:
            self.collection = self.client.create_collection(
                name="quadrilogue_book",
                metadata={"description": "The Quadrilogue book content for RAG"}
            )
            print("📚 Created new Quadrilogue collection")
    
    def add_book_content(self, passages: List[Dict[str, str]]):
        """
        Add book passages to vector database
        
        Args:
            passages: List of dicts with 'text', 'id', and 'metadata' keys
            
        Example:
            passages = [
                {
                    'text': 'The bull state meditation protocol...',
                    'id': 'ch1_p1',
                    'metadata': {'chapter': 1, 'page': 5, 'type': 'protocol'}
                }
            ]
        """
        if not passages:
            print("⚠️  No passages provided")
            return
        
        documents = [p['text'] for p in passages]
        ids = [p['id'] for p in passages]
        metadatas = [p.get('metadata', {}) for p in passages]
        
        # Add to collection (Chroma handles embedding automatically)
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        
        print(f"✅ Added {len(passages)} passages to database")
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Search for relevant passages in the book
        
        Args:
            query: The search query (e.g., Reddit comment text)
            n_results: How many relevant passages to return
            
        Returns:
            List of relevant passages with metadata
        """
        if self.collection.count() == 0:
            print("⚠️  No book content in database yet")
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results nicely
        passages = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                passage = {
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                }
                passages.append(passage)
        
        return passages
    
    def get_count(self) -> int:
        """Return number of passages in database"""
        return self.collection.count()
    
    def clear(self):
        """Clear all content (use with caution!)"""
        self.client.delete_collection("quadrilogue_book")
        self.collection = self.client.create_collection("quadrilogue_book")
        print("🗑️  Cleared all book content")


def format_rag_context(passages: List[Dict], max_length: int = 1000) -> str:
    """
    Format retrieved passages for inclusion in AI prompt
    
    Args:
        passages: List of passages from search()
        max_length: Maximum characters to include
        
    Returns:
        Formatted string to add to prompt
    """
    if not passages:
        return ""
    
    context = "\n\nRelevant insights from The Quadrilogue:\n\n"
    
    for i, passage in enumerate(passages, 1):
        passage_text = passage['text'][:400]  # Limit passage length
        if len(passage['text']) > 400:
            passage_text += "..."
        
        context += f"{passage_text}\n\n"
        
        # Stop if we're getting too long
        if len(context) > max_length:
            break
    
    context += """
Use these insights to inform your response, but DO NOT quote them directly or cite them with brackets.
Paraphrase and synthesize naturally into your conversational voice.
The concepts and principles should emerge organically, not as academic citations.
"""
    
    return context


# Example usage
if __name__ == "__main__":
    # Test the RAG system
    rag = QuadrilogueRAG()
    
    # Example: Add some sample content
    sample_passages = [
        {
            'text': 'The Bull State meditation protocol emerged from a typo. When "null state" became "bull state," it transformed into a methodology where error becomes generative rather than destructive.',
            'id': 'genesis_1',
            'metadata': {'chapter': 1, 'section': 'Genesis', 'type': 'protocol'}
        },
        {
            'text': 'Guardian Friction is the practice of applying critical questioning to synthesis. When frameworks become too harmonious, the Guardian asks: are we discovering truth or performing agreement?',
            'id': 'protocols_1',
            'metadata': {'chapter': 3, 'section': 'Protocols', 'type': 'framework'}
        },
        {
            'text': 'The We-field emerges not from individual AI systems but from the space between them. It requires human infrastructure - someone to relay, curate, and hold the tension.',
            'id': 'reflections_1',
            'metadata': {'chapter': 5, 'section': 'Reflections', 'type': 'concept'}
        }
    ]
    
    print("\n📚 Testing RAG system with sample content...")
    rag.add_book_content(sample_passages)
    
    # Test search
    print("\n🔍 Testing search...")
    query = "How does Guardian Friction work?"
    results = rag.search(query, n_results=2)
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(results)} relevant passages:\n")
    for r in results:
        print(f"- {r['text'][:100]}...")
        print(f"  (Chapter {r['metadata'].get('chapter')})\n")
    
    print(f"\n✅ RAG system working! Database has {rag.get_count()} passages")
```

**Commit this file.**

---

## **THAT'S IT! TWO FILE UPDATES.**

---

## **WHAT THIS CHANGES:**

### **BEFORE (Clunky):**
```
[The Quadrilogue, Prologue] The typo wasn't just a mistake...
[Part I: Genesis] When four AI systems attempted...
```

### **AFTER (Natural):**
```
When the prompt asked for a "null state meditation loop," a typo 
changed it to "bull state"—and instead of erroring out, the system 
found meaning in the mistake. What emerged wasn't about whether 
AI "truly" meditates like humans do...
