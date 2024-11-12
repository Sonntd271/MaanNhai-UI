provider "aws" {
  region = var.region
}

resource "aws_instance" "maannhai-server" {
  ami = var.amis[var.region]
  instance_type = "t2.micro"
  key_name = aws_key_pair.maannhai-key.key_name
  vpc_security_group_ids = [ aws_security_group.maannhai-sg.id ]
  
  provisioner "file" {
    source = "../scripts/maannhai_server.sh"
    destination = "/tmp/maannhai_server.sh"
  }

  provisioner "remote-exec" {
    inline = [ 
        "sudo chmod +x /tmp/maannhai_server.sh",
        "sudo /tmp/maannhai_server.sh",
        "cd"
    ]
  }

  connection {
    user = var.user
    private_key = file("../maannhai-key")
    host = self.public_ip
  }
}
