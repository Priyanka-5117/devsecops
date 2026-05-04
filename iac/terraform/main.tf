# ✅ FIX 1: S3 bucket WITH encryption
resource "aws_s3_bucket" "data_bucket" {
  bucket = "devsecops-test-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encryption" {
  bucket = aws_s3_bucket.data_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ✅ FIX 2: Security group with restricted access
resource "aws_security_group" "restricted_sg" {
  name = "restricted-security-group"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ✅ FIX 3: EC2 WITH monitoring enabled
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  monitoring    = true
}
