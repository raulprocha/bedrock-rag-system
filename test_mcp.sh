#!/bin/bash

# Aguarde o deploy completar e pegue os IDs
AGENT_ID=$(terraform output -raw agent_id 2>/dev/null)
AGENT_ALIAS_ID=$(terraform output -raw agent_alias_id 2>/dev/null)
KB_ID=$(terraform output -raw knowledge_base_id 2>/dev/null)

if [ -z "$AGENT_ID" ]; then
    echo "Erro: Agent ainda não foi criado. Execute 'terraform apply' primeiro."
    exit 1
fi

echo "=== Testando MCP Server ==="
echo "Agent ID: $AGENT_ID"
echo "Agent Alias ID: $AGENT_ALIAS_ID"
echo "KB ID: $KB_ID"
echo ""

# Teste 1: Listar tools
echo '{"method": "tools/list"}' | python3 mcp_server.py

echo ""
echo "=== Para usar com Kiro CLI ==="
echo "1. Copie mcp_config.json para ~/.config/kiro-cli/mcp.json"
echo "2. Reinicie o Kiro CLI"
echo "3. Use: 'Pergunte ao agent sobre [seu tópico]'"
