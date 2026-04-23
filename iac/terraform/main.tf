resource "aws_s3_bucket" "data_bucket" {
bucket = "devsecops-test-bucket"
}
resource "aws_security_group" "open_sg" {
name = "open-security-group"
ingress {
from_port = 0
to_port = 0
protocol = "-1"
cidr_blocks = ["0.0.0.0/0"]
}
}
resource "aws_instance" "web" {
ami = "ami-0c55b159cbfafe1f0"
instance_type = "t2.micro"
monitoring = false
}
