output "knowledge_base_id" {
  value = aws_bedrockagent_knowledge_base.kb.id
}

output "knowledge_base_arn" {
  value = aws_bedrockagent_knowledge_base.kb.arn
}

output "data_source_id" {
  value = aws_bedrockagent_data_source.kb_data_source.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.kb_data.bucket
}

output "opensearch_collection_endpoint" {
  value = aws_opensearchserverless_collection.kb_collection.collection_endpoint
}

output "agent_id" {
  value = aws_bedrockagent_agent.rag_agent.id
}

output "agent_alias_id" {
  value = aws_bedrockagent_agent_alias.rag_agent_alias.id
}
