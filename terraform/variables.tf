variable "region" {
  default = "us-east-1"
}

variable "kb_name" {
  default = "simple-knowledge-base"
}

variable "embedding_model_arn" {
  default = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
}

variable "kb_role_arn" {
  default = "arn:aws:iam::253223147282:role/AmazonBedRockAgentCoreRole-PPD"
}

variable "agent_name" {
  default = "rag-agent"
}

variable "model_id" {
  default = "anthropic.claude-3-sonnet-20240229-v1:0"
}
