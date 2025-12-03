# Amazon Bedrock RAG System with Knowledge Base & Agent

Production-ready RAG (Retrieval Augmented Generation) system demonstrating advanced AWS Bedrock capabilities including Knowledge Bases, Agents, and Model Context Protocol (MCP) integration.

## 🎯 Project Overview

This project showcases a complete implementation of a RAG system using AWS Bedrock services, featuring:
- **Hierarchical chunking** for optimal context retrieval
- **FAISS-powered vector search** via OpenSearch Serverless
- **Automatic RAG** through Bedrock Agents
- **MCP integration** for seamless AI assistant workflows
- **Infrastructure as Code** with Terraform

## 🏗️ Architecture

```
┌─────────────┐
│  S3 Bucket  │ ← Document Storage
└──────┬──────┘
       │
       ↓
┌──────────────────────────┐
│ Bedrock Knowledge Base   │ ← Hierarchical Chunking
│ (Titan Embeddings)       │   Parent: 1500 tokens
└──────┬───────────────────┘   Child: 300 tokens
       │                        Overlap: 60 tokens
       ↓
┌──────────────────────────┐
│ OpenSearch Serverless    │ ← FAISS Vector Search
│ (1536-dim vectors)       │   L2 distance + HNSW
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│   Bedrock Agent          │ ← Automatic RAG
│   (Claude/Nova)          │   Context-aware responses
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│   MCP Server (Local)     │ ← Model Context Protocol
│   → Kiro CLI             │   Tool integration
└──────────────────────────┘
```

## ✨ Key Features

### 1. Hierarchical Chunking Strategy
- **Parent chunks (1500 tokens)**: Provide broad context for comprehensive answers
- **Child chunks (300 tokens)**: Enable precise semantic search
- **60-token overlap**: Maintains continuity across chunk boundaries
- **Benefit**: Searches in child chunks for precision, returns parent chunks for context

### 2. FAISS Vector Search
- **Engine**: FAISS (Facebook AI Similarity Search)
- **Dimensions**: 1536 (Amazon Titan Embeddings)
- **Algorithm**: HNSW (Hierarchical Navigable Small World)
- **Distance metric**: L2 (Euclidean distance)
- **Performance**: Sub-millisecond similarity search at scale

### 3. Automatic RAG with Bedrock Agent
- Agent automatically determines when to query the Knowledge Base
- Seamless integration between retrieval and generation
- Context-aware responses with source attribution
- Session management for multi-turn conversations

### 4. MCP Integration
- Exposes Bedrock capabilities as MCP tools
- Compatible with Kiro CLI and other MCP clients
- Two main tools:
  - `invoke_bedrock_agent`: Full RAG pipeline
  - `retrieve_from_kb`: Direct KB queries

## 🚀 Quick Start

### Prerequisites

```bash
# Required tools
- AWS CLI configured
- Terraform >= 1.0
- Python 3.8+

# Required AWS permissions
- bedrock:*
- aoss:* (OpenSearch Serverless)
- s3:*
- iam:PassRole
```

### 1. Clone and Configure

```bash
git clone <repository-url>
cd kb_agent-core

# Copy and update configuration files
cp config.py.example config.py
cp terraform.tfvars.example terraform.tfvars

# Edit with your AWS account details
vim config.py
vim terraform.tfvars
```

### 2. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Review plan
terraform plan

# Deploy
terraform apply -auto-approve
```

### 3. Create OpenSearch Index

The Knowledge Base requires a FAISS-enabled index:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create index (update config.py first)
python3 create_index.py
```

### 4. Upload Documents

```bash
# Get bucket name from Terraform
BUCKET=$(terraform output -raw s3_bucket_name)

# Upload your documents
aws s3 cp your-document.pdf s3://$BUCKET/
```

### 5. Sync Knowledge Base

```bash
# Get resource IDs
KB_ID=$(terraform output -raw knowledge_base_id)
DS_ID=$(terraform output -raw data_source_id)

# Start ingestion job
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id $KB_ID \
  --data-source-id $DS_ID \
  --region us-east-1

# Monitor progress
aws bedrock-agent get-ingestion-job \
  --knowledge-base-id $KB_ID \
  --data-source-id $DS_ID \
  --ingestion-job-id <JOB_ID>
```

### 6. Test the System

```bash
# Test agent with RAG
python3 test_agent.py

# Test direct KB retrieval
python3 test_kb.py

# Interactive CLI
python3 ask_agent.py "What are the main features of Amazon Bedrock?"
```

## 📁 Project Structure

```
.
├── README.md                      # This file
├── LICENSE                        # MIT License
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── config.py.example              # Configuration template
├── terraform.tfvars.example       # Terraform variables template
│
├── main.tf                        # Terraform main config
├── variables.tf                   # Terraform variables
├── outputs.tf                     # Terraform outputs
├── s3.tf                          # S3 bucket for documents
├── opensearch.tf                  # OpenSearch Serverless
├── knowledge_base.tf              # Knowledge Base + Data Source
├── agent.tf                       # Bedrock Agent
│
├── create_index.py                # Create FAISS index
├── recreate_index.py              # Recreate index (if needed)
├── check_index.py                 # Verify index configuration
│
├── test_agent.py                  # Test agent with RAG
├── test_kb.py                     # Test KB retrieval
├── ask_agent.py                   # Interactive CLI
│
├── mcp_server.py                  # MCP server implementation
├── mcp_config.json                # MCP configuration
└── test_mcp.sh                    # MCP testing script
```

