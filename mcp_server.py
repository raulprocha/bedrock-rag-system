#!/usr/bin/env python3
import json
import sys
import boto3
import os
from typing import Any

class BedrockAgentMCP:
    def __init__(self):
        session = boto3.Session(profile_name='CIANDT-Contributor-253223147282')
        self.bedrock = session.client('bedrock-agent-runtime', region_name='us-east-1')
        self.agent_id = None
        self.agent_alias_id = None
    
    def set_agent(self, agent_id: str, agent_alias_id: str):
        self.agent_id = agent_id
        self.agent_alias_id = agent_alias_id
    
    def invoke_agent(self, query: str, session_id: str = "default") -> str:
        if not self.agent_id or not self.agent_alias_id:
            return "Error: Agent not configured"
        
        response = self.bedrock.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=session_id,
            inputText=query
        )
        
        result = ""
        for event in response['completion']:
            if 'chunk' in event:
                result += event['chunk']['bytes'].decode('utf-8')
        
        return result
    
    def retrieve_kb(self, query: str, kb_id: str) -> list:
        response = self.bedrock.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': query}
        )
        
        results = []
        for item in response.get('retrievalResults', []):
            results.append({
                'content': item['content']['text'],
                'score': item.get('score', 0)
            })
        return results

def handle_request(request: dict) -> dict:
    method = request.get('method')
    params = request.get('params', {})
    
    mcp = BedrockAgentMCP()
    
    if method == 'tools/list':
        return {
            'tools': [
                {
                    'name': 'invoke_bedrock_agent',
                    'description': 'Invoke Bedrock Agent with a query',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'agent_id': {'type': 'string'},
                            'agent_alias_id': {'type': 'string'},
                            'query': {'type': 'string'},
                            'session_id': {'type': 'string', 'default': 'default'}
                        },
                        'required': ['agent_id', 'agent_alias_id', 'query']
                    }
                },
                {
                    'name': 'retrieve_from_kb',
                    'description': 'Retrieve documents from Knowledge Base',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'kb_id': {'type': 'string'},
                            'query': {'type': 'string'}
                        },
                        'required': ['kb_id', 'query']
                    }
                }
            ]
        }
    
    elif method == 'tools/call':
        tool_name = params.get('name')
        args = params.get('arguments', {})
        
        if tool_name == 'invoke_bedrock_agent':
            mcp.set_agent(args['agent_id'], args['agent_alias_id'])
            result = mcp.invoke_agent(args['query'], args.get('session_id', 'default'))
            return {'content': [{'type': 'text', 'text': result}]}
        
        elif tool_name == 'retrieve_from_kb':
            results = mcp.retrieve_kb(args['query'], args['kb_id'])
            return {'content': [{'type': 'text', 'text': json.dumps(results, indent=2)}]}
    
    return {'error': 'Unknown method'}

def main():
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({'error': str(e)}))
            sys.stdout.flush()

if __name__ == '__main__':
    main()
