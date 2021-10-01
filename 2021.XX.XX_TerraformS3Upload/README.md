# Abusing Terraform to Upload Static Websites to S3

## Purpose

Demonstrate how to use Terraform to create and manage content and its metadata
(wrt MIME types and caching) on S3.

## Blog post

- 2021.XX.XX: [Abusing Terraform to Upload Static Websites to S3](https://www.tangramvision.com/blog/abusing-terraform-to-upload-static-websites-to-s3)

## Usage

This project uses Terraform (get it from
https://www.terraform.io/downloads.html). To run `main.tf`, you'll need:

- AWS credentials in `~/.aws/credentials` under a profile named `aws_admin` (or
you can change the profile name in `main.tf`)
- To change the bucket name to something unique

Then, run Terraform with:

```
# Initialize terraform in the current directory and download the AWS provider
terraform init
# Preview what changes will be made
terraform plan
# Make the changes (create and populate the S3 bucket)
terraform apply
```