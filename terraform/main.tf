# ---------------------------
# Github
# ---------------------------
resource "github_repository" "url_shortener" {
  name            = "url-shortener"
  visibility      = "private"
  has_issues      = true
  has_projects    = true
  has_downloads   = true
  has_discussions = false
  has_wiki        = false
}

# ---------------------------
# AWS EC2
# ---------------------------
data "aws_ami" "debian_12" {
  most_recent = true
  owners      = ["aws-marketplace"]
  filter {
    name   = "name"
    values = ["debian-12-amd64-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_subnet" "default_availability_zone" {
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "Default subnet for ap-northeast-2a"
  }
}

resource "aws_security_group" "url_shortener_sg" {
  name        = "url-shortener-sg"
  description = "Allow incoming traffic to the Debian EC2 Instance"
  vpc_id      = aws_default_vpc.default.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming HTTP connections"
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming HTTPS connections"
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming SSH connections"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "tls_private_key" "url_shortener_key_pair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "url_shortener_key_pair" {
  key_name   = "url-shortener-key-pair"
  public_key = tls_private_key.url_shortener_key_pair.public_key_openssh
}

resource "local_file" "ssh_key" {
  filename = "vars/${aws_key_pair.url_shortener_key_pair.key_name}.pem"
  content  = tls_private_key.url_shortener_key_pair.private_key_pem
}

resource "aws_instance" "url_shortener_vm" {
  ami                         = data.aws_ami.debian_12.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_default_subnet.default_availability_zone.id
  vpc_security_group_ids      = [aws_security_group.url_shortener_sg.id]
  associate_public_ip_address = true
  source_dest_check           = false
  key_name                    = aws_key_pair.url_shortener_key_pair.key_name
  user_data                   = null
  user_data_replace_on_change = true

  root_block_device {
    volume_size           = 8
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  tags = {
    Name = "URL Shortener VM"
  }
}

resource "aws_ec2_instance_state" "url_shortener_vm" {
  instance_id = aws_instance.url_shortener_vm.id
  state       = "stopped"
}
