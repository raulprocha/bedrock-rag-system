#!/usr/bin/env python3
"""
Interactive CLI for Bedrock Agent.

This script provides an interactive command-line interface
for querying the Bedrock Agent with RAG capabilities.
"""

import sys
import argparse
from typing import Optional

from scripts.bedrock_client import BedrockClient
from scripts.config import config


def interactive_mode(client: BedrockClient) -> None:
    """
    Run interactive mode for continuous queries.
    
    Args:
        client: Initialized BedrockClient instance.
    """
    print("=" * 70)
    print("Bedrock Agent Interactive CLI")
    print("=" * 70)
    print("Type 'exit' or 'quit' to end the session")
    print("Type 'help' for available commands")
    print()
    
    session_id = "interactive-session"
    
    while True:
        try:
            query = input("\n🤖 Query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if query.lower() == 'help':
                print("\nAvailable commands:")
                print("  - Type any question to query the agent")
                print("  - 'exit', 'quit', 'q' - Exit the CLI")
                print("  - 'help' - Show this help message")
                continue
            
            print("\n💭 Response:")
            for chunk in client.invoke_agent_stream(query, session_id=session_id):
                print(chunk, end='', flush=True)
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def single_query_mode(client: BedrockClient, query: str) -> None:
    """
    Execute a single query and exit.
    
    Args:
        client: Initialized BedrockClient instance.
        query: Query text.
    """
    print(f"Query: {query}\n")
    print("Response:")
    
    for chunk in client.invoke_agent_stream(query):
        print(chunk, end='', flush=True)
    
    print("\n")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Interactive CLI for AWS Bedrock Agent with RAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py
  
  # Single query
  python cli.py "What are the main features of Amazon Bedrock?"
  
  # Specify custom agent
  python cli.py --agent-id AGENT_ID --alias-id ALIAS_ID "Your question"
        """
    )
    
    parser.add_argument(
        'query',
        nargs='*',
        help='Query text (if not provided, enters interactive mode)'
    )
    parser.add_argument(
        '--agent-id',
        help='Bedrock Agent ID (overrides config)'
    )
    parser.add_argument(
        '--alias-id',
        help='Bedrock Agent Alias ID (overrides config)'
    )
    parser.add_argument(
        '--profile',
        help='AWS profile name (overrides config)'
    )
    parser.add_argument(
        '--region',
        help='AWS region (overrides config)'
    )
    
    args = parser.parse_args()
    
    # Initialize client
    client = BedrockClient(
        profile_name=args.profile,
        region_name=args.region
    )
    
    # Override config if provided
    if args.agent_id:
        config.AGENT_ID = args.agent_id
    if args.alias_id:
        config.AGENT_ALIAS_ID = args.alias_id
    
    # Validate configuration
    if not config.validate():
        print("❌ Error: Missing required configuration.")
        print("Please update config.py with your AWS resources.")
        sys.exit(1)
    
    # Run appropriate mode
    if args.query:
        query = ' '.join(args.query)
        single_query_mode(client, query)
    else:
        interactive_mode(client)


if __name__ == "__main__":
    main()
