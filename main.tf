provider "aws" {
  region  = var.region
  profile = "CIANDT-Contributor-253223147282"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
