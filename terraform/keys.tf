resource "aws_key_pair" "maannhai-key" {
  key_name = "maannhai-key"
  public_key = file("../maannhai-key.pub")
}
