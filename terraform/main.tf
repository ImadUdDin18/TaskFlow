resource "aws_instance" "taskflow_server" {
  ami                    = "ami-0521cb2d60cfbb1a6"
  instance_type          = "t3.micro"
  key_name               = "aws-internship-key"
  subnet_id              = "subnet-0feff7bed32f77a4f"
  vpc_security_group_ids = ["sg-090903194a48d1160"]
  iam_instance_profile   = "EC2-S3-Admin-Role"

  tags = {
    Name = "My-First-Aws-Server"
  }
  lifecycle {
    ignore_changes = [user_data]
  }
}