#!/usr/bin/env python3
"""
Interactive CLI to ask questions to the Bedrock Agent.
Usage: python3 ask_agent.py "Your question here"
"""
import boto3
import sys

session = boto3.Session(profile_name='CIANDT-Contributor-253223147282', region_name='us-east-1')
client = session.client('bedrock-agent-runtime')

query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'What chunking strategies are available in Bedrock Knowledge Bases?'

response = client.invoke_agent(
    agentId='UXKVAWIHD9',
    agentAliasId='WSQUCAPCEV',
    sessionId='interactive-session',
    inputText=query
)

for event in response['completion']:
    if 'chunk' in event:
        chunk = event['chunk']
        if 'bytes' in chunk:
            print(chunk['bytes'].decode('utf-8'), end='', flush=True)

print()
