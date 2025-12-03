resource "aws_opensearchserverless_security_policy" "kb_encryption" {
  name = "${var.kb_name}-encryption"
  type = "encryption"
  policy = jsonencode({
    Rules = [{
      ResourceType = "collection"
      Resource     = ["collection/${var.kb_name}"]
    }]
    AWSOwnedKey = true
  })
}

resource "aws_opensearchserverless_security_policy" "kb_network" {
  name = "${var.kb_name}-network"
  type = "network"
  policy = jsonencode([{
    Rules = [{
      ResourceType = "collection"
      Resource     = ["collection/${var.kb_name}"]
    }]
    AllowFromPublic = true
  }])
}

resource "aws_opensearchserverless_access_policy" "kb_access" {
  name = "${var.kb_name}-access"
  type = "data"
  policy = jsonencode([{
    Rules = [{
      ResourceType = "collection"
      Resource     = ["collection/${var.kb_name}"]
      Permission   = ["aoss:*"]
    }, {
      ResourceType = "index"
      Resource     = ["index/${var.kb_name}/*"]
      Permission   = ["aoss:*"]
    }]
    Principal = [
      data.aws_caller_identity.current.arn,
      var.kb_role_arn
    ]
  }])
}

resource "aws_opensearchserverless_collection" "kb_collection" {
  name = var.kb_name
  type = "VECTORSEARCH"
  depends_on = [
    aws_opensearchserverless_security_policy.kb_encryption,
    aws_opensearchserverless_security_policy.kb_network
  ]
}
