#!/usr/bin/env python3
"""
Test Bedrock Agent with RAG capabilities.
The agent automatically retrieves relevant context from the Knowledge Base.
"""
import boto3

session = boto3.Session(profile_name='CIANDT-Contributor-253223147282', region_name='us-east-1')
client = session.client('bedrock-agent-runtime')

response = client.invoke_agent(
    agentId='UXKVAWIHD9',
    agentAliasId='WSQUCAPCEV',
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
