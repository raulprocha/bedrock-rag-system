#!/usr/bin/env python3
"""
Check OpenSearch Serverless index configuration.
Useful for verifying the engine type (FAISS vs nmslib) and other settings.
"""
import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

session = boto3.Session(profile_name='CIANDT-Contributor-253223147282', region_name='us-east-1')
credentials = session.get_credentials()
auth = AWSV4SignerAuth(credentials, 'us-east-1', 'aoss')

client = OpenSearch(
    hosts=[{'host': '9a8nfylg5l5w7rn4pkx3.us-east-1.aoss.amazonaws.com', 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300
)

response = client.indices.get(index='bedrock-knowledge-base-index')
print(json.dumps(response, indent=2))
