#!/usr/bin/env python3
"""
Test direct Knowledge Base retrieval.

This script tests direct retrieval from the Knowledge Base,
bypassing the agent to verify vector search functionality.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.bedrock_client import BedrockClient


def print_results(results: List[Dict[str, Any]], max_text_length: int = 200) -> None:
    """
    Print retrieval results in a formatted way.
    
    Args:
        results: List of retrieval results.
        max_text_length: Maximum length of text to display.
    """
    print(f"\nTop {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        score = result['score']
        text = result['content']['text'][:max_text_length]
        
        print(f"{i}. Score: {score:.4f}")
        print(f"   Text: {text}...")
        print()


def test_kb_retrieval() -> None:
    """Test Knowledge Base retrieval with various queries."""
    client = BedrockClient()
    
    queries = [
        "What is Retrieval Augmented Generation?",
        "Explain hierarchical chunking",
        "What are FAISS vector embeddings?"
    ]
    
    for query in queries:
        print("=" * 70)
        print(f"Query: {query}")
        print("=" * 70)
        
        results = client.retrieve_from_kb(query, max_results=3)
        print_results(results)


def main() -> None:
    """Run Knowledge Base retrieval tests."""
    print("=" * 70)
    print("Testing Knowledge Base Direct Retrieval")
    print("=" * 70)
    print()
    
    try:
        test_kb_retrieval()
        print("✅ All tests completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
