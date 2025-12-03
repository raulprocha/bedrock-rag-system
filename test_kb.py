#!/usr/bin/env python3
"""
Test direct retrieval from Bedrock Knowledge Base.
This bypasses the agent and queries the KB directly.
"""
import boto3

session = boto3.Session(profile_name='CIANDT-Contributor-253223147282', region_name='us-east-1')
client = session.client('bedrock-agent-runtime')

response = client.retrieve(
    knowledgeBaseId='Z9SKJS11DX',
    retrievalQuery={'text': 'What is Retrieval Augmented Generation?'}
)

print("Top 3 results:\n")
for i, result in enumerate(response['retrievalResults'][:3], 1):
    print(f"{i}. Score: {result['score']:.4f}")
    print(f"   Text: {result['content']['text'][:200]}...")
    print()
