resource "aws_s3_bucket" "kb_data" {
  bucket = "${var.kb_name}-data-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "kb_data" {
  bucket = aws_s3_bucket.kb_data.id
  versioning_configuration {
    status = "Enabled"
  }
}
