#!/usr/bin/env python3
"""
Test Bedrock Agent with RAG capabilities.

This script tests the agent's ability to retrieve relevant context
from the Knowledge Base and generate informed responses.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.bedrock_client import BedrockClient


def test_agent_basic_query() -> None:
    """Test agent with a basic query about Bedrock features."""
    client = BedrockClient()
    
    query = "What are the main features of Amazon Bedrock?"
    print(f"Query: {query}\n")
    print("Response:")
    
    # Stream response
    for chunk in client.invoke_agent_stream(query, session_id='test-session-1'):
        print(chunk, end='', flush=True)
    
    print("\n")


def test_agent_chunking_query() -> None:
    """Test agent with a query about chunking strategies."""
    client = BedrockClient()
    
    query = "What chunking strategies are available in Bedrock Knowledge Bases?"
    print(f"Query: {query}\n")
    print("Response:")
    
    response = client.invoke_agent(query, session_id='test-session-2')
    print(response)
    print()


def main() -> None:
    """Run all agent tests."""
    print("=" * 70)
    print("Testing Bedrock Agent with RAG")
    print("=" * 70)
    print()
    
    try:
        test_agent_basic_query()
        print("-" * 70)
        test_agent_chunking_query()
        
        print("✅ All tests completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
