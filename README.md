# Amazon Bedrock RAG System with Knowledge Base & Agent

Production-ready RAG (Retrieval Augmented Generation) system using Amazon Bedrock Knowledge Base, Bedrock Agent, and MCP (Model Context Protocol) for integration with Kiro CLI.

## Architecture

```
S3 Bucket → Bedrock Knowledge Base → OpenSearch Serverless (FAISS)
                ↓
         Bedrock Agent (Automatic RAG)
                ↓
         MCP Server (Local) → Kiro CLI
```

## Features

- ✅ **Hierarchical Chunking**: Parent chunks (1500 tokens) + Child chunks (300 tokens) with 60 token overlap
- ✅ **FAISS Vector Search**: High-performance similarity search with OpenSearch Serverless
- ✅ **Amazon Titan Embeddings**: 1536-dimensional vectors for semantic search
- ✅ **Automatic RAG**: Bedrock Agent automatically retrieves relevant context
- ✅ **MCP Integration**: Seamless integration with Kiro CLI via Model Context Protocol
- ✅ **Infrastructure as Code**: Complete Terraform deployment

## Current Status

- ✅ S3 Bucket created
- ✅ OpenSearch Serverless collection (FAISS engine)
- ✅ Bedrock Agent deployed (ID: UXKVAWIHD9)
- ✅ Knowledge Base active (ID: Z9SKJS11DX)
- ✅ Hierarchical chunking configured
- ✅ MCP Server operational
- ✅ Document indexed (bedrock-ug.pdf)

## Prerequisites

- AWS CLI configured with appropriate profile
- Terraform >= 1.0
- Python 3.8+
- IAM permissions for Bedrock, OpenSearch Serverless, and S3

## Quick Start

### 1. Deploy Infrastructure

```bash
terraform init
terraform apply -auto-approve
```

### 2. Upload Documents

```bash
aws s3 cp your-document.pdf s3://simple-knowledge-base-data-253223147282/ \
  --profile CIANDT-Contributor-253223147282
```

### 3. Sync Knowledge Base

```bash
KB_ID=$(terraform output -raw knowledge_base_id)
DS_ID=$(terraform output -raw data_source_id)

aws bedrock-agent start-ingestion-job \
  --knowledge-base-id $KB_ID \
  --data-source-id $DS_ID \
  --region us-east-1 \
  --profile CIANDT-Contributor-253223147282
```

### 4. Test the System

```bash
python3 ask_agent.py "What are the main features of Amazon Bedrock?"
```

## Chunking Strategy

### Hierarchical Chunking Configuration

- **Parent Chunks**: 1500 tokens (broad context)
- **Child Chunks**: 300 tokens (precise retrieval)
- **Overlap**: 60 tokens (continuity between chunks)

**How it works:**
1. System searches in child chunks for precision
2. Returns parent chunks for comprehensive context
3. Optimal balance between accuracy and context

### Benefits

- More complete answers with broader context
- Better handling of complex queries
- Improved semantic understanding
- Reduced information fragmentation

## MCP Integration

### Available Tools

#### invoke_bedrock_agent
Interact with the Agent (automatic RAG)

**Parameters:**
- `agent_id`: Agent ID
- `agent_alias_id`: Alias ID
- `query`: Your question
- `session_id`: (optional) Session ID for conversation continuity

#### retrieve_from_kb
Direct search in Knowledge Base

**Parameters:**
- `kb_id`: Knowledge Base ID
- `query`: Search text

### Setup MCP

```bash
mkdir -p ~/.config/kiro-cli
cp mcp_config.json ~/.config/kiro-cli/mcp.json
```

### Usage in Kiro CLI

```
"Ask the agent about [your topic]"
"Search the knowledge base for information about X"
```

## Testing

### Test Agent with RAG

```bash
python3 test_agent.py
```

### Test Direct KB Retrieval

```bash
python3 test_kb.py
```

### Manual MCP Test

```bash
# List available tools
echo '{"method": "tools/list"}' | python3 mcp_server.py

# Invoke agent
echo '{"method": "tools/call", "params": {"name": "invoke_bedrock_agent", "arguments": {"agent_id": "UXKVAWIHD9", "agent_alias_id": "WSQUCAPCEV", "query": "Hello"}}}' | python3 mcp_server.py
```

