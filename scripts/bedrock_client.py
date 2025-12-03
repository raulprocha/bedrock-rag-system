#!/usr/bin/env python3
"""
Bedrock Agent and Knowledge Base Client

This module provides a high-level interface for interacting with
AWS Bedrock Agents and Knowledge Bases.
"""

from typing import Dict, List, Any, Optional, Iterator

import boto3

from .config import config


class BedrockClient:
    """Client for AWS Bedrock Agent and Knowledge Base operations."""
    
    def __init__(
        self,
        profile_name: Optional[str] = None,
        region_name: Optional[str] = None
    ) -> None:
        """
        Initialize Bedrock client.
        
        Args:
            profile_name: AWS profile name.
            region_name: AWS region name.
        """
        self.profile_name = profile_name or config.AWS_PROFILE
        self.region_name = region_name or config.AWS_REGION
        
        session = boto3.Session(
            profile_name=self.profile_name,
            region_name=self.region_name
        )
        
        self.agent_runtime = session.client('bedrock-agent-runtime')
        self.agent_client = session.client('bedrock-agent')
    
    def invoke_agent(
        self,
        query: str,
        agent_id: Optional[str] = None,
        agent_alias_id: Optional[str] = None,
        session_id: str = "default-session"
    ) -> str:
        """
        Invoke Bedrock Agent with a query.
        
        Args:
            query: User query text.
            agent_id: Agent ID (uses config if not provided).
            agent_alias_id: Agent alias ID (uses config if not provided).
            session_id: Session ID for conversation continuity.
            
        Returns:
            Complete response text from the agent.
        """
        agent_id = agent_id or config.AGENT_ID
        agent_alias_id = agent_alias_id or config.AGENT_ALIAS_ID
        
        response = self.agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=query
        )
        
        # Collect response chunks
        result = []
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    result.append(chunk['bytes'].decode('utf-8'))
        
        return ''.join(result)
    
    def invoke_agent_stream(
        self,
        query: str,
        agent_id: Optional[str] = None,
        agent_alias_id: Optional[str] = None,
        session_id: str = "default-session"
    ) -> Iterator[str]:
        """
        Invoke Bedrock Agent with streaming response.
        
        Args:
            query: User query text.
            agent_id: Agent ID (uses config if not provided).
            agent_alias_id: Agent alias ID (uses config if not provided).
            session_id: Session ID for conversation continuity.
            
        Yields:
            Response chunks as they arrive.
        """
        agent_id = agent_id or config.AGENT_ID
        agent_alias_id = agent_alias_id or config.AGENT_ALIAS_ID
        
        response = self.agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=query
        )
        
        for event in response['completion']:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    yield chunk['bytes'].decode('utf-8')
    
    def retrieve_from_kb(
        self,
        query: str,
        kb_id: Optional[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents from Knowledge Base.
        
        Args:
            query: Search query text.
            kb_id: Knowledge Base ID (uses config if not provided).
            max_results: Maximum number of results to return.
            
        Returns:
            List of retrieval results with scores and content.
        """
        kb_id = kb_id or config.KNOWLEDGE_BASE_ID
        
        response = self.agent_runtime.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': max_results
                }
            }
        )
        
        return response['retrievalResults']
    
    def start_ingestion_job(
        self,
        kb_id: Optional[str] = None,
        data_source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Start Knowledge Base ingestion job.
        
        Args:
            kb_id: Knowledge Base ID (uses config if not provided).
            data_source_id: Data source ID (uses config if not provided).
            
        Returns:
            Ingestion job details.
        """
        kb_id = kb_id or config.KNOWLEDGE_BASE_ID
        data_source_id = data_source_id or config.DATA_SOURCE_ID
        
        response = self.agent_client.start_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=data_source_id
        )
        
        return response['ingestionJob']
    
    def get_ingestion_job(
        self,
        job_id: str,
        kb_id: Optional[str] = None,
        data_source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get ingestion job status.
        
        Args:
            job_id: Ingestion job ID.
            kb_id: Knowledge Base ID (uses config if not provided).
            data_source_id: Data source ID (uses config if not provided).
            
        Returns:
            Ingestion job details and statistics.
        """
        kb_id = kb_id or config.KNOWLEDGE_BASE_ID
        data_source_id = data_source_id or config.DATA_SOURCE_ID
        
        response = self.agent_client.get_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=data_source_id,
            ingestionJobId=job_id
        )
        
        return response['ingestionJob']


def main() -> None:
    """Main function for CLI testing."""
    import sys
    
    client = BedrockClient()
    
    if len(sys.argv) < 2:
        print("Usage: python bedrock_client.py [agent|retrieve] <query>")
        sys.exit(1)
    
    command = sys.argv[1]
    query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "What is Amazon Bedrock?"
    
    if command == "agent":
        print("Invoking agent...")
        response = client.invoke_agent(query)
        print(f"\nResponse:\n{response}")
    elif command == "retrieve":
        print("Retrieving from KB...")
        results = client.retrieve_from_kb(query, max_results=3)
        print(f"\nTop {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['score']:.4f}")
            print(f"   Text: {result['content']['text'][:200]}...")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
