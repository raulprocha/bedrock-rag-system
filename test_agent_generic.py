#!/usr/bin/env python3
"""
Test Bedrock Agent with RAG capabilities.
The agent automatically retrieves relevant context from the Knowledge Base.

Usage: Update config.py with your AWS resources before running.
"""
import boto3
try:
    from config import AWS_PROFILE, AWS_REGION, AGENT_ID, AGENT_ALIAS_ID
except ImportError:
    print("Error: config.py not found. Copy config.py.example to config.py and update with your values.")
    exit(1)

session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
client = session.client('bedrock-agent-runtime')

response = client.invoke_agent(
    agentId=AGENT_ID,
    agentAliasId=AGENT_ALIAS_ID,
    sessionId='test-session-1',
    inputText='What are the main features of Amazon Bedrock?'
)

print("Response:")
for event in response['completion']:
    if 'chunk' in event:
        chunk = event['chunk']
        if 'bytes' in chunk:
            print(chunk['bytes'].decode('utf-8'), end='', flush=True)

print("\n")
