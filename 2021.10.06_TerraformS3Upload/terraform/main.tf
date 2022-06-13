terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.60.0"
    }
  }
}

provider "aws" {
  # Configuration options
  profile = "aws_admin"
  region  = "us-west-1"
}

variable "website_root" {
  type        = string
  description = "Path to the root of website content"
  default     = "../content"
}

resource "aws_s3_bucket" "my_static_website" {
  bucket = "blog-example-m9wtv64y"
  acl    = "private"

  website {
    index_document = "index.html"
  }
}

# If using an external CLI tool to determine file MIME types
#
#data "external" "get_mime" {
#  for_each = local.website_files
#  program  = ["bash", "./get_mime.sh"]
#  query = {
#    filepath : "${var.website_root}/${each.key}"
#  }
#}

locals {
  website_files = fileset(var.website_root, "**")

  file_hashes = {
    for filename in local.website_files :
    filename => filemd5("${var.website_root}/${filename}")
  }

  mime_types = jsondecode(file("mime.json"))
}

resource "aws_s3_bucket_object" "file" {
  for_each = local.website_files

  bucket       = aws_s3_bucket.my_static_website.id
  key          = each.key
  source       = "${var.website_root}/${each.key}"
  source_hash  = local.file_hashes[each.key]
  acl          = "public-read"
  content_type = lookup(local.mime_types, regex("\\.[^.]+$", each.key), null)
  # content_type = data.external.get_mime[each.key].result.mime
}

output "website_endpoint" {
  value = aws_s3_bucket.my_static_website.website_endpoint
}

# If using cloudfront and cloudfront invalidations:
#
#resource "null_resource" "invalidate_cache" {
#  triggers = local.file_hashes
#
#  provisioner "local-exec" {
#    command = "aws --profile=aws_admin cloudfront create-invalidation --distribution-id=${aws_cloudfront_distribution.my_distribution.id} --paths=/*"
#  }
#}