## Resources Created

| Resource | Name/ID | Description |
|----------|---------|-------------|
| S3 Bucket | `simple-knowledge-base-data-253223147282` | Document storage |
| OpenSearch Collection | `simple-knowledge-base` | Vector database (FAISS) |
| Knowledge Base | `Z9SKJS11DX` | Bedrock KB with hierarchical chunking |
| Data Source | `3DLV3IC5QF` | S3 data source connector |
| Bedrock Agent | `UXKVAWIHD9` | RAG agent |
| Agent Alias | `WSQUCAPCEV` | Production alias |

## Terraform Outputs

```bash
terraform output knowledge_base_id      # Knowledge Base ID
terraform output agent_id               # Agent ID
terraform output agent_alias_id         # Agent Alias ID
terraform output s3_bucket_name         # S3 Bucket name
terraform output opensearch_collection_endpoint  # OpenSearch endpoint
```

## Cost Estimation

| Service | Estimated Cost |
|---------|---------------|
| OpenSearch Serverless | ~$0.24/hour (~$175/month) |
| Bedrock Agent | Pay-per-use (~$0.002/1K tokens) |
| S3 Storage | ~$0.023/GB/month |
| Titan Embeddings | ~$0.0001/1K tokens |

**Note**: Costs vary based on usage. Use AWS Cost Explorer for accurate tracking.

## Troubleshooting

### 403 Forbidden when creating KB
- Missing IAM permissions
- Ensure role has `aoss:APIAccessAll` and `s3:ListBucket` permissions

### Agent doesn't return document information
- Verify KB sync completed: `aws bedrock-agent list-ingestion-jobs`
- Check documents exist in S3: `aws s3 ls s3://simple-knowledge-base-data-253223147282/`

### MCP not working
- Install dependencies: `pip install boto3 opensearch-py requests-aws4auth`
- Verify AWS credentials: `aws sts get-caller-identity --profile CIANDT-Contributor-253223147282`

### OpenSearch index engine error
- Index must use FAISS engine (not nmslib)
- Use `recreate_index.py` to recreate with correct engine

## Advanced Configuration

### Custom Chunking Strategy

Edit `knowledge_base.tf`:

```hcl
vector_ingestion_configuration {
  chunking_configuration {
    chunking_strategy = "HIERARCHICAL"
    hierarchical_chunking_configuration {
      level_configuration {
        max_tokens = 2000  # Adjust parent chunk size
      }
      level_configuration {
        max_tokens = 400   # Adjust child chunk size
      }
      overlap_tokens = 80  # Adjust overlap
    }
  }
}
```

### Multimodal Content Support

For images, audio, and video:
- Use **Nova Multimodal Embeddings** for direct embedding
- Or use **Bedrock Data Automation** for text conversion
- Configure chunk duration (1-30 seconds) for audio/video

## Security Best Practices

- ✅ Use IAM roles with least privilege
- ✅ Enable S3 bucket versioning
- ✅ Use OpenSearch Serverless encryption
- ✅ Rotate AWS credentials regularly
- ✅ Monitor with CloudWatch
- ⚠️ Never commit AWS credentials to Git

## Project Structure

```
.
├── main.tf                 # Terraform main configuration
├── variables.tf            # Terraform variables
├── outputs.tf              # Terraform outputs
├── s3.tf                   # S3 bucket configuration
├── opensearch.tf           # OpenSearch Serverless setup
├── knowledge_base.tf       # Knowledge Base & Data Source
├── agent.tf                # Bedrock Agent configuration
├── mcp_server.py          # MCP server implementation
├── mcp_config.json        # MCP configuration
├── test_agent.py          # Agent testing script
├── test_kb.py             # KB retrieval testing script
├── ask_agent.py           # Interactive agent CLI
├── create_index.py        # OpenSearch index creation
├── recreate_index.py      # Index recreation with FAISS
└── README.md              # This file
```

## Contributing

This is a demonstration project showcasing AWS Bedrock capabilities. Feel free to fork and adapt for your use cases.

## License

MIT License - See LICENSE file for details

## Author

Built as a demonstration of production-ready RAG systems using AWS Bedrock services.

## References

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
