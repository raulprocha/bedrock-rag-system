#!/usr/bin/env python3
"""
Create OpenSearch Serverless index with FAISS engine for Bedrock Knowledge Base.
This index is required before creating the Knowledge Base in Terraform.
"""
import boto3
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

index_body = {
    'settings': {
        'index.knn': True
    },
    'mappings': {
        'properties': {
            'bedrock-knowledge-base-default-vector': {
                'type': 'knn_vector',
                'dimension': 1536,
                'method': {
                    'engine': 'faiss',
                    'space_type': 'l2',
                    'name': 'hnsw'
                }
            },
            'AMAZON_BEDROCK_TEXT_CHUNK': {'type': 'text'},
            'AMAZON_BEDROCK_METADATA': {'type': 'text'}
        }
    }
}

response = client.indices.create(index='bedrock-knowledge-base-index', body=index_body)
print(response)