## 🔧 Configuration

### Chunking Strategy

Modify `knowledge_base.tf` to adjust chunking parameters:

```hcl
vector_ingestion_configuration {
  chunking_configuration {
    chunking_strategy = "HIERARCHICAL"
    hierarchical_chunking_configuration {
      level_configuration {
        max_tokens = 1500  # Parent chunk size
      }
      level_configuration {
        max_tokens = 300   # Child chunk size
      }
      overlap_tokens = 60  # Overlap between chunks
    }
  }
}
```

### Embedding Model

Change embedding model in `variables.tf`:

```hcl
variable "embedding_model_arn" {
  default = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
  # Or use: amazon.titan-embed-text-v2
  # Or use: cohere.embed-english-v3
}
```

## 🧪 Testing

### Unit Tests

```bash
# Test agent invocation
python3 test_agent.py

# Test KB retrieval
python3 test_kb.py

# Test MCP server
./test_mcp.sh
```

### Integration Tests

```bash
# Test full RAG pipeline
python3 ask_agent.py "Explain hierarchical chunking in Bedrock"

# Test with different queries
python3 ask_agent.py "What is FAISS?"
python3 ask_agent.py "How does RAG work?"
```

## 📊 Performance Metrics

Based on testing with a 49.4 MB PDF (Amazon Bedrock User Guide):

| Metric | Value |
|--------|-------|
| Indexing time | ~4-5 minutes |
| Query latency | ~2-3 seconds |
| Retrieval accuracy | High (hierarchical chunking) |
| Context window | Up to 1500 tokens per result |

## 💰 Cost Estimation

| Service | Cost | Notes |
|---------|------|-------|
| OpenSearch Serverless | ~$175/month | 2 OCUs (search + indexing) |
| Bedrock Agent | ~$0.002/1K tokens | Pay-per-use |
| S3 Storage | ~$0.023/GB/month | Minimal for documents |
| Titan Embeddings | ~$0.0001/1K tokens | One-time per document |

**Total estimated cost**: ~$180-200/month for continuous operation

**Cost optimization tips**:
- Delete OpenSearch collection when not in use
- Use S3 Intelligent-Tiering for documents
- Batch document processing to minimize embedding costs

## 🔒 Security Best Practices

- ✅ IAM roles with least privilege principle
- ✅ S3 bucket versioning enabled
- ✅ OpenSearch Serverless encryption at rest
- ✅ VPC endpoints for private connectivity (optional)
- ✅ CloudWatch logging for audit trails
- ⚠️ Never commit credentials to Git
- ⚠️ Use AWS Secrets Manager for sensitive data

## 🐛 Troubleshooting

### Issue: 403 Forbidden when creating Knowledge Base

**Solution**: Ensure IAM role has required permissions:
```json
{
  "Effect": "Allow",
  "Action": [
    "aoss:APIAccessAll",
    "s3:ListBucket",
    "s3:GetObject",
    "bedrock:InvokeModel"
  ],
  "Resource": "*"
}
```

### Issue: OpenSearch index engine error

**Error**: "The OpenSearch Serverless engine type associated with your vector index is invalid"

**Solution**: Index must use FAISS engine. Run:
```bash
python3 recreate_index.py
```

### Issue: Agent doesn't return document information

**Checklist**:
1. Verify ingestion job completed: `aws bedrock-agent list-ingestion-jobs`
2. Check documents in S3: `aws s3 ls s3://<bucket>/`
3. Test direct retrieval: `python3 test_kb.py`
4. Verify agent-KB association in AWS Console

## 🚀 Advanced Features

### Multimodal Content Support

Bedrock Knowledge Bases support images, audio, and video:

**Option 1: Nova Multimodal Embeddings**
- Direct embedding of multimedia files
- Visual similarity search
- Configure chunk duration (1-30 seconds) for audio/video

**Option 2: Bedrock Data Automation**
- Converts multimedia to text first
- Audio transcription
- Video scene descriptions
- Image OCR

### Custom Metadata Filtering

Add metadata to documents for filtered retrieval:

```python
response = client.retrieve(
    knowledgeBaseId='KB_ID',
    retrievalQuery={'text': 'query'},
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'filter': {
                'equals': {
                    'key': 'category',
                    'value': 'technical'
                }
            }
        }
    }
)
```

## 📚 Learning Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Knowledge Bases for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Agents for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)

## 🤝 Contributing

Contributions are welcome! This project demonstrates AWS Bedrock capabilities and can be extended for various use cases.

**Ideas for contributions**:
- Add support for more embedding models
- Implement semantic chunking strategy
- Add monitoring dashboards
- Create CI/CD pipeline
- Add more test cases

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 👤 Author

**Raul Rocha**

This project was built to demonstrate production-ready RAG systems using AWS Bedrock services, showcasing:
- Cloud architecture design
- Infrastructure as Code (Terraform)
- AI/ML integration
- API development (MCP)
- DevOps best practices

## 🙏 Acknowledgments

- AWS Bedrock team for excellent documentation
- OpenSearch community for FAISS integration
- Model Context Protocol contributors

---

**Note**: This is a demonstration project. For production use, additional considerations for scalability, monitoring, and security hardening are recommended.
