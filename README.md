# Amazon Bedrock RAG System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Terraform](https://img.shields.io/badge/terraform-1.0+-purple.svg)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready Retrieval Augmented Generation (RAG) system built with AWS Bedrock, featuring hierarchical chunking, FAISS vector search, and Model Context Protocol (MCP) integration.

## 🎯 Overview

This project demonstrates enterprise-grade implementation of a RAG system using AWS Bedrock services:

- **Hierarchical Chunking**: Parent chunks (1500 tokens) + Child chunks (300 tokens) with 60-token overlap
- **FAISS Vector Search**: High-performance similarity search via OpenSearch Serverless
- **Amazon Titan Embeddings**: 1536-dimensional semantic vectors
- **Automatic RAG**: Bedrock Agent with intelligent context retrieval
- **MCP Integration**: Seamless AI assistant workflows
- **Infrastructure as Code**: Complete Terraform deployment

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

## 📁 Project Structure

```
.
├── terraform/              # Infrastructure as Code
│   ├── main.tf            # Main configuration
│   ├── variables.tf       # Input variables
│   ├── outputs.tf         # Output values
│   ├── s3.tf              # S3 bucket for documents
│   ├── opensearch.tf      # OpenSearch Serverless
│   ├── knowledge_base.tf  # Knowledge Base + Data Source
│   └── agent.tf           # Bedrock Agent
│
├── scripts/               # Python utilities
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── opensearch_manager.py  # OpenSearch operations
│   └── bedrock_client.py  # Bedrock API client
│
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_agent.py      # Agent testing
│   └── test_kb.py         # KB retrieval testing
│
├── docs/                  # Additional documentation
│
├── cli.py                 # Interactive CLI
├── mcp_server.py          # MCP server implementation
├── requirements.txt       # Python dependencies
├── config.py.example      # Configuration template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Python 3.8+
- Required AWS permissions (Bedrock, OpenSearch Serverless, S3, IAM)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/raulprocha/bedrock-rag-system.git
   cd bedrock-rag-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS resources**
   ```bash
   cp config.py.example scripts/config.py
   # Edit scripts/config.py with your AWS details
   ```

4. **Deploy infrastructure**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

5. **Create OpenSearch index**
   ```bash
   python -m scripts.opensearch_manager create
   ```

6. **Upload documents**
   ```bash
   aws s3 cp your-document.pdf s3://YOUR_BUCKET_NAME/
   ```

7. **Sync Knowledge Base**
   ```bash
   python -m scripts.bedrock_client sync
   ```

## 💻 Usage

### Interactive CLI

```bash
# Interactive mode
python cli.py

# Single query
python cli.py "What are the main features of Amazon Bedrock?"
```

### Python API

```python
from scripts.bedrock_client import BedrockClient

# Initialize client
client = BedrockClient()

# Query agent
response = client.invoke_agent("Your question here")
print(response)

# Direct KB retrieval
results = client.retrieve_from_kb("Search query", max_results=5)
for result in results:
    print(f"Score: {result['score']}")
    print(f"Text: {result['content']['text']}")
```

### Testing

```bash
# Test agent
python tests/test_agent.py

# Test KB retrieval
python tests/test_kb.py
```

### OpenSearch Management

```bash
# Create index
python -m scripts.opensearch_manager create

# Check index configuration
python -m scripts.opensearch_manager check

# Recreate index with FAISS
python -m scripts.opensearch_manager recreate
```

## 🔧 Configuration

### Chunking Strategy

Edit `terraform/knowledge_base.tf`:

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

Edit `terraform/variables.tf`:

```hcl
variable "embedding_model_arn" {
  default = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
}
```

## 📊 Performance

Based on testing with 49.4 MB PDF (Amazon Bedrock User Guide):

| Metric | Value |
|--------|-------|
| Indexing time | ~4-5 minutes |
| Query latency | ~2-3 seconds |
| Retrieval accuracy | High (hierarchical chunking) |
| Context window | Up to 1500 tokens per result |

## 💰 Cost Estimation

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| OpenSearch Serverless | ~$175 | 2 OCUs (search + indexing) |
| Bedrock Agent | Pay-per-use | ~$0.002/1K tokens |
| S3 Storage | ~$0.023/GB | Minimal for documents |
| Titan Embeddings | One-time | ~$0.0001/1K tokens |

**Total**: ~$180-200/month for continuous operation

## 🔒 Security

- ✅ IAM roles with least privilege
- ✅ S3 bucket versioning enabled
- ✅ OpenSearch Serverless encryption at rest
- ✅ No credentials in repository
- ✅ CloudWatch logging for audit trails

## 🐛 Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues and solutions.

## 📚 Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Raul Rocha**
- Email: raulrocha.rpr@gmail.com
- GitHub: [@raulprocha](https://github.com/raulprocha)

## 🙏 Acknowledgments

- AWS Bedrock team for excellent documentation
- OpenSearch community for FAISS integration
- Model Context Protocol contributors

---

**Built with ❤️ to demonstrate production-ready RAG systems on AWS**
