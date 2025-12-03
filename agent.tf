resource "aws_bedrockagent_agent" "rag_agent" {
  agent_name              = var.agent_name
  agent_resource_role_arn = var.kb_role_arn
  foundation_model        = var.model_id
  instruction             = "You are a helpful assistant that answers questions using the knowledge base. Always search the knowledge base before answering."
}

resource "aws_bedrockagent_agent_knowledge_base_association" "kb_association" {
  agent_id             = aws_bedrockagent_agent.rag_agent.id
  knowledge_base_id    = aws_bedrockagent_knowledge_base.kb.id
  description          = "Knowledge base for RAG"
  knowledge_base_state = "ENABLED"
}

resource "aws_bedrockagent_agent_alias" "rag_agent_alias" {
  agent_id         = aws_bedrockagent_agent.rag_agent.id
  agent_alias_name = "prod"
  depends_on       = [aws_bedrockagent_agent_knowledge_base_association.kb_association]
}
