output "jenkins_ip" {
  value = aws_instance.jenkins-server.public_ip
}