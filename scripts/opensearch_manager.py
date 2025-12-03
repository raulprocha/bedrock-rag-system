#!/usr/bin/env python3
"""
OpenSearch Serverless Index Manager

This module provides utilities for creating, checking, and managing
OpenSearch Serverless indexes with FAISS engine for Bedrock Knowledge Base.
"""

import json
from typing import Dict, Any, Optional

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

from .config import config


class OpenSearchManager:
    """Manager for OpenSearch Serverless operations."""
    
    def __init__(
        self,
        collection_endpoint: Optional[str] = None,
        profile_name: Optional[str] = None,
        region_name: Optional[str] = None
    ) -> None:
        """
        Initialize OpenSearch Manager.
        
        Args:
            collection_endpoint: OpenSearch collection endpoint URL.
            profile_name: AWS profile name.
            region_name: AWS region name.
        """
        self.profile_name = profile_name or config.AWS_PROFILE
        self.region_name = region_name or config.AWS_REGION
        self.collection_endpoint = collection_endpoint or config.opensearch_endpoint
        
        # Extract host from endpoint
        self.host = self.collection_endpoint.replace("https://", "").replace("http://", "")
        
        # Initialize AWS session and auth
        session = boto3.Session(profile_name=self.profile_name, region_name=self.region_name)
        credentials = session.get_credentials()
        self.auth = AWSV4SignerAuth(credentials, self.region_name, 'aoss')
        
        # Initialize OpenSearch client
        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': 443}],
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=300
        )
    
    def create_index(
        self,
        index_name: str = "bedrock-knowledge-base-index",
        dimension: int = 1536,
        engine: str = "faiss"
    ) -> Dict[str, Any]:
        """
        Create OpenSearch index with FAISS engine.
        
        Args:
            index_name: Name of the index to create.
            dimension: Vector dimension (1536 for Titan embeddings).
            engine: Vector engine type (faiss or nmslib).
            
        Returns:
            Dict containing the creation response.
            
        Raises:
            Exception: If index creation fails.
        """
        index_body = {
            'settings': {
                'index.knn': True
            },
            'mappings': {
                'properties': {
                    'bedrock-knowledge-base-default-vector': {
                        'type': 'knn_vector',
                        'dimension': dimension,
                        'method': {
                            'engine': engine,
                            'space_type': 'l2',
                            'name': 'hnsw'
                        }
                    },
                    'AMAZON_BEDROCK_TEXT_CHUNK': {'type': 'text'},
                    'AMAZON_BEDROCK_METADATA': {'type': 'text'}
                }
            }
        }
        
        response = self.client.indices.create(index=index_name, body=index_body)
        return response
    
    def delete_index(self, index_name: str = "bedrock-knowledge-base-index") -> Dict[str, Any]:
        """
        Delete OpenSearch index.
        
        Args:
            index_name: Name of the index to delete.
            
        Returns:
            Dict containing the deletion response.
        """
        return self.client.indices.delete(index=index_name)
    
    def get_index_info(self, index_name: str = "bedrock-knowledge-base-index") -> Dict[str, Any]:
        """
        Get index configuration and settings.
        
        Args:
            index_name: Name of the index to query.
            
        Returns:
            Dict containing index information.
        """
        return self.client.indices.get(index=index_name)
    
    def recreate_index(
        self,
        index_name: str = "bedrock-knowledge-base-index",
        dimension: int = 1536
    ) -> Dict[str, Any]:
        """
        Delete and recreate index with FAISS engine.
        
        Args:
            index_name: Name of the index to recreate.
            dimension: Vector dimension.
            
        Returns:
            Dict containing the creation response.
        """
        print(f"Deleting index: {index_name}...")
        self.delete_index(index_name)
        
        print(f"Creating index with FAISS engine...")
        response = self.create_index(index_name, dimension, engine='faiss')
        
        print("Index created successfully!")
        return response


def main() -> None:
    """Main function for CLI usage."""
    import sys
    
    manager = OpenSearchManager()
    
    if len(sys.argv) < 2:
        print("Usage: python opensearch_manager.py [create|delete|check|recreate]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        response = manager.create_index()
        print(json.dumps(response, indent=2))
    elif command == "delete":
        response = manager.delete_index()
        print(json.dumps(response, indent=2))
    elif command == "check":
        response = manager.get_index_info()
        print(json.dumps(response, indent=2))
    elif command == "recreate":
        response = manager.recreate_index()
        print(json.dumps(response, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
